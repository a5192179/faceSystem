from multiprocessing import Process
# from tool.camera import add_camera_args, Camera
from main_2015 import showResult
import cv2
# import argparse
import datetime
import os
import shutil
import time

from module.detectFace.algo import detectFaceIF as detectFace
from module.verifyFace.algo import verifyFace
from module.statisticTime import statisticTime
from module.detectSideFace.algo import detectSideFace

from common import readInput

from queue import Queue
import base64
import json
class singleCameraProcessor(Process):
    def __init__(self, config, inputStream, cameraID, identityBase, q):
        Process.__init__(self)
        self.inputStream = inputStream
        self.cameraID = cameraID

        # output
        # self.resultSavePath = config.get('output', 'resultSavePath')
        # self.suffix = config.get('output', 'suffix')
        self.resultSaveFolder = config.get('output', 'resultSaveFolder') + '_' + cameraID

        # run mode
        self.bShowResult = config.getboolean('runMode', 'showResult')
        self.bSaveResult = config.getboolean('runMode', 'saveResult')
        self.skipMode = config.get('runMode', 'skipMode') # frame time
        self.skipFrame = config.getint('runMode', 'skipFrame')
        self.skipTime = config.getint('runMode', 'skipTime') # second

        # algo
        self.leaveThreshold = config.getfloat('algo', 'leaveThreshold')
        self.leaveErrorThreshold = config.getfloat('algo', 'leaveErrorThreshold')
        self.sideFaceThreshold = config.getfloat('algo', 'sideFaceThreshold')
        self.similarThreshold = config.getfloat('algo', 'similarThreshold')
        self.ageScale = config.getfloat('algo', 'ageScale')
        self.useGPU = config.getboolean('algo', 'useGPU')

        if self.bSaveResult:
            if not os.path.exists(self.resultSaveFolder):
                # print('no save path')
                os.mkdir(self.resultSaveFolder)
            else:
                shutil.rmtree(self.resultSaveFolder)
                # print('remove')
                os.mkdir(self.resultSaveFolder)
        
        self.identityBase = identityBase
        print('init success')

        self.test = 0
        self.Q = q

    def read(self):
		# return next frame in the queue
        print('read, self.test', self.test)
        # print('len(self.Q.queue):', len(self.Q.queue))
        # if type(self.Q) == type(1):
        #     self.Q = Queue(maxsize=27)
        # print('len(self.Q.queue):', len(self.Q.queue))
        # frame = self.Q.get()
        # print('frame', frame)
        # return frame
        return

    def run(self):
        # self.Q = Queue(maxsize=27)
        print('camera ', self.cameraID, ' run')
        faceDetector = detectFace.faceDetector(useGPU = self.useGPU)
        sideFaceDetector = detectSideFace.sideFaceDetector(sideFaceThreshold = self.sideFaceThreshold)
        faceVerifier = verifyFace.faceVerifier(self.identityBase, similarThreshold = self.similarThreshold, ageScale = self.ageScale, useGPU = self.useGPU)
        timeStatistician = statisticTime.timeStatistician(self.identityBase, self.cameraID, self.leaveThreshold, self.leaveErrorThreshold)
        inputReader = readInput.InputReader(self.inputStream)
        print('load model end------------')
        # parser = argparse.ArgumentParser()
        # parser = add_camera_args(parser, self.inputStream)
        # args = parser.parse_args()
        # cap = Camera(args)
        # fps = cap.get_fps()
        # cap = Camera(args)
        # fps = cap.get_fps()
        # bRtsp = False
        # if self.inputStream == '0':
        #     inputStream = 0
        #     cap = cv2.VideoCapture(inputStream)
        # elif self.inputStream.find('rtsp') != -1:
        #     cap = Camera(args)
        #     fps = cap.get_fps()
        #     bRtsp = True
        # else:
        #     cap = cv2.VideoCapture(self.inputStream)
        # if not bRtsp:
        #     fps = cap.get(cv2.CAP_PROP_FPS)
        fps = inputReader.getFPS()
        frameId = 0
        lastFrameId = 0
        finalInfos = []
        while True:
            # while frameId < 20:
            # grab the next frame from the stream, store the current timestamp, and store the new date
            # _, frame = cap.read()
            # if bRtsp:
            #     frame = cap.read()
            # else:
            #     success,frame = cap.read()
            #     if not success:
            #         break
            frame, bStop = inputReader.read()
            if bStop:
                break
            if frame is None:
                continue
            frameId += 1

            # print('get frame', frameId)
            if frameId < 20:
                # print('skip frame', frameId)
                continue

            # add time to frame
            if self.skipMode == 'time':
                if (frameId - lastFrameId) / fps < self.skipTime:
                    # print('skip by time, frame:', frameId)
                    continue
            elif self.skipMode == 'frame':
                if frameId - lastFrameId < self.skipFrame:
                    # print('skip by frame, frame:', frameId)
                    # cv2.waitKey(50)
                    continue
            elif self.skipMode == 'none':
                pass
            else:
                print('error, self.skipMode is', self.skipMode)
            ts_begin = time.time()
            lastFrameId = frameId

            # detect faces
            ts = time.time()
            oriFaces = faceDetector.detectFace(frame)
            print('detect time:', time.time() - ts)
            # print('detect face', len(oriFaces))
            ts = time.time()
            faces = sideFaceDetector.getFrontFaces(oriFaces)
            print('side time:', time.time() - ts)
            print('frame:', frameId, 'front face:', len(faces))
            # verify faces
            ts = time.time()
            bInBases, identities, ages, genders = faceVerifier.verifyFaces(faces)
            print('verify time:', time.time() - ts)
            #==================================
            # savePath = '../data/testFace'
            # for i_face in range(len(faces)):
            #     imgName = str(frameId) + '-' + str(identities[i_face]) + '.jpg'
            #     cv2.imwrite(savePath + '/' + imgName, faces[i_face])
            #==================================
            # statistic time
            ts = time.time()
            # print('before time:', time.time() - ts_begin)
            # ts = time.time()
            stayTimes = timeStatistician.getStayTimebyIdentities(identities, frameId, fps)
            # print('stayTimes time:', time.time() - ts)
            # ts = time.time()
            finalStayTimes = timeStatistician.getFinalStayTime(frameId, fps)
            # print('finalStayTimes time:', time.time() - ts)
            dataList = [] # output for zheng
            if len(finalStayTimes) > 0:
                # ts = time.time()
                for identity in finalStayTimes:
                    age, gender = faceVerifier.getAgeAndGender(identity)
                    finalStayTime = finalStayTimes[identity]
                    # print('------')
                    # print('identity:', identity,
                    #       'age:', age,
                    #       'gender:', gender,
                    #       'final stay time:', finalStayTime)
                    # print('------')
                    imgStr = 'ID:' + identity + ', Age:' + age + ', Gender:' + gender + ', Time:' + str(round(finalStayTime, 2))
                    finalInfos.append(imgStr)
                    outputLine = {"sex": gender, "age":age, "stayTime":finalStayTime}
                    dataList.append(outputLine)
                # print('【finalStayTimes output】 time:', time.time() - ts)
            # for each frame statistic show
            # ts = time.time()
            index = 0
            faceInfos = []
            for face in faces:
                bInBase = bInBases[index]
                identity = identities[index]
                age = ages[index]
                gender = genders[index]
                stayTime = stayTimes[index]
                # width = face.shape[1]
                # high = face.shape[0]
                # # print('rate:', high/width, 'high:', high, 'width:', width)
                if bInBase:
                    inBaseStr = 'Existing'
                else:
                    inBaseStr = 'New'
                imgStr = inBaseStr + '-ID : ' + identity + '-Age : ' + age + '-Gender : ' + gender + '-Time : ' + str(round(stayTime, 2))
                faceInfos.append(imgStr)
                index += 1
                # cv2.putText(face, imgStr, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)
                # cv2.imshow('frame', face)
                # cv2.waitKey(500)
                # =============================
                # savePath = '../output/testFaceResult'
                # for i_face in range(len(faces)):
                #     imgName = str(frameId) + '-' + str(identities[i_face]) + '.jpg'
                #     cv2.imwrite(savePath + '/' + imgName, faces[i_face])
                # =============================
            # print('finalInfos:', len(finalInfos))
            if self.bShowResult or self.bSaveResult:
                showResult.showResult(frame, str(frameId), faces, faceInfos, finalInfos, self.bShowResult, self.bSaveResult, self.resultSaveFolder)
            if self.bSaveResult:
                shutil.copy('./config/config.ini', self.resultSaveFolder + '/config.ini')
            print('end time:', time.time() - ts)
            print('[all] time:', time.time() - ts_begin)

            # ==================
            resultFrame = showResult.drawResult(frame, str(frameId), faces, faceInfos, finalInfos)
            if not self.Q.full():
                print('put')
                self.Q.put(resultFrame)
            else:
                print('sleep')
                time.sleep(0.28)
                continue

            writeFrameJson(faces, bInBases, identities, ages, genders, stayTimes)
            writeFinalJson(finalInfos)
            # ==================
            # self.test = len(self.Q.queue)
            # print('run, self.test', self.test)
            # print('len(self.Q.queue):', len(self.Q.queue))
            print('-------------frame end, id:', frameId, '--------------')

def writeFrameJson(faces, bInBases, identities, ages, genders, stayTimes, jsonPath = './main_2015/intrusion.json'):
    infoList = []
    index = 0
    for face in faces:
        info = {}
        # bInBase = bInBases[index]
        identity = identities[index]
        age = ages[index]
        gender = genders[index]
        stayTime = stayTimes[index]
        info['identity'] = identity
        info['age'] = age
        info['gender'] = gender
        info['stayTime'] = str(round(stayTime, 2))
        img = cv2.imencode('.jpg', face)[1]
        personImg = str(base64.b64encode(img))[2:-1]
        info['person'] = personImg
        infoList.append(info)
        index += 1

    if not os.path.exists(jsonPath):
        with open(jsonPath, 'w', encoding='utf-8') as f:
            json.dump(infoList, f, ensure_ascii=False)
    else:
        with open(jsonPath, 'r') as f:
            load_dict = json.load(f)
            num_item = len(load_dict)
            if num_item > 15:
                iterNum = 15
            else:
                iterNum = num_item
            for i in range(iterNum):
                item_dict = load_dict[i]
                if identities.count(item_dict['identity'].split(' ')[0]) > 0:
                    continue
                infoList.append(item_dict)
        with open(jsonPath, 'w', encoding='utf-8') as f:
            json.dump(infoList, f, ensure_ascii=False)

def writeFinalJson(finalInfos, jsonPath = './main_2015/leave.json'):
    infoList = []
    index = 0
    finalInfoDict = {'leave':finalInfos}

    infoList.append(finalInfoDict)
    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(infoList, f, ensure_ascii=False)

# def json_str(personImg, personTime, personPath):
#     dict = {}
#     dict["info"] = 'WARNING'
#     dict["time"] = personTime
#     dict["person"] = personImg
#     dict["path"] = personPath
#     return dict

# def writeJson(img, time, age, jsonPath):
#     obj = json_str(img, personTime, personPath)
#     item_list = []
#     if not os.path.exists(jsonPath):
#         item_list.append(obj)
#         with open(jsonPath, 'w', encoding='utf-8') as f:
#             json.dump(item_list, f, ensure_ascii=False)
#     else:
#         with open(jsonPath, 'r') as f:
#             load_dict = json.load(f)
#             num_item = len(load_dict)
#             for i in range(num_item):
#                 item_dict = load_dict[i]
#                 item_list.append(item_dict)
#         item_list.append(obj)
#         with open(jsonPath, 'w', encoding='utf-8') as f:
#             json.dump(item_list, f, ensure_ascii=False)

# def gen_data(faces, personROI, box):
#     presonID = len(feats)
#     x, y, w, h = box
#     img = cv2.imencode('.jpg', personROI)[1]
#     personImg = str(base64.b64encode(img))[2:-1]