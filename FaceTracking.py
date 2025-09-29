# This code enables a Tello drone to track and follow a human face using computer vision techniques.
# using OpenCV for face detection and a PID controller for smooth movement adjustments, the drone can maintain an optimal distance and alignment with the detected face.
import cv2
# numpy is used for numerical operations, particularly for handling arrays and mathematical calculations.
import numpy as np
# djitellopy is a Python library that provides an interface to control Tello drones.
# this library simplifies the process of sending commands to the drone and receiving data from it. written by: Arvind Sanjeev
from djitellopy import tello

import time
# Initialize the Tello drone
me = tello.Tello()
# Connect to the drone
me.connect()
# Print the battery level of the drone
print(me.get_battery())
# Start the video stream from the drone's camera
me.streamon()
# Take off the drone
me.takeoff()
# Allow some time for the drone to stabilize after takeoff
me.send_rc_control(0, 0, 25, 0)
# Give the drone some time to reach a stable hover position
time.sleep(2.2)
# Set the width and height for the video frame
w, h = 360, 240

# Forward Backward range defined by area of the face
# The drone will try to maintain the face area within this range to keep an optimal distance from the face.
# If the area is less than 6200, the drone will move forward. If the area is greater than 6800, the drone will move backward.
# if the area is more than 6200 and less than 6800, the drone will stay in place.
# The area is calculated based on the width and height of the detected face in the video frame.
# This range may need to be adjusted based on the specific environment and the size of the face being tracked.
# 6200 to 6,800 is a good starting point for most scenarios.
# for reference, an average adult face occupies an area of approximately 8,000 to 10,000 pixels in a 640x480 image when the person is about 1 meter away from the camera.
# Adjusting the range to 6200-6800 helps to ensure that the drone maintains a comfortable distance from the face, allowing for better tracking and reducing the risk of collision.
# 6200 is to close, 6800 is too far
fbRange = [6200, 6800]

# Proportional, Integral, Derivative values are based on tuning tests. These values may need to be adjusted for different environments or drones.
pid = [0.4, 0.4, 0]
# Previous error initialized to zero
pError = 0

# Function to find the face in the image from the drone's camera
def findFace(img):

    # Load the pre-trained Haar Cascade classifier for face detection.
    # This XML file contains the data needed to detect faces in images.
    # for more information on haarcascades, visit: https://github.com/opencv/opencv/tree/master/data/haarcascades
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    # Convert the image to grayscale for the face detection algorithm
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale image
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    # Initialize lists to store the center coordinates and areas of detected faces
    myFaceListC = []
    # Initialize a list to store the areas of detected faces
    myFaceListArea = []


    # Draw a rectangle in the center of the image to represent the desired position of the face
    for (x, y, w, h) in faces:
        # Draw a rectangle around each detected face
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Calculate the center coordinates of the face
        cx = x + w // 2
        # Calculate the center y-coordinate of the face
        cy = y + h // 2
        # Calculate the area of the face
        area = w * h
        # Draw a circle at the center of the face
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        # Append the center coordinates of the face to the list
        myFaceListC.append([cx, cy])
        # Append the area of the face to the list
        myFaceListArea.append(area)

    # check if any faces were detected
    if len(myFaceListArea) != 0:
        # if there are faces detected, find the index of the face with the largest area
        i = myFaceListArea.index(max(myFaceListArea))
        # Draw a rectangle in the center of the image to represent the desired position of the face
        return img, [myFaceListC[i], myFaceListArea[i]]

    else:
        # if no faces were detected, return the original image and a default value
        return img, [[0, 0], 0]

# Function to track the face and adjust the drone's position
def trackFace( info, w, pid, pError):

    # info[0] = [x, y], info[1] = area

    # Extract the area of the detected face
    area = info[1]
    # Extract the x and y coordinates of the center of the detected face
    x, y = info[0]
    # Initialize forward/backward movement variable
    fb = 0
    # Calculate the error between the center of the image and the center of the detected face
    error = x - w // 2 # Center of the image from the center of the face and the red frame

    # Proportional control is pid[0] * error
    # Derivative control is pid[1] * (error - pError)
    speed = pid[0] * error + pid[1] * (error - pError)

    # Limit the speed to be between -100 and 100
    speed = int(np.clip(speed, -100, 100))

    # Forward/Backward control based on the area of the detected face
    # If the area is within the defined range, no forward/backward movement is needed
    if area > fbRange[0] and area < fbRange[1]: # Green zone area
        # forward/backward movement is zero if the area is within the range (green zone)
        fb = 0
    # If the area is greater than the upper limit of the range, the drone is too close to the face and needs to move backward
    elif area > fbRange[1]: # Too close area
        # move backward
        fb = -20
    # If the area is less than the lower limit of the range and not zero, the drone is too far from the face and needs to move forward
    elif area < fbRange[0] and area != 0: # Too far area and not zero
        # move forward
        fb = 20
    #if no face is detected, stop all movement
    if x == 0: # No face detected
        # stop all movement
        speed = 0
        # forward/backward movement is zero
        error = 0

    #print(speed, fb)

    # Send the calculated speed and forward/backward movement commands to the drone
    me.send_rc_control(0, fb, 0, speed)

    # Return the current error for use in the next iteration
    return error

#cap = cv2.VideoCapture(1)

# while loop to continuously get frames from the drone's camera and process them
while True:

    #_, img = cap.read()

    # Read a frame from the drone's camera
    img = me.get_frame_read().frame
    #  Resize the frame to the defined width and height
    img = cv2.resize(img, (w, h))
    # Find the face in the frame
    img, info = findFace(img)

    # Track the face and adjust the drone's position
    pError = trackFace( info, w, pid, pError)
    # pid = [Proportional, Integral, Derivative]
    # info = [[x, y], area]
    # pError = previous error

    #print("Center", info[0], "Area", info[1])

    # Display the processed frame
    cv2.imshow("Output", img)

    # Break the loop and land the drone if the 'q' key is pressed
    if cv2.waitkey(1) & 0xFF == ord('q'):
        # Land the drone
        me.land()
        # break the loop
        break