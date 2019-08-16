import numpy as np
import cv2
bodyfind = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cap = cv2.VideoCapture(1)
retf, framef = cap.read()
gray = cv2.cvtColor(framef, cv2.COLOR_BGR2GRAY)
body = bodyfind.detectMultiScale(gray, 1.3, 5)
cv2.imshow('body',body)
for (x,y,w,h) in body:
    cutbody = framef[y:y+h,x:x+w]
    cv2.imshow('res',cutbody)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release
