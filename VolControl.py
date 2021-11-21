"""
Code Author : Akarshan Mishra
"""

import pyautogui
import cv2
import mediapipe as mp
import time
import math


videoCapture = cv2.VideoCapture(0)

mpHands = mp.solutions.hands #Calling hand detection class
hands = mpHands.Hands(max_num_hands=1) #We can change parameters here
#But No need to change parameters

mpDraw = mp.solutions.drawing_utils #this is to draw lines between landmarks

'''
The code below is for the fps counter
The fps counter uses the time library of python
'''

previousTime = 0
currenTime = 0
x1,x2,y1,y2 = 0,0,0,0
voldistance = 0

while True:
  sucess,img = videoCapture.read()
  img = cv2.flip(img, 1) #This is to flip video as input is always mirror of actual footage
  RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting to rgb because hands object needs RGB image

  results = hands.process(RGBimg) #calling method process to process the frame and give results

  # print(results.multi_hand_landmarks) #getting hands co-ordinates here

  if results.multi_hand_landmarks: #if we have hand_coordinates
    for eachpoint in results.multi_hand_landmarks:
      mpDraw.draw_landmarks(img, eachpoint, mpHands.HAND_CONNECTIONS)
      '''
      from img till eachpoint we are drawing points
      mpHands.HAND_CONNECTIONS draws connection lines
      '''
      for id, landmark in enumerate(eachpoint.landmark):
        #print(id, landmark) #id are points from Hand Landmark Model
        # the landmarks are the ratio of the image, landmarks are in ratio
        height, width, channl = img.shape
        cx, cy = int(landmark.x*width), int(landmark.y*height)
        # print(id, cx, cy) #getting the pixel co-ordinates for each
        # Hand Landmark Model

        """
        The code block should detect landmarks and represent them with a
        circle
        """
        if id == 4:
          x1, y1 = 0, 0
          cv2.circle(img, (cx, cy), 20, (255,0,100), cv2.FILLED)
          x1, y1 = cx, cy
        if id == 8:
          x2, y2 = 0, 0
          cv2.circle(img, (cx, cy), 20, (100, 0, 255), cv2.FILLED)
          x2, y2 = cx, cy
      distance = round(math.sqrt((x2-x1)**2+(y2-y1)**2)*0.3)
    print(distance)
    if distance < 35:
      pyautogui.press('volumedown')
    elif distance > 35:
      pyautogui.press('volumeup')

  '''
  fps counter is below
  '''
  currenTime = time.time()
  framerate = 1/(currenTime-previousTime)
  previousTime = currenTime
  cv2.putText(img, str('FPS:'+ str(framerate)), (10,70), cv2.FONT_ITALIC, 2,(255,0,255),2)
  ########img, FPS VAL, Position, FONT, SIZE, COLOR, THICKNESS#####

  # cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
  # cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  # #####FULL_SCREEN_ABOVE######
  cv2.imshow("Image", img)
  cv2.waitKey(1)

'''
The code above runs the webcam
'''



