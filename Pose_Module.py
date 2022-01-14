# coding: utf-8

# In[ ]:

import cv2
import mediapipe as mp
import time
import math


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print("the id and lm is : ",id, lm)
                cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                self.lmList.append([id, cx, cy, cz])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1, z1 = self.lmList[15][1:]
        x2, y2, z2 = self.lmList[13][1:]
        x3, y3, z3 = self.lmList[11][1:]
        x4, y4, z4 = self.lmList[16][1:]
        x5, y5, z5 = self.lmList[14][1:]
        x6, y6, z6 = self.lmList[12][1:]
        x7, y7, z7 = self.lmList[23][1:]
        x8, y8, z8 = self.lmList[24][1:]
        cx, cy = (x3 + x7) // 2, (y3 + y7 + 30) // 2
        cxx, cyy = (x6 + x8) // 2, (y6 + y8) // 2



        # Calculate the Angle and length
        if p1 == 16:
            # Right Arm
            difference = abs(z5 - z4)
            angle = math.degrees(math.atan2(y4 - y5, x4 - x5) -
                                 math.atan2(y6 - y5, x6 - x5))
            wx, wy = (cx + cxx + 200) // 2, (cy + cyy - 20) // 2
            length = math.hypot(x4 - wx, y4 - wy)
            print(length)
            length1 = math.hypot(x5 - cxx, y5 - cyy)
            print(length1)
            print(angle)
            # Draw pose landmarks on the image
            cv2.line(img, (x4, y4), (x5, y5), (255, 255, 255), 3)
            cv2.line(img, (x6, y6), (x5, y5), (255, 255, 255), 3)
            cv2.circle(img, (x4, y4), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x4, y4), 15, (0, 0, 255), 2)
            cv2.circle(img, (x5, y5), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x5, y5), 15, (0, 0, 255), 2)
            cv2.circle(img, (x6, y6), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x6, y6), 15, (0, 0, 255), 2)
            # cv2.circle(img, (cxx, cyy), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (cxx, cyy), 15, (0, 0, 255), 2)
            # cv2.circle(img, (wx, wy), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (wx, wy), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x5 - 50, y5 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        # cv2.putText(img, str(difference), (x2 - 350, y2 + 50),
        # cv2.FONT_HERSHEY_PLAIN, 2, (0, 211, 255), 2)

        else:
            # # Left Arm
            wx, wy = (cx + cxx - 200) // 2, (cy + cyy + 20) // 2
            difference = abs(z2 - z1)
            angle = math.degrees(math.atan2(y2 - y3, x2 - x3) -
                                 math.atan2(y2 - y1, x2 - x1))
            length = math.hypot(x1 - wx, y1 - wy)
            print(length)
            length1 = math.hypot(x2 - cx, y2 - cy)
            print(length1)
            print(angle)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (cx, cy), 15, (0, 0, 255), 2)
            # cv2.circle(img, (wx, wy), 10, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (wx, wy), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        # cv2.putText(img, str(difference), (x2 - 350, y2 + 50),
        # cv2.FONT_HERSHEY_PLAIN, 2, (0, 211, 255), 2)
        if angle >= 0:
            angle += 360
        return angle, difference, length, length1


# In[ ]:


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
