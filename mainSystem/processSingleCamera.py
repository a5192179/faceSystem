from multiprocessing import Process
from tool.camera import add_camera_args, Camera
from mainSystem import showResult
import cv2
import argparse
import datetime

from module.detectFace.algo import detectFaceCaffe
from module.verifyFace.algo import verifyFace
from module.statisticTime import statisticTime

class singleCameraProcessor(Process):
    def __init__(self, config, inputStream, cameraID):
        Process.__init__(self)
        self.inputStream = inputStream
        self.cameraID = cameraID
        

    def run(self):
        print('run')
        faceDetector = detectFaceCaffe.faceDetector()
        faceVerifier = verifyFace.faceVerifier()
        timeStatistician = statisticTime.timeStatistician(faceVerifier.facebase)
        print('load model end------------')
        parser = argparse.ArgumentParser()
        parser = add_camera_args(parser, self.inputStream)
        args = parser.parse_args()
        cap = Camera(args)
        frameId = 0
        finalInfos = []
        while True:
            # while frameId < 20:
            # grab the next frame from the stream, store the current timestamp, and store the new date
            # _, frame = cap.read()
            frame = cap.read()
            if frame is None:
                break
            frameId += 1
            print('get frame', frameId)
            # cv2.imshow('frame', frame)
            # cv2.waitKey(500)
            # add time to frame
            nowTime = datetime.datetime.now()
            # if (nowTime - imgTime).seconds < 10:
            #     continue
            imgTime = nowTime
            # detect faces
            faces = faceDetector.detectFace(frame)
            print('detect face', len(faces))
            # verify faces
            bInBases, identities, ages, genders = faceVerifier.verifyFaces(faces)
            #==================================
            # savePath = '../data/testFace'
            # for i_face in range(len(faces)):
            #     imgName = str(frameId) + '-' + str(identities[i_face]) + '.jpg'
            #     cv2.imwrite(savePath + '/' + imgName, faces[i_face])
            #==================================
            # statistic time
            stayTimes = timeStatistician.getStayTimebyIdentities(identities, imgTime)
            finalStayTimes = timeStatistician.getFinalStayTime()
            
            if len(finalStayTimes) > 0:
                for identity in finalStayTimes:
                    age, gender = faceVerifier.getAgeAndGender(identity)
                    print('------')
                    print('identity:', identity,
                          'age:', age,
                          'gender:', gender,
                          'final stay time:', finalStayTimes[identity])
                    print('------')
                    imgStr = 'id:' + str(identity) + ',age:' + age + ',gender:' + gender + ',stayTime:' + str(stayTime)
                    finalInfos.append(imgStr)

            index = 0
            faceInfos = []
            for face in faces:
                bInBase = bInBases[index]
                identity = identities[index]
                age = ages[index]
                gender = genders[index]
                stayTime = stayTimes[index]
                width = face.shape[1]
                high = face.shape[0]
                print('rate:', high/width, 'high:', high, 'width:', width)
                imgStr = str(round(high/width, 2)) + ',' + str(bInBase) + ',' + str(identity) + ',' + age + ',' + gender + ',' + str(round(stayTime, 2))
                faceInfos.append(imgStr)
                # cv2.putText(face, imgStr, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)
                # cv2.imshow('frame', face)
                # cv2.waitKey(500)
                # =============================
                savePath = '../data/testFace'
                for i_face in range(len(faces)):
                    imgName = str(frameId) + '-' + str(identities[i_face]) + '.jpg'
                    cv2.imwrite(savePath + '/' + imgName, faces[i_face])
                # =============================
                index += 1
            
            showResult.showResult(frame, str(frameId), faces, faceInfos, finalInfos)
            print('-------------frame end, id:', frameId, '--------------')
            # return bInBases, identities, ages, genders, stayTimes