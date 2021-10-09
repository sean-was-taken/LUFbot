from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=15, trigger=14)

avg = 0
for x in range(10):
  avg += ultrasonic.distance

avg /= 10

print(f"average distance from ground is: {avg} meters")
