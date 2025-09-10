
#Get Frame from Drone
#Once we have setup the tello drone we will get the frame/image from it. We will create a simple function for this, that will take the drone object as the input argument and return the current image.

def telloGetFrame(myDrone,w=360,h=240):
# GET THE IMGAE FROM TELLO
myFrame = myDrone.get_frame_read()
myFrame = myFrame.frame
img = cv2.resize(myFrame, (w, h))
return img

#Now we will call this function inside a while loop.
while True:
## STEP 1
img = telloGetFrame(myDrone)
# DISPLAY IMAGE
cv2.imshow("MyResult", img)
# WAIT FOR THE 'Q' BUTTON TO STOP
if cv2.waitKey(1) and 0xFF == ord('q'):
# replace the 'and' with '&amp;'
myDrone.land()
break