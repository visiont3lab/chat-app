
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


    def find_face_profile(self,im):
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        roi_color=gray
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = im[y:y+h, x:x+w]
            
            ret,thresh = cv2.threshold(roi_gray,40,255,cv2.THRESH_BINARY)
            thresh = cv2.medianBlur(thresh,15)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            hull = cv2.convexHull(cnt)

            cv2.drawContours(roi_color, hull, -1, (0,255,0), 3)
        return roi_color

    def run_blur(self,im):
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        res = gray
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2) # RGB--> BGR
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = im[y:y+h, x:x+w]
            res = cv2.medianBlur(roi_color, 15)
        return res

