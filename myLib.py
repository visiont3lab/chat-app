
import cv2 
import numpy as np

# !git clone https://github.com/anaustinbeing/haar-cascade-files.git

class algorithm:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haar-cascade-files/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haar-cascade-files/haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier('haar-cascade-files/haarcascade_smile1.xml')  

    def run(self,im):
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2) # RGB--> BGR
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = im[y:y+h, x:x+w]

            eyes = self.eye_cascade.detectMultiScale(roi_gray,1.1,5)
            for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),3)
                cv2.rectangle(im,(x+ex,y+ey),(x+ex+ew,y+ey+eh),(0,255,0),3)

            smile = self.smile_cascade.detectMultiScale(roi_gray,1.3,5)
            for (sx,sy,sw,sh) in smile:
                cv2.rectangle(im,(x+sx,y+sy),(x+sx+sw,y+sy+sh),(125,125,0),3)
        return im



