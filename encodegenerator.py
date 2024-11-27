import cv2 
import face_recognition
import pickle
import os

folderPath = "Images"
PathList = os.listdir(folderPath)
imgList = []
studentIDS=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIDS.append(os.path.splitext(path)[0])



def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # change the color space of the image i.e from BGR(open cv uses) to RGB(face_recognition uses)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # find the face locations in the image
        encode= face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(imgList)

# save the encodings in a file , so that we can use it later
# images along with their encodings are saved in a list

encodeListKnownWithID = [encodeListKnown,studentIDS]
file= open("Encodefile.p","wb")
pickle.dump(encodeListKnownWithID,file)
file.close()
