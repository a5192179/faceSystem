from imutils.video import VideoStream
import cv2
import os
import time
class InputReader():
    def __init__(self, inputStream):
        if inputStream.endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso')):
            self.inputType = 'videoFile'
            if not os.path.exists(inputStream):
                raise BaseException('miss file:' + inputStream)
            self.cap = cv2.VideoCapture(inputStream)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        elif inputStream[0:4] == 'rtsp':
            self.inputType = 'rtsp'
            cap = cv2.VideoCapture(inputStream)
            fpsGoal = cap.get(cv2.CAP_PROP_FPS)
            self.fps = fpsGoal
            cap.release()
            self.timeDeltaGoal = 1 / fpsGoal
            # start
            cap = VideoStream(inputStream)
            self.cap = cap.start()
            # init time
            self.lastFrameTime = time.time()
        elif inputStream.isdecimal():
            self.inputType = 'camera'
            self.cap = cv2.VideoCapture(int(inputStream))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            raise BaseException('wrong input:' + inputStream)
        self.noneFrameNum = 0

    def read(self):
        bStop = False
        if self.inputType == 'rtsp':
            timeNow = time.time()
            deltaTime = self.timeDeltaGoal - (timeNow - self.lastFrameTime)
            # print('timeNow', timeNow, 'lastFrameTime', self.lastFrameTime, 'deltaTime', deltaTime)
            if deltaTime < 0:
                deltaTime = 0
            time.sleep(deltaTime)
            frame = self.cap.read()
            self.lastFrameTime = timeNow + deltaTime
            if frame is None:
                print('InputStream read none')
                self.noneFrameNum += 1
                if self.noneFrameNum > 10:
                    bStop = True
                    print('InputStream end')
            else:
                self.noneFrameNum = 0
            return frame, bStop
        elif self.inputType == 'camera' or self.inputType == 'videoFile':
            success,frame = self.cap.read()
            if not success:
                print('InputStream read none')
                frame = None
            if frame is None:
                self.noneFrameNum += 1
                if self.noneFrameNum > 10:
                    bStop = True
                    print('InputStream end')
            else:
                self.noneFrameNum = 0
            return frame, bStop

    def getFPS(self):
        return self.fps

    def release(self):
        if self.inputType == 'videoFile' or self.inputType == 'camera':
            self.cap.release()

if __name__ == "__main__":
    path = "D:/project/touristAnalyse/data/videos/test2.mp4"
    # path = "rtsp://admin:1234abcd@192.168.1.132:554/Streaming/Channels/1"
    path = '0'
    inputReader = InputReader(path)
    fps = inputReader.getFPS()
    print('set fps', fps)
    frameNum = 0
    timeBegin = time.time()
    while frameNum < 2000:
        frame, bStop = inputReader.read()
        if bStop:
            break
        if not frame is None:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        else:
            continue
        frameNum += 1
        if (frameNum % 100 == 0):
            timeEnd = time.time()
            print('test fps', frameNum / (timeEnd - timeBegin))

    print('frameNum', frameNum)