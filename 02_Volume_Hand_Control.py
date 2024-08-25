import cv2
import numpy as np
import time
import handTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###################### Cam Size Setup #########################
wCam, hCam = 640, 480
#################### Volume Change Code #######################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange =  volume.GetVolumeRange()

minVolume = volRange[0]
maxVolume = volRange[1]
volVB = 400
volPercnt = 0

##############################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

Detector = htm.HandDetector(detectionCon= 0.7)

while True:
    success, img = cap.read()
    img = Detector.findHands(img)
    lmList = Detector.findposition(img, draw = False)

    if len(lmList) != 0:
        # thumb position
        x1, y1 = lmList[4]['cx'], lmList[4]['cy']
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)

        # 1st Finger position
        x2, y2 = lmList[8]['cx'], lmList[8]['cy']
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)

        # 2nd Finger position
        x3, y3 = lmList[12]['cx'], lmList[12]['cy']
        cv2.circle(img, (x3, y3), 8, (255, 0, 255), cv2.FILLED)        

        # Draw line between thumb and finger
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate finger to finger length
        lenghtFF= math.hypot(x3 - x2, y3 - y2)

        if lenghtFF > 40:
            # Change color or line
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)

            # Calculate distance between thumb and finger
            lenghtTF = math.hypot(x2 - x1, y2 - y1)
            # Set volume based on finger length
            vol = np.interp(lenghtTF, (40, 200), [minVolume, maxVolume])
            # Set volume bar length based on finger length
            volVB = np.interp(lenghtTF, (40, 200), [400, 80])
            # Set %age 
            volPercnt = np.interp(lenghtTF, (40, 200), [0, 100])
            # Set volume level
            volume.SetMasterVolumeLevel(vol, None)

    # Display volume bar with %age
    cv2.rectangle(img, (50, 80), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, (int(volVB))), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPercnt)} %', (30, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # FPS calculation and display code
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


