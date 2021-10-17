#import libraries
import gpiozero
import time

# declare rover (base of the LUFbot)
rover = gpiozero.Robot(left=(19, 26), right=(16, 20))
rover.left()
print("Left!")
time.sleep(1)
rover.right()
print("Right!")
time.sleep(1)
rover.forward()
print("Forward!")
time.sleep(1)
rover.backward()
print("Backward!")
time.sleep(1)
rover.stop()
print("Stopped!")
