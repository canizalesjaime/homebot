from gpiozero import AngularServo
from time import sleep 

servo1 = AngularServo(14, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000) #base
servo2 = AngularServo(18, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000)
servo3 = AngularServo(12, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000)
servo4 = AngularServo(25, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000)


try:
    while True:
        angle=int(input("Enter angle: (0 to 180):"))
        servo1.angle=angle
        sleep(1)
        servo2.angle=angle
        sleep(1)
        servo3.angle=angle
        sleep(1)
        servo4.angle=angle
        sleep(1)
except KeyboardInterrupt:
    print("stopped")
