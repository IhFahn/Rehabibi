import cv2
import mediapipe as mp
import time
from datetime import datetime
import math


class poseDetector:
    def __init__(self):
        # self.mode = mode
        # self.upBody = upBody
        # self.smooth = smooth
        # self.detectionCon = detectionCon
        # self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=False,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate Angle
        angle = math.degrees(
            math.atan2(y1 - y2, x1 - x2) - math.atan2(y3 - y2, x3 - x2)
        )

        if angle < 0:
            angle = abs(angle)

        if angle > 270:
            angle = abs(angle - 360)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (188, 0, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (188, 0, 255), 3)

            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(
                img,
                str(int(angle)) + "deg",
                (x2 + 20, y2 + 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (255, 0, 255),
                2,
            )

        return angle

    def pointsnRange(self, exer, orient):
        if orient == "R":
            if exer == 1:  # Front Straight Leg Raise
                po1 = 27
                po2 = 24
                po3 = 28
                ran = (0, 20)

            if exer == 2:  # Inner Quadriceps Range
                po1 = 24
                po2 = 26
                po3 = 28
                ran = (150, 165)

            if exer == 3:  # Side Straight Leg Raise
                po1 = 27
                po2 = 23
                po3 = 28
                ran = (0, 20)

            if exer == 4:  # Pronated Hip Extension
                po1 = 27
                po2 = 23
                po3 = 28
                ran = (0, 20)

        if orient == "L":
            if exer == 1:  # Front Straight Leg Raise
                po1 = 27
                po2 = 23
                po3 = 28
                ran = (0, 20)

            if exer == 2:  # Inner Quadriceps Range
                po1 = 23
                po2 = 25
                po3 = 27
                ran = (150, 165)

            if exer == 3:  # Side Straight Leg Raise
                po1 = 27
                po2 = 24
                po3 = 28
                ran = (0, 20)

            if exer == 4:  # Pronated Hip Extension
                po1 = 27
                po2 = 24
                po3 = 28
                ran = (0, 20)

        return po1, po2, po3, ran


# def main():
#     cap = cv2.VideoCapture('SLR.mp4')
#     pTime = 0
#     detector = poseDetector()

#     while True:
#         success, img = cap.read()
#         img = detector.findPose(img)
#         lmList = detector.findPosition(img, draw=False)
#         try:
#             print(lmList[28])
#             cv2.circle(img, (lmList[28][1],lmList[28][2]), 15, (255,0,0), cv2.FILLED)
#         except:
#             pass

#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime

#         cv2.putText(img, str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)

# if __name__ == "__main__":
#     main()
