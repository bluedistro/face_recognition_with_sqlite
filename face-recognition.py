import numpy as np
import os
import sqlite3
import cv2

def insertOrUpdate(id, name):
    #connecting to the db
    conn =sqlite3.connect("FaceBase")

    #check if id already exists
    query = "SELECT * FROM People WHERE ID="+str(id)
    #returning the data in rows
    cursor = conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        query="UPDATE People SET Name="+str(name)+" WHERE ID="+str(id)
    else:
        query="INSERT INTO People(ID, Name) VALUES("+str(id)+","+str(name)+")"
    conn.execute(query)
    conn.commit()
    conn.close()


face_cascade = cv2.CascadeClassifier('Classifiers/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('Classifiers/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
id = input('Enter user id: ')
name = input('Enter name: ')
insertOrUpdate(id, name)
sample_number = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        sample_number += 1

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        cv2.imwrite('dataSet/User.'+str(id)+"."+str(sample_number)+".jpg",  gray[y:y+h,x:x+w])
        cv2.rectangle(img, (x-50,y-50), (x+w+50, y+h+50), (0,255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex-50, ey-50), (ex+ew+50, ey+eh+50), (0, 0, 255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(1);
    if(sample_number>30):
        cap.release()
        cv2.destroyAllWindows()
        break;

