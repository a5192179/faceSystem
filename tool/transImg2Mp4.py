import cv2

videoSavePath = 'D:/project/touristAnalyse/data/videos'
imgFolder = 'D:/project/touristAnalyse/data/collectLS120701/img'
countFrame = -1
width = 1420
high = 750
imgSize = (width, high)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
videoOut = cv2.VideoWriter()
videoID = 0
videoOut.open(videoSavePath + '/test6.mp4', fourcc, 25, imgSize, True)

for i in range(500):
    imgPath = imgFolder + '/' + str(i) + '.jpg'
    frame = cv2.imread(imgPath)
    videoOut.write(frame)

videoOut.release()