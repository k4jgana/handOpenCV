import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam = 640,480
vol=0
volRect=0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
prevTime=0
volPerc=0
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = -50
maxVol = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])
        x1, y1=lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1],lmList[8][2]

        cx, cy =(x1+x2) // 2 , (y1+y2) // 2

        cv2.circle(img,(x1,y1),15,(0,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img, (cx, cy), 15, (0, 123, 255), cv2.FILLED)
        cv2.putText(img, f': {int(volPerc)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 255), 2)
        lenght = math.hypot(x2-x1,y2-y1)
        # print(lenght)

        vol = np.interp(lenght,[50,200],[minVol,maxVol])
        volRect = np.interp(lenght, [50, 200], [400, 150])
        volPerc = np.interp(lenght,[50,200],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        # print(vol)


        if lenght<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volRect)), (85, 400), (0, 255, 0), cv2.FILLED)

    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime=currTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cv2.imshow("Img",img)
    cv2.waitKey(1)