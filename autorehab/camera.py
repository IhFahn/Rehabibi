import cv2, os, urllib.request
import time
import mediapipe as mp
import numpy as np 
import winsound
import PoseModule as pm
from django.shortcuts import render


class IPWebCam(object):
    def __init__(self, exerciseType, duration, reps):
        self.video = cv2.VideoCapture(0)
        self.exerciseType = exerciseType
        self.duration = duration
        self.reps = reps
        self.pTime = 0
        self.detector = pm.poseDetector()
        self.legLength = []
        self.start_time = 0
        self.nSecond = 0
        self.elapsed_time = 0
        self.counter = 0


    def get_frame(self):


        while True:
            self.success, self.img = self.video.read()
            self.img = self.detector.findPose(self.img, False)
            self.lmList = self.detector.findPosition(self.img, draw=False)

            if len(self.lmList) != 0:
        # ------------------(p1, MIDPOINT, p2)

                self.p1, self.p2, self.p3, self.range = self.detector.pointsnRange(self.exerciseType, "R")
                self.angle = self.detector.findAngle(self.img, self.p1, self.p2, self.p3)
                self.percentage = np.interp(self.angle, self.range, (0, 100))
                cv2.putText(
                    self.img,
                    str(int(self.percentage)) + "%",
                    (self.lmList[24][1] + 60, self.lmList[24][2] + 90),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (255, 0, 255),
                    2,
                )

                if self.percentage == 100:
                    if self.start_time == 0:
                        self.start_time = time.time()

                    self.elapsed_time = time.time() - self.start_time
                    print(self.elapsed_time)

                else:
                    self.elapsed_time = 0
                    self.start_time = 0

                if int(self.elapsed_time) == self.duration:
                    print("yes yes yes")
                    winsound.Beep(440, 500)
                    self.counter += 0.5
                    # self.start_time = 0
                    # self.elapsed_time = 0
                    continue
            frame_flip = cv2.flip(self.img, 1)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
            return jpeg.tobytes()

    def __del__(self):
        self.video.release()

    def timeGetter(self):
        return self.elapsed_time
    
    def repsGetter(self):
        return self.reps

    

    





