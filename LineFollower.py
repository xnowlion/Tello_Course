# This code enables a Tello drone to track and follow a human face using computer vision techniques.
# using OpenCV for face detection and a PID controller for smooth movement adjustments, the drone can maintain an optimal distance and alignment with the detected face.
import cv2
# numpy is used for numerical operations, particularly for handling arrays and mathematical calculations.
import numpy as np
# djitellopy is a Python library that provides an interface to control Tello drones.
# this library simplifies the process of sending commands to the drone and receiving data from it. written by: Arvind Sanjeev
from djitellopy import tello

# Initialize the Tello drone
me = tello.Tello()
# Connect to the drone
me.connect()
# Print the battery level of the drone
print(me.get_battery())
# Start the video stream from the drone's camera
me.streamon()
# Take off the drone
#me.takeoff()

# camera object for local webcam
# If you have multiple cameras connected to your computer, you can change the index (0, 1, 2, etc.) to select the desired camera.
# 0 is usually the default camera, 1 is the second camera, and so on.
# If you only have one camera, use 0.
# If you want to use an external webcam, make sure it is connected and recognized by your system, then use the appropriate index.
# If you want to use the Tello drone's camera, you don't need to use cv2.VideoCapture; instead, you can use the drone's video stream as shown in the code.
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1)

# HSV values for the color to be tracked
# HSV means Hue, Saturation, and Value, which are components of a color model used in image processing.
# >> You can use the OpenCV Color Picker to find the HSV values for the color you want to track. <<
# Adjust these values based on the color of the line you want the drone to follow.
# For a white line, you might use:
# hsvVals = [0, 0, 200, 179, 30, 255]
# The values are in the format: [H_min, S_min, V_min, H_max, S_max, V_max]
# You may need to experiment with these values to get the best results for your specific environment and lighting conditions.
# The current values are set to track a White line.
hsvVals = [0,0,188,179,33,245]

# Number of sensors (segments) to divide the image into for line detection
# More sensors can provide more detailed information about the line's position but may also increase computational load.
# Fewer sensors can simplify the processing but may reduce accuracy in detecting the line's position.
# 3 is a good starting point for basic line following tasks.
# the image will be divided into 3 vertical segments, allowing the drone to determine if the line is to the left, center, or right.
sensors = 3

# Threshold for determining if a sensor detects the line
# This value represents the minimum proportion of pixels in a sensor segment that must match the target color
# for the sensor to be considered as "detecting" the line.
# A lower threshold makes the sensor more sensitive, while a higher threshold makes it less sensitive.
# You may need to adjust this value based on the lighting conditions and the color of the line.
# A threshold of 0.2 means that if 20% or more of the pixels in a sensor segment match the target color, the sensor will be considered as detecting the line.
threshold = 0.2

# Set the width and height for the video frame
width, height = 480, 360

# Sensitivity for the drone's movement adjustments
# This value affects how aggressively the drone responds to the line's position.
# A lower sensitivity value makes the drone more responsive to small deviations from the line,
# while a higher sensitivity value makes it less responsive.
# You may need to experiment with this value to find the best balance between responsiveness and stability for your specific setup.
# A sensitivity of 3 is a good starting point for basic line following tasks.
senstivity = 3  # if number is high less sensitive

# Weights for the drone's turning adjustments based on sensor readings
# These weights determine how much the drone should turn based on which sensors detect the line.
# The weights are applied to the sensor readings to calculate the drone's turning rate.
# Negative weights indicate a turn to the left, while positive weights indicate a turn to the right.
# The weights are set to provide a balanced response to the line's position, allowing the drone to smoothly follow the line.
# You may need to adjust these weights based on the specific characteristics of your line and environment.
# The current weights are set to provide a moderate turning response when the line is detected by the left or right sensors, and no turning when the line is detected by the center sensor.
weights = [-25, -15, 0, 15, 25]

# Forward speed of the drone
# This value determines how fast the drone moves forward while following the line.
# You may need to adjust this value based on the speed of the line following task and the drone's capabilities.
# A forward speed of 15 is a good starting point for basic line following tasks.
# If the drone is moving too fast and overshooting the line, try reducing this value.
# If the drone is moving too slowly and not keeping up with the line, try increasing this value.
# Make sure to test the drone's performance at different speeds to find the optimal setting for your specific setup.
# Note: Always ensure that the drone has enough space to maneuver safely at the chosen speed.
# Note: The forward speed should be set in conjunction with the sensitivity and weights to achieve smooth and effective line following behavior.
# Note: The forward speed may also need to be adjusted based on the lighting conditions and the color of the line.
# Note: The forward speed should be tested in a safe environment to prevent accidents or damage to the drone.
# Note: The forward speed may also need to be adjusted based on the battery level of the drone, as lower battery levels may affect the drone's performance.
# Note: The forward speed should be set in conjunction with the drone's altitude to ensure stable flight while following the line.
# Note: The forward speed may also need to be adjusted based on the surface on which the line is drawn, as different surfaces may affect the drone's ability to follow the line.
# Note: The forward speed should be tested in different environments to ensure consistent performance.
# Note: The forward speed may also need to be adjusted based on the drone's payload, as carrying additional weight may affect the drone's speed and maneuverability.
# Note: The forward speed should be set in conjunction with the drone's turning rate to ensure
fSpeed = 15

# Initial curve value for turning adjustments
# This variable will be updated based on the sensor readings to determine the drone's turning rate.
# It is initialized to 0, indicating no turning at the start.
# The curve value will be modified in the sendCommands function based on the sensor output.
# A curve value of 0 means the drone will fly straight ahead.
# The curve value will be adjusted to positive or negative values based on the line's position relative to the sensors.
# Positive curve values will cause the drone to turn right, while negative curve values will cause it to turn left.
# The curve value will be calculated using the weights defined earlier, allowing for smooth and responsive turning behavior.
# The curve value will be updated in real-time as the drone processes the video feed and detects the line.
# The curve value will be used in conjunction with the forward speed to control the drone's movement while following the line.
############################# Copilot Generated Comments as suggestions ##############################################################################
# The curve value may need to be adjusted based on the specific characteristics of the line and environment.
# The curve value should be tested in a safe environment to ensure effective line following behavior.
# The curve value may also need to be adjusted based on the drone's battery level, payload, and other factors affecting its performance.
########################################################################################################################################################
curve = 0

# Main loop
# This loop continuously captures frames from the drone's camera, processes the images to detect the line,
# and sends commands to the drone to follow the line based on the detected position.
# The loop runs indefinitely until manually stopped, allowing the drone to continuously adjust its flight path to follow the line.
# The loop includes functions for image thresholding, contour detection, sensor output calculation, and command sending.
# The loop also includes OpenCV functions to display the processed images for debugging and visualization purposes.
# The loop may need to be modified or optimized based on the specific requirements of the line following task and the drone's capabilities.
############################# Copilot Generated Comments as suggestions ##############################################################################
# The loop should be tested in a safe environment to ensure effective and safe line following behavior.
# The loop may also need to include error handling and safety checks to prevent accidents or damage to the drone.
# The loop may also need to include functionality for landing or stopping the drone based on specific conditions or commands.
# The loop may also need to include functionality for adjusting the drone's altitude based on the line's position or other factors.
# The loop may also need to include functionality for handling obstacles or other environmental factors that may affect the drone's ability to follow the line.
# The loop may also need to include functionality for logging or recording data related to the line following task for analysis and improvement.
# The loop may also need to include functionality for integrating with other systems or software for enhanced capabilities or features.
# The loop may also need to include functionality for user input or control to allow for manual adjustments or overrides during the line following task.
########################################################################################################################################################
def thresholding(img):

    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define the lower and upper bounds for the HSV values to create a mask
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    # Define the upper bound for the HSV values to create a mask
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    # Create a binary mask where the specified color range is white and the rest is black
    mask = cv2.inRange(hsv, lower, upper)

    # return the binary mask
    return mask

# Function to get the contours of the detected line and calculate its center position
# This function finds the largest contour in the binary mask, calculates its bounding rectangle,
# and determines the center position of the line for translation adjustments.
# The function also draws the contour and center point on the original image for visualization.
# The center x-coordinate is returned for use in determining the drone's left-right movement.
def getContours(imgThres, img):

    # Initialize center coordinates
    cx = 0
    # Find contours in the binary mask
    # A Contour is a curve joining all the continuous points along a boundary with the same color or intensity.
    # Contours are useful for shape analysis, object detection, and recognition.
    # "contours" is a list of all the contours (Edges) found in the image.
    contours, hieracrhy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # If contours are found, proceed to find the largest one
    if len(contours) != 0:

        # Find the largest contour based on area
        biggest = max(contours, key=cv2.contourArea)
        # Get the bounding rectangle for the largest contour
        x, y, w, h = cv2.boundingRect(biggest)
        # Calculate the center x-coordinate of the bounding rectangle
        cx = x + w // 2
        # Calculate the center y-coordinate of the bounding rectangle
        cy = y + h // 2
        # Draw the bounding rectangle on the original image
        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        # Draw a circle at the center of the bounding rectangle
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

# Function to get the sensor output based on the binary mask
# This function divides the binary mask into vertical segments (sensors) and calculates the proportion of
# white pixels in each segment. If the proportion exceeds a defined threshold, the sensor is considered
# to be detecting the line (output 1), otherwise it is not (output 0).
# The function returns a list of sensor outputs, which is used to determine the drone's turning adjustments.
def getSensorOutput(imgThres, sensors):

    # Divide the binary mask into vertical segments (sensors)
    imgs = np.hsplit(imgThres, sensors)
    # Calculate the total number of pixels in each sensor segment
    # the total number of pixels is used to determine the proportion of white pixels in each segment.
    # to define whether the sensor is detecting the line based on the threshold value. 0 or 1.
    totalPixels = (img.shape[1] // sensors) * img.shape[0]

    # Initialize an empty list to store the sensor outputs
    senOut = []
    # Loop through each sensor segment
    for x, im in enumerate(imgs):
        # Count the number of white pixels in the sensor segment
        pixelCount = cv2.countNonZero(im)
        # Determine if the sensor is detecting the line based on the threshold
        # The threshold value is used to define whether the sensor is detecting the line (output 1) or not (output 0).
        if pixelCount > threshold * totalPixels:
            # If the proportion of white pixels exceeds the threshold, the sensor detects the line
            # Append 1 to the sensor output list
            senOut.append(1)

        else:
            # If the proportion of white pixels does not exceed the threshold, the sensor does not detect the line
            # Append 0 to the sensor output list
            senOut.append(0)

        # cv2.imshow(str(x), im)

    # print(senOut)

    # return the list of sensor outputs
    # an array of 0s and 1s representing the state of each sensor (0 = no line detected, 1 = line detected)
    return senOut

# Function to send movement commands to the drone based on sensor output and line position
# This function calculates the left-right movement and turning adjustments for the drone based on the
# sensor output and the center position of the detected line. It then sends the appropriate commands to
# the drone to follow the line.
def sendCommands(senOut, cx):

    # Use the global curve variable to store the turning adjustment
    global curve

    ## TRANSLATION MOVEMENT ######################
    # Calculate left-right movement based on the center x-coordinate of the line
    lr = (cx - width // 2) // senstivity
    # Limit the left-right movement to be between -10 and 10
    lr = int(np.clip(lr, -10, 10))


    # Dead zone for left-right movement to prevent small oscillations
    # If the left-right movement is between -2 and 2, set it to 0
    if 2 > lr > -2: lr = 0

    ## ROTATION MOVEMENT ##########################

    # Determine the turning adjustment based on the sensor output
    # The sensor output is a list of 0s and 1s representing the state of each sensor (0 = no line detected, 1 = line detected).
    # The turning adjustment is calculated using predefined weights for each possible sensor output combination.
    # The turning adjustment is used to control the drone's rotation to follow the line.
    # 1, 0, 0 = Left
    if senOut == [1, 0, 0]: curve = weights[0]

    # 1, 1, 0 = Slight Left
    elif senOut == [1, 1, 0]: curve = weights[1]
    # 0, 1, 0 = Straight
    elif senOut == [0, 1, 0]: curve = weights[2]
    # 0, 1, 1 = Slight Right
    elif senOut == [0, 1, 1]: curve = weights[3]
    # 0, 0, 1 = Right
    elif senOut == [0, 0, 1]: curve = weights[4]
    # 0, 0, 0 = No line detected (default to Straight)
    elif senOut == [0, 0, 0]: curve = weights[2]
    # 1, 1, 1 = All sensors detect the line (default to Straight)
    elif senOut == [1, 1, 1]: curve = weights[2]
    # 1, 0, 1 = Left and Right sensors detect the line (default to Straight)
    elif senOut == [1, 0, 1]: curve = weights[2]

    # Send the calculated left-right movement and turning adjustment commands to the drone
    me.send_rc_control(lr, fSpeed, 0, curve)

# Main loop to continuously capture frames, process images, and control the drone
while True:

    #_, img = cap.read()

    # Capture a frame from the drone's camera
    img = me.get_frame_read().frame
    # resize the image to the defined width and height
    img = cv2.resize(img, (width, height))
    # invert the image vertically (flip it upside down)
    img = cv2.flip(img, 0)
    # Apply color thresholding to create a binary mask
    imgThres = thresholding(img)
    # Get the contours of the detected line and calculate its center position
    cx = getContours(imgThres, img)  ## For Translation
    # Get the sensor output based on the binary mask
    senOut = getSensorOutput(imgThres, sensors)  ## Rotation
    # Send movement commands to the drone based on sensor output and line position
    sendCommands(senOut, cx)
    # Display the original image with annotations
    cv2.imshow("Output", img)
    # Display the binary mask image
    cv2.imshow("Path", imgThres)
    # Wait for 1 millisecond before capturing the next frame
    cv2.waitKey(1)

