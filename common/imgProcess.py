import numpy as np
import cv2

def getSquareByRect(img, rect, wholeImg):
    # rect: [left_top.u, left_top.v, width, high]
    tlu = rect[0] # top left u
    tlv = rect[1] # top left v
    width = rect[2]
    high = rect[3]
    wholeW = wholeImg.shape[1]
    wholeH = wholeImg.shape[0]
    if width > high:
        base = width - high
        if base % 2 == 0:
            addTop = int(base / 2)
            addButtom = addTop
        else:
            addTop = int((base + 1) / 2)
            addButtom = addTop - 1

        if tlv - addTop < 0:
            black = np.zeros([addTop - tlv, width, 3], dtype='uint8')
            newImg = np.vstack((black, wholeImg[0:tlv+high, tlu:tlu+width, :]))
        else:
            newImg = wholeImg[tlv - addTop:tlv+high, tlu:tlu+width, :]
        if tlv + high + addButtom > wholeH:
            black = np.zeros([addButtom - (wholeH - tlv - high), width, 3], dtype='uint8')
            newImg = np.vstack((newImg, wholeImg[tlv+high:wholeH, tlu:tlu+width, :], black))
        else:
            newImg = np.vstack((newImg, wholeImg[tlv+high:tlv+high+addButtom, tlu:tlu+width, :]))
    else:
        base = high - width
        if base % 2 == 0:
            addLeft = int(base / 2)
            addRight = addLeft
        else:
            addLeft = int((base + 1) / 2)
            addRight = addLeft - 1

        if tlu - addLeft < 0:
            black = np.zeros([high, addLeft - tlu, 3], dtype='uint8')
            newImg = np.hstack((black, wholeImg[tlv:tlv+high, 0:tlu+width, :]))
        else:
            newImg = wholeImg[tlv:tlv+high, tlu - addLeft:tlu+width, :]
        if tlu + width + addRight > wholeW:
            black = np.zeros([high, addRight - (wholeW - tlu - width), 3], dtype='uint8')
            newImg = np.hstack((newImg, wholeImg[tlv:tlv+high, tlu+width:wholeW, :], black))
        else:
            newImg = np.hstack((newImg, wholeImg[tlv:tlv+high, tlu+width:+width+addRight, :]))
    return newImg

def getSquareRectByRect(rect, wholeImg):
    # rect: [left_top.u, left_top.v, width, high]
    tlu = rect[0] # top left u
    tlv = rect[1] # top left v
    width = rect[2]
    high = rect[3]
    wholeW = wholeImg.shape[1]
    wholeH = wholeImg.shape[0]
    if width > high:
        base = width - high
        if base % 2 == 0:
            addTop = int(base / 2)
            addButtom = addTop
        else:
            addTop = int((base + 1) / 2)
            addButtom = addTop - 1

        if tlv - addTop < 0:
            newTlu = tlu
            newTlv = 0
            newWidth = width
            newHigh = high + addTop + addButtom
        elif tlv + high + addButtom >= wholeH:
            newTlu = tlu
            newTlv = wholeH - (high + addTop + addButtom) - 1
            newWidth = width
            newHigh = high + addTop + addButtom
        else:
            newTlu = tlu
            newTlv = tlv - addTop
            newWidth = width
            newHigh = high + addButtom
    else:
        base = high - width
        if base % 2 == 0:
            addLeft = int(base / 2)
            addRight = addLeft
        else:
            addLeft = int((base + 1) / 2)
            addRight = addLeft - 1

        if tlu - addLeft < 0:
            newTlu = 0
            newTlv = tlv
            newWidth = width + addLeft + addRight
            newHigh = high
        elif tlu + width + addRight >= wholeW:
            newTlu = wholeW - (width + addLeft + addRight) - 1
            newTlv = tlv
            newWidth = width + addLeft + addRight
            newHigh = high
        else:
            newTlu = tlu - addLeft
            newTlv = tlv
            newWidth = width + addRight
            newHigh = high
    newRect = [newTlu, newTlv, newWidth, newHigh]
    return newRect

def getImgByRect(img, rect):
    # rect: [left_top.u, left_top.v, width, high]
    newImg = img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]
    return newImg


def tansISFormat2BGR(img):
    img = np.transpose(img, (1,2,0))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def tansBGR2ISFormat(img, rect, wholeImg, rsize = [112, 112]):
    # rect: [left_top.u, left_top.v, width, high]
    img = getSquareByRect(img, rect, wholeImg)
    img = cv2.resize(img, (rsize[0], rsize[1]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2,0,1))
    return img

if __name__ == "__main__":
    # ori = np.ones([100, 200, 3], dtype='uint8')
    # wholeImg = cv2.imread('../data/testS/100200.png')
    # rect = [19, 9, 100, 50]
    # rect = [19, 49, 100, 50]
    # rect = [19, 49, 170, 50]
    wholeImg = cv2.imread('../data/testS/200100.png')
    # rect = [9, 19, 50, 100]
    # rect = [49, 19, 50, 100]
    rect = [49, 19, 50, 170]
    img = wholeImg[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]
    # newImg = getSquareByRect(img, rect, wholeImg)
    newImg = tansBGR2ISFormat(img, rect, wholeImg)
    newImg = tansISFormat2BGR(newImg)
    cv2.imshow('wholeImg', wholeImg)
    cv2.imshow('img', img)
    cv2.imshow('newImg', newImg)
    cv2.waitKey(0)