#https://www.computervision.zone/topic/finding-the-face/

#Finding the Face

#Once we get the frames form the drone, then its time to find the faces in our image.
# We will create a function for this in the utilities file.
# We will be using the viola jones method to find the faces, so we have first get the haarcascade xml file.
# This will be added in the main directory. Now we can load this file and detect the faces.

def findFace(img):
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

#Now that we have the faces we will find their coordinates and display it on the image.
for (x, y, w, h) in faces:
cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

#Once we have all the faces we will target one of them and use its coordinates to operate the drone.
# We will first create empty lists in which we will add the Center points of the detected faces and their areas.
myFacesListC = []
myFaceListArea = []

#Then we will find the center point and the area of each face and add this to our list
for (x, y, w, h) in faces:
cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
cx = x + w//2
cy = y + h//2
area = w*h
myFacesListC.append([cx,cy])
myFaceListArea.append(area)

#Once we have all the faces we will find the closest one and return its coordinates. If no faces are found we will return 0.
if len(myFaceListArea) != 0:
i = myFaceListArea.index(max(myFaceListArea))
# index of closest face
return img,[myFacesListC[i],myFaceListArea[i]]
else:
return img, [[0,0],0]

#Lastly we will call this function in the main script
## STEP 2
img, c = findFace(img)