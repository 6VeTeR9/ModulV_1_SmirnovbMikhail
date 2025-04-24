import cv2 as cv 
import numpy as np 
import imutils

color = (255,255,255)
    # I have defined lower and upper boundaries for each color for my camera
    # Strongly recommended finding for your own camera.
colors = {'blue': [np.array([26, 119, 35]), np.array([179, 222, 255])],
          'red': [np.array([161, 165, 127]), np.array([178, 255, 255])],
          'yellow': [np.array([0, 190, 130]), np.array([255, 255, 255])], 
          'green': [np.array([26, 97, 69]), np.array([121, 212, 114])]}
def find_color(frame, points):
    mask = cv.inRange(frame, points[0], points[1])#create mask with boundaries 
    cnts = cv.findContours(mask, cv.RETR_TREE,
                        cv.CHAIN_APPROX_SIMPLE) # find contours from mask 
    cnts = imutils.grab_contours(cnts) 
    for c in cnts:
        area = cv.contourArea(c) # find how big countour is 
        if area > 5000:	# only if countour is big enough, then
            M = cv.moments(c)
            cx = int(M['m10'] / M['m00']) # calculate X position 
            cy = int(M['m01'] / M['m00']) # calculate Y position 
            return c, cx, cy
        
cap = cv.VideoCapture(0)
while cap.isOpened(): #main loop 
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #convertion to HSV 
    for name, clr in colors.items(): # for each color in colors 
        if find_color(hsv, clr): # call find_color function above 
            c, cx, cy = find_color(hsv, clr)
            cv.drawContours(frame, [c], -1, color, 3) #draw contours 
            cv.circle(frame, (cx, cy), 7, color, -1)	# draw circle
            cv.putText(frame, name, (cx,cy),
                    cv.FONT_HERSHEY_SIMPLEX, 1, color, 1) # put text 
    cv.imshow("Frame: ", frame) # show image 
    if cv.waitKey(1) == ord('q'): 
        break
cap.release() #idk what it is
cv.destroyAllWindows() # close all windows opened by opencv