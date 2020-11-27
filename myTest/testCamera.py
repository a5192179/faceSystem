import cv2
inputPath = "rtsp://admin:1234abcd@192.168.1.132:554/Streaming/Channels/1"
camera = cv2.VideoCapture(inputPath)
cv2.namedWindow('MyCamera')

while True:
    success, frame = camera.read()
    cv2.imshow('MyCamera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyWindow('MyCamera')
camera.release()