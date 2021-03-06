# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 00:17:06 2016

@author: anmol
"""

from __future__ import print_function
from imutils.object_detection import non_max_suppression
#from imutils import paths
import numpy as np
#import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments

#cap = cv2.VideoCapture(0)
"""
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""
"""
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path of image file")
args = vars(ap.parse_args())
""" 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
# loop over the image paths
while(True):
     #capture frame by frame
     ret,image = cap.read()
     image = imutils.resize(image, width=min(400, image.shape[1]))
     orig = image.copy()
 
	# detect people in the image
     (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
 
	# draw the original bounding boxes
     for (x, y, w, h) in rects:
		
       cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
       print (x,y)        
	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
     rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
     pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
     
	# draw the final bounding boxes
     for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
     
      
	# show some information on the number of bounding boxes
      #filename = imagePath[imagePath.rfind("/") + 1:]
     print("[INFO]  {} original boxes, {} after suppression".format(
		 len(rects), len(pick)))
     
	# show the output images
     cv2.imshow("Before NMS", orig)
     cv2.imshow("After NMS", image)
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()