if __name__ == "__main__":
    print("This script must be imported")
    exit()

#import libraries
import gpiozero
import time

# declare rover (base of the LUFbot)
rover = gpiozero.Robot(left=(19, 26), right=(16, 20))

# declare proximity sensor
sensor = gpiozero.DistanceSensor(echo=15, trigger=14)

# decleare speaker (unless @HunterMittan's code is different)
speaker = gpiozero.TonalBuzzer(pin=8)

# fall prevention
def fall(distance):
    # the robot has reached a cliff!!
    speaker.play("A4")
    rover.backward()
    while True:
        if (sensor.distance < distance):
            break
        else:
            time.sleep(0.1)
    speaker.stop()
    rover.stop()


def motor_test():
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


def sensor_test(samples=10, sleep_time=0.1):
    avg = 0
    for x in range(samples):
        avg += sensor.distance
        time.sleep(sleep_time)
    avg /= samples
    print(f"average distance from ground is: {avg} meters")
    return avg
