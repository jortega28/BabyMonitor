__author__ = 'Justin'
#Initialize a camera and capture a few images
#This is an equipment test

from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    i = 0
    while i is not 3:
        imwrite(i + ".jpg",img) #save image
