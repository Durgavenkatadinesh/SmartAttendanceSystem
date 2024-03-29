import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone

from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://smartattendance-2e574-default-rtdb.firebaseio.com/",
    'storageBucket':'smartattendance-2e574.appspot.com'
})


bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing of the mode images as a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imageModesList = []

for path in modePathList:
    imageModesList.append(cv2.imread(os.path.join(folderModePath,path)))

#print(len(imageModesList))


# Loading the encoding file

print('Loading Encoded File')
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

# separating encodeListKnown and studentIds
encodeListKnown,studentIds = encodeListKnownWithIds
# print(studentIds)
print('Encode file loaded successfully')

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[160:160 + 480, 48:48 + 640] = img
    imgBackground[40:40 + 622, 810:810 + 406] = imageModesList[modeType]


    # if faceCurrFrame:
    for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print('Matches',matches)
        print('FaceDis',faceDis)

        # Finding the index with min faceDis
        matchIndex = np.argmin(faceDis)
        # print('MatchIndex',matchIndex)
        if matches[matchIndex] and faceDis[matchIndex] < 0.5:
            # print(faceDis[matchIndex])
            # print('Known Face is Detected')
            print(studentIds[matchIndex])

            y1, x2, y2, x1 = faceLoc
            # we multiply it with 4 because we reduced the size by 4
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            bbox = 48 + x1, 160 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1
    if counter != 0:
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            # Getting image from the storage
            blob = bucket.get_blob(f'Images/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (858, 112), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1,
                    (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo['name']), (956, 424), cv2.FONT_HERSHEY_TRIPLEX, 1.1, (100, 100, 100),
                    1)
        cv2.putText(imgBackground, str(id), (1005, 485), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo['branch']), (1005, 539), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                    (255, 255, 255), 1)
        # cv2.putText(imgBackground, str(studentInfo['standing']), (910,615), cv2.FONT_HERSHEY_TRIPLEX, 0.6,(100,100,100),1)
        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 615), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                    (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 615), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                    (100, 100, 100), 1)

        imgBackground[167:167 + 216, 906:906 + 216] = imgStudent

        counter += 1



    #cv2.imshow('webcam', img)
    cv2.imshow("Face Attendence", imgBackground)
    cv2.waitKey(1)


