#!/usr/bin/python

#####################################################
#### NOTE: THIS SOFTWARE IS IN THE PUBLIC DOMAIN ####
#####################################################
"""
Additional notes:
This software is in now way affiliated with the company Woodman Labs inc. (which manufactures these really nice tiny cameras)
This software was designed for the Hero3 Black edition camera, on Python 2.7.

THIS SOFTWARE MAY BREAK YOUR CAMERA, SD CARD, AND/OR BATTERY.
USE IT AT YOUR OWN RISK!
I doubt it will break your computer, but there's no guarantee!

If you like this software, please share and/or upgrade it!
"""

from urllib2 import urlopen
#import scipy as sp
#import cv2
from time import sleep

# Global variable. I know... I'm a bad programmer.
# After importing this module, you should do: goPro.password = "your real password"
password = "goprohero"

def initInteractive():
    # Interactive (test) mode. Comment out when importing inside a program.
    #If you're in python 3, change 'raw_input' by 'input'.
    password = raw_input("Enter your camera's wifi password (press Enter for default password)\n")
    if password == "": password = "goprohero"

def send(group,action):
    # Every command is pretty much the same...
    try:
        urlopen("http://10.5.5.9/camera/"+group+"?t="+password+"&p=%"+action, timeout=0.01)
    except:
        pass

# Test connection

def beep():
    # This makes the camera sound a single beep loudly, for testing or other purpose.
    send("LL","01")
    sleep(1)
    send("LL","00")

# Power

def powerOn():
    # Turns on the camera (doesn't work on mine)
    #send("PW","01")
    try:
        urlopen("http://10.5.5.9/bacpac/PW?t="+password+"&p=%01", timeout=1)
    except:
        pass

def powerOff():
    send("PW","00")

def changeMode():
    # I think this one is under this caterogy because it's linked to the physical power button.
    send("PW","02")


# Capture
# I don't know what SH stands for... The other ones are pretty obvious!

def startCapture():
    send("SH","01")

def stopCapture():
    send("SH","00")


# Preview

def previewOn():
    send("PV","02")

def previewOff():
    send("PV","00")

# Camera Mode

def modeVideo():
    send("CM","00")

def modePhoto():
    send("CM","01")

def modeBurst():
    send("CM","02")

def modeTimelapse():
    send("CM","03")


# Orientation

def orientationUp():
    send("UP","00")

def orientationDown():
    send("UP","01")


# Video Resolution

def videoResolution4k():
    send("VR","02")

"""I did not include other commands becuase they don't consistently work.
Here is what I found with trian and error:
Letters:VR
00:error
01:error
02:4k cin12
03:2.7k cin24
04:error
05:no error, displays [x]. Seems to be a modifier key.
06:error
07:960p48
08:Camera freezes. Sometimes, it displays [x] and freezes.
09:error

05 then 02:2.7k cin24
05 then 06:720p60
05 then 06 then 05:1080p30 Worked once!
"""

# Protune
"""
Considering video resolutions are somewhat limited, I recommend manually setting
your two favorite video modes on the camera, one on protune.
"""

def proTuneOn():
    send("PT","01")

def proTuneOff():
    send("PT","00")


# FOV

def fovWide():
    send("FV","00")

def fovMedium():
    send("FV","01")

def fovNarrow():
    send("FV","02")


# Photo resolution

def photoRes12Wide():
    # Highest photo res of all
    send("PR","05")

def photoRes8Medium():
    # Highest photo res at Medium FOV (in the list of commands I could find.)
    send("PR","01")

"""Other useless photo resolutions
Why would I want a lower resolution if it's not to avoid fisheye FOV?

11mp wide : http://<ip>/camera/PR?t=<password>&p=%00
5mp wide : http://<ip>/camera/PR?t=<password>&p=%02
5mp medium : http://<ip>/camera/PR?t=<password>&p=%03
07mp w : http://<ip>/camera/PR?t=<password>&p=%04
07mp m : http://<ip>/camera/PR?t=<password>&p=%06
"""


# Timelapse Timer

def timelapse60sec():
    send("TI","06")

"""I don't really care about the other ones.

0,5sec : http://<ip>/camera/TI?t=<password>&p=%00
1sec : http://<ip>/camera/TI?t=<password>&p=%01
2sec : http://<ip>/camera/TI?t=<password>&p=%02
5sec : http://<ip>/camera/TI?t=<password>&p=%03
10sec : http://<ip>/camera/TI?t=<password>&p=%04
30sec : http://<ip>/camera/TI?t=<password>&p=%05
"""

# Other functions

def locateOn():
    # This makes the camera sound a beep loudly, to help find it.
    send("LL","01")

def locateOff():
    send("LL","00")

def beepMute():
    # Mutes the camera beep
    send("BS","00")
    
def beepLow():
    # Volume at 70%. Seems a lot, but it must not be in decibels, which is a log scale.
    send("BS","01")

def beepHigh():
    # Volume at 100%
    send("BS","02")


### OpenCV section ###

def grabImage():
    # Returns a numpy array containing a live picture
    
    # Initiate video capture object
    cam = cv2.VideoCapture("http://10.5.5.9:8080/live/amba.m3u8")
    
    # Grab the image
    ret, im = cam.read()
    
    # Return the image (or None, if capture was unsuccessful)
    return im

def testStream():
    # Creates an OpenCV windows displaying the current stream.
    # This is for test purpose because it will keep hold of the command line.
    
    # Create camera object. "-1" will open any camera connected
    cam = cv2.VideoCapture("http://10.5.5.9:8080/live/amba.m3u8")

    # Create display window
    cv2.namedWindow("",cv2.CV_WINDOW_AUTOSIZE)

    # Load Haar face recog
    haar = cv2.CascadeClassifier()
    haar.load("/usr/share/opencv/haarcascade_frontalface_alt.xml")

    if not haar.empty(): print("Classifier loaded!")

    # Loop
    print("Press 'Ctrl+C' to quit.")
    while True:
      # Get image
      # "ret" is True if an image is returned.
      ret, image = cam.read()
      
      # Cascade classifier
      faces = haar.detectMultiScale(image,minSize=(150,150))
      
      # Check wether any face was detected
      if faces != ():
        # Draw every faces
        for face in faces:
          # Draw rectangle
          cv2.rectangle(image,(face[0],face[1]),(face[0]+face[2],face[1]+face[3]),255)

      # Display image
      cv2.imshow("",image)

      # Execute events
      cv2.waitKey(1)

###################

# Ask for password if in interactive mode
#if __IPYTHON__:
#    initInteractive()

