#!/usr/bin/python

import scipy as sp
import cv2

import goPro

goPro.password = "syphilis"

# Creates an OpenCV windows displaying the current stream.
# This is for test purpose because it will keep hold of the command line.

# Create camera object. "-1" will open any camera connected
cam = cv2.VideoCapture("http://10.5.5.9:8080/live/amba.m3u8")

# Create display window
cv2.namedWindow("",cv2.CV_WINDOW_AUTOSIZE)

# Load Haar face recog
#haar = cv2.CascadeClassifier()
#haar.load("/usr/share/opencv/haarcascade_frontalface_default.xml")
#haar.load("/usr/share/opencv/haarcascade_fullbody.xml")

#if not haar.empty(): print("Classifier loaded!")

# Loop
print("Press 'Ctrl+C' to quit.")
while True:
    # Get image
    # "ret" is True if an image is returned.
    ret, image = cam.read()

    # Cascade classifier
    #ped = haar.detectMultiScale(image,minSize=(30,30),maxSize=(80,80))

    # Check wether any face was detected
    #if ped != ():
    #    #goPro.beep()
    #    # Draw every pedestrian
    #    for person in ped:
    #      # Draw rectangle
    #      cv2.rectangle(image,(person[0],person[1]),(person[0]+person[2],person[1]+person[3]),255)


    # Display image
    cv2.imshow("",image)

    # Execute events
    cv2.waitKey(1)
