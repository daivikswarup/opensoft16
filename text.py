#!/usr/bin/env python
import numpy as np 
import cv2

# Pass images having relative size of text blooks comparable to image size
# better corp them and pass part of it   

def detect_text(file_name):
    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
    _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    height = np.size(image, 0)
    width = np.size(image, 1)
    
    index =1
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        # discard areas that are too large
        if h>0.9*height and w>0.9*width:
           continue
        
        # discard areas that are too small
        if h<height*0.02 or w<width*0.02:
            continue
        
        # draw rectangle around contour on original image
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

        cropped = image[y :y +  h , x : x + w]

        s =  'images/crop_' + str(index) + '.jpg' 
        cv2.imwrite(s , cropped)
        index = index + 1

    # write original image with added contours to disk  
    cv2.imwrite("images/contoured.jpg", image) 

file_name ='images/c.jpg'
detect_text(file_name)
