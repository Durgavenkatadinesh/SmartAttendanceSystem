import os
import cv2
import face_recognition
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://smartattendance-2e574-default-rtdb.firebaseio.com/",
    'storageBucket':'smartattendance-2e574.appspot.com'
})


# Importing student images
folderPath = 'Images'
imagesPathList = os.listdir(folderPath)
imageList = []
studentIds = []

for path in imagesPathList:
    imageList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            encode = face_encodings[0]
            encodeList.append(encode)
        else:
            # Handle the case where no face is detected in the image
            print("No face found in the image.")
    return encodeList
print('Encoding started...')
encodeListKnown = findEncodings(imageList)

encodeListKnownWithIds = [encodeListKnown,studentIds]
print(encodeListKnown)
print('Encoding complete')

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()