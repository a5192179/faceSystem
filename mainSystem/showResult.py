import cv2
import numpy as np
import math
import os

def resizeImgIntoFrame(img, H, W):
    imgH = img.shape[0]
    imgW = img.shape[1]
    rate = max(imgH/H, imgW/W)
    newH = int(imgH / rate)
    newW = int(imgW / rate)
    imgNew = cv2.resize(img, (newW, newH))
    return imgNew

def showResult(mainImg, mainImgInfo, others, othersInfos, infos, bShowResult, bSaveResult, savePath):
    border = 2
    mainW = 800
    mainH = 450
    infoW = mainW
    infoH = 140 + border
    otherW = 200 + border * 2
    otherH = mainH + infoH
    maxOtherNum = 4
    maxInfoNum = 8
    otherEachH = math.floor(otherH/maxOtherNum)
    infoEachH = math.floor(infoH/maxInfoNum)
    background = np.zeros([mainH + infoH, mainW + otherW, 3], dtype='uint8')

    mainImgShow = resizeImgIntoFrame(mainImg, mainH, mainW)
    hup = 0
    hDown = mainImgShow.shape[0]
    wLeft = 0
    wRight = mainImgShow.shape[1]
    background[hup:hDown, wLeft:wRight, :] = mainImgShow
    cv2.putText(background, mainImgInfo, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

    for i in range(min(maxOtherNum, len(others))):
        otherImgShow = resizeImgIntoFrame(others[i], otherEachH - 20 - 2*border, otherW - border) #上下留5，字30
        hup = i * otherEachH
        hDown = hup + otherImgShow.shape[0]
        wLeft = mainW + 2 * border
        wRight = wLeft + otherImgShow.shape[1]
        background[hup:hDown, wLeft:wRight, :] = np.copy(otherImgShow)
        imgStr = othersInfos[i]
        cv2.putText(background, imgStr, (wLeft, hDown + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

    begin = max(0, len(infos) - maxInfoNum)
    for i in range(begin, len(infos)):
        # print(i)
        imgStr = infos[i]
        cv2.putText(background, imgStr, (border, 15 + mainH + infoEachH * (i - begin)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    # ===========================================
    if bSaveResult:
        imgName = mainImgInfo + '.jpg'
        cv2.imwrite(savePath + '/' + imgName, background)
    # ===========================================
    if bShowResult:
        cv2.imshow('img', background)
        cv2.waitKey(41)


if __name__ == "__main__":
    img = cv2.imread('../data/show/1.jpg')
    mainImgInfo = 'frame id: 1'
    others = []
    othersInfos = []
    for i in range(5):
        others.append(img[0:100, 0:100, :])
        othersInfos.append('1234567890abc')
    infos = []
    for i in range(12):
        infos.append('1234567890abc-' + str(i))
    showResult(img, mainImgInfo, others, othersInfos, infos)