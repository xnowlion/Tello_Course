#https://www.computervision.zone/topic/setup-and-acquiring-frame/

#Setup Drone
#In this Tutorial we are going to program a drone to track a face. We will do this using opencv and apply a PID controller to have smooth movements.
#First we will create a utilities file in which we will add all the functions. Then we will import all the tello and the cv2 packages.

from djitellopy
import Telloimport cv2

#Then we will create the tello intitialization function that will setup the tello drone for flight and send commands. We will set all the speed to 0. We have 4 types of speeds
#    Forward Backwards
#    Left Right
#    Up Down
#    Yaw (rotation)

def intializeTello():
# CONNECT TO TELLO
myDrone = Tello()
myDrone.connect()
myDrone.for_back_velocity = 0
myDrone.left_right_velocity = 0
myDrone.up_down_velocity = 0
myDrone.yaw_velocity = 0
myDrone.speed =0
print(myDrone.get_battery())
myDrone.streamoff()
myDrone.streamon()
return myDrone

#Now we will call this function in the main script.
myDrone = intializeTello()