from multiprocessing import Process
from tool.camera import add_camera_args, Camera
from mainSystem import showResult
import cv2
import argparse
import datetime
import os
import shutil
import time

from module.detectFace.algo import detectFaceCaffe
from module.verifyFace.algo import verifyFace
from module.statisticTime import statisticTime
from module.detectSideFace.algo import detectSideFace

class singleCameraProcessor(Process):
    def __init__(self, config, inputStream, cameraID):
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


        if self.bSaveResult:
            if not os.path.exists(self.resultSaveFolder):
                # print('no save path')
                os.mkdir(self.resultSaveFolder)
            else:
                shutil.rmtree(self.resultSaveFolder)
                # print('remove')
                os.mkdir(self.resultSaveFolder)
        

    def run(self):
        print('camera ', self.cameraID, ' run')
        faceDetector = detectFaceCaffe.faceDetector()
        sideFaceDetector = detectSideFace.sideFaceDetector(sideFaceThreshold = self.sideFaceThreshold)
        faceVerifier = verifyFace.faceVerifier(similarThreshold = self.similarThreshold, ageScale = self.ageScale)
        timeStatistician = statisticTime.timeStatistician(faceVerifier.facebase, self.leaveThreshold, self.leaveErrorThreshold)
        # print('load model end------------')
        parser = argparse.ArgumentParser()
        parser = add_camera_args(parser, self.inputStream)
        args = parser.parse_args()
        # cap = Camera(args)
        # fps = cap.get_fps()
        cap = cv2.VideoCapture(self.inputStream)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frameId = 0
        lastFrameId = 0
        finalInfos = []
        while True:
            # while frameId < 20:
            # grab the next frame from the stream, store the current timestamp, and store the new date
            # _, frame = cap.read()
            success,frame = cap.read()
            if not success:
                break
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
            # if frameId == 24:
            #     cv2.waitKey(11000)
            #     a=1
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
                    imgStr = 'id:' + identity + ',age:' + age + ',gender:' + gender + ',stayTime:' + str(finalStayTime)
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
                imgStr = str(bInBase) + ',' + identity + ',' + age + ',' + gender + ',' + str(round(stayTime, 2))
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
            print('-------------frame end, id:', frameId, '--------------')