__author__ = 'Justin'

import cv2
from cv2 import *
import os

#Capture 3 short videos and give them an incremental name

cam = cv2.VideoCapture(0)

s, img = cam.read()
imwrite(str(0)+".jpg",img)
imgsize = cv2.imread('0.jpg')
os.remove('0.jpg')

height,width,layers = imgsize.shape
fourcc = cv2.cv.CV_FOURCC(*'I420')

i = 1
j = 1
while j is not 4:
    video = cv2.VideoWriter('video{}.avi'.format(j),fourcc,15,(width,height))
    while i is not 81:
        s, img = cam.read()
        if s:    # frame captured without any errors
            imwrite(str(i)+".jpg",img) #save image
            img = cv2.imread(str(i)+".jpg")
            video.write(img)
            os.remove(str(i)+".jpg")
            i = i+1
    i=1
    j = j+1

cv2.destroyAllWindows()
video.release()