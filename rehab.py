import cv2
import time
import mediapipe
import PoseModule as pm
from datetime import datetime
import numpy as np
import winsound
import argparse

parser = argparse.ArgumentParser(description="set up settings")
parser.add_argument(
    "--orientation", default="R", type=str, help="R for Right leg, L for Left leg"
)
parser.add_argument(
    "--exercise",
    type=int,
    help="1. Front Straight Leg Raise  2. Inner Quadriceps Range  3. Side Straight Leg Raise  4. Pronated Hip Extension",
)
parser.add_argument("--duration", type=int)

args = parser.parse_args()

cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDetector()
legLength = []
start_time = 0
duration = args.duration
nSecond = 0
elapsed_time = 0
counter = 0


while True:
    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # ------------------(p1, MIDPOINT, p2)

        p1, p2, p3, range = detector.pointsnRange(args.exercise, args.orientation)
        angle = detector.findAngle(img, p1, p2, p3)
        per = np.interp(angle, range, (0, 100))
        cv2.putText(
            img,
            str(int(per)) + "%",
            (lmList[24][1] + 60, lmList[24][2] + 90),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 0, 255),
            2,
        )

        if per == 100:
            if start_time == 0:
                start_time = time.time()

            elapsed_time = time.time() - start_time
            print(elapsed_time)

        else:
            elapsed_time = 0
            start_time = 0

        if int(elapsed_time) == duration:
            print("yes yes yes")
            winsound.Beep(440, 500)
            counter += 0.5
            # start_time = 0
            # elapsed_time = 0
            continue

    # try:
    #     print(lmList[28])
    #     if not legLength:
    #         legLength = lmList[28][1] - lmList[24][1]
    #         raiseHeight = legLength/3
    #         requiredHeight = lmList[24][2] - raiseHeight

    #     if lmList[28][2] < requiredHeight and legLength:#stopped at this part, tricky

    #         if start_time == 0:
    #             start_time = time.time()

    #         elapsed_time = time.time() - start_time
    #         print(elapsed_time)

    #     else:
    #         elapsed_time = 0
    #         start_time = 0

    #     #cv2.circle(img, (lmList[28][1],lmList[28][2]), 15, (255,0,0), cv2.FILLED)
    # except:
    #     pass

    cv2.putText(
        img,
        str(int(elapsed_time)) + "sec",
        (50, 70),
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (0, 0, 255),
        3,
    )
    cv2.putText(
        img,
        str(int(counter)) + "rep",
        (500, 70),
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (0, 0, 255),
        3,
    )

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # if 0xFF == ord('q'):
    #     break
