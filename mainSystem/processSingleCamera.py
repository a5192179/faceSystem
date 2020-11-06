from multiprocessing import Process
from tool.camera import add_camera_args, Camera
import cv2
import argparse
import datetime

from module.detectFace.algo import detectFace
from module.verifyFace.algo import verifyFace
from module.statisticTime import statisticTime

class singleCameraProcessor(Process):
    def __init__(self, config, inputStream, cameraID):
        Process.__init__(self)
        self.inputStream = inputStream
        self.cameraID = cameraID

        # ====================
        self.faceDetector = detectFace.faceDetector()
        # self.faceVerifier = verifyFace.faceVerifier()
        # self.timeStatistician = statisticTime.timeStatistician(self.faceVerifier.facebase)
        # ====================
        print('init end------------')

    def run(self):
        print('run')
        # parser = argparse.ArgumentParser()
        # parser = add_camera_args(parser, self.inputStream)
        # args = parser.parse_args()
        # cap = Camera(args)
        # while True:
        #     # grab the next frame from the stream, store the current timestamp, and store the new date
        #     # _, frame = cap.read()
        #     frame = cap.read()
        #     if frame is None:
        #         break
        #     # add time to frame
        #     imgTime = datetime.datetime.now()
        #     # detect faces
        #     faces = self.faceDetector.detectFace(frame)
        #     # verify faces
        #     bInBases, identities, ages, genders = self.faceVerifier.verifyFaces(faces)
        #     # statistic time
        #     stayTimes = self.timeStatistician.getStayTimebyIdentities(identities, imgTime)

        #     index = 0
        #     for face in faces:
        #         bInBase = bInBases[index]
        #         identity = identities[index]
        #         age = ages[index]
        #         gender = genders[index]
        #         stayTime = stayTimes[index]
        #         str = bInBase + ',' + identity + ',' + age + ',' + gender + ',' + stayTime
        #         cv2.putText(face, str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)
        #         cv2.imshow('frame', face)
        #         cv2.waitKey(1500)
        #         index += 1
        #     return bInBases, identities, ages, genders, stayTimes