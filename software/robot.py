if __name__ == "__main__":
    print("This script must be imported")
    exit()

#import libraries
import gpiozero
import time

#declare rover (base of the LUFbot)
rover = gpiozero.Robot(left=(19,26), right=(16,20))

#declare proximity sensor
sensor = gpiozero.DistanceSensor(echo=15, trigger=14, threshold_distance=0.07)

#decleare speaker (unless @HunterMittan's code is different)
speaker = gpiozero.TonalBuzzer(pin=8)

#maybe declare LEDs, not sure

#fall prevention
def fall():
    # the robot has reached a cliff!!
    speaker.play("A4")
    rover.backward()
    sensor.wait_for_in_range()
    speaker.stop()
    rover.stop()

sensor.when_out_of_range = fall

