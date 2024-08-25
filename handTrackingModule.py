import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, 
                                        max_num_hands=self.maxHands, 
                                        min_detection_confidence=self.detectionCon, 
                                        min_tracking_confidence=self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils



    def findHands(self, frame, draw=True):
        imRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
    

    def findposition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append({'id': id, 'cx': cx, 'cy': cy})
                if draw:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
        return lmList
    

    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType
  
    def FingerPositions(self, frame):
        tipIds = [4, 8, 12, 16, 20]
        lmList = self.findposition(frame, draw=False)
        handData, handsType =  self.Marks(frame)
        fingers = []
        
        if len(lmList) != 0:
            for hand,handType in zip(handData,handsType):
                if handType=='Right':
                    if lmList[tipIds[0]]['cx'] < lmList[tipIds[0] - 2]['cx']:
                        fingers.append(1)
                    else:
                            fingers.append(0)
                if handType=='Left':
                    if lmList[tipIds[0]]['cx'] > lmList[tipIds[0] - 2]['cx']:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            for id in range(1,5) :
                if lmList[tipIds[id]]['cy'] < lmList[tipIds[id] - 3]['cy']:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers


width=1280
height=720 