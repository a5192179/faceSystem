import numpy as np
import cv2
import math
def SMD2(img):
    '''
    :param img:narray 二维灰度图像
    :return: float 图像约清晰越大
    '''
    shape = np.shape(img)
    out = 0
    for x in range(0, shape[0]-1):
        for y in range(0, shape[1]-1):
            out+=math.fabs(int(img[x,y])-int(img[x+1,y]))*math.fabs(int(img[x,y]-int(img[x,y+1])))
    return out

def isClear(img, distinctionThreshold = 0.3):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    distinction = SMD2(imgGray) / (imgGray.shape[0] * imgGray.shape[1])
    print(distinction)
    if distinction > distinctionThreshold:
        return True
    else:
        return False

if __name__ == "__main__":
    imgPath = 'D:/project/touristAnalyse/output/ISCameraLS_000003/face/336-0.jpg'
    print(imgPath)
    img = cv2.imread(imgPath)
    isClear(img)
    print('---------------------------------------------------')