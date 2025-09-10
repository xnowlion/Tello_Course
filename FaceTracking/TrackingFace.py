#https://www.computervision.zone/topic/tracking-the-face/
#Drone Programming Course>Face Tracking> Tracking the Face
#Tracking the Face

#To track the face we will create a function that will use the information of the face and try to follow it. We could simply assgin a value of speed but instead we will be using varying speed based on how far the face is. This can be achieved using PID controller. We will only use the Propotional and Derivative part of the controller.
#PID Controller
def trackFace(myDrone,c,w,pid,pError):
print(c)
## PIDerror = c[0][0] - w//2
# Current Value - Target Value
speed = int(pid[0]*error + pid[1] * (error-pError))

#Sending Rotation to Drone
#Once we have the speed value we can send it to the drone. But before we do that we will just make sure that the face is detected.
if c[0][0] != 0:
myDrone.yaw_velocity = speed
else:
myDrone.left_right_velocity = 0
myDrone.for_back_velocity = 0
myDrone.up_down_velocity = 0
myDrone.yaw_velocity = 0
error = 0
# SEND VELOCITY VALUES TO TELLO
if myDrone.send_rc_control:
myDrone.send_rc_control(myDrone.left_right_velocity,myDrone.for_back_velocity,
myDrone.up_down_velocity, myDrone.yaw_velocity)

#Now we will return the error since we will need it for the calculation of the Derivative part of the PID controller in the next frame.
	return error

#Lastly we will call this function in the main script.
	## STEP 3
pError = trackFace(myDrone,c,w,pid,pError)