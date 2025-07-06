#from gpiozero import AngularServo
import gpiod
from time import sleep 

## USING GPIZERO ##############################################################
# servo1 = AngularServo(14, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000) #base
# servo2 = AngularServo(18, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000) #shoulder
# servo3 = AngularServo(25, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000) #elbow
# servo4 = AngularServo(12, min_angle=0,max_angle=180,min_pulse_width=.5/1000,max_pulse_width=2.5/1000) #girpper

# try:
#     while True:
#         angle=int(input("Enter angle: (0 to 180):"))
#         servo1.angle=angle
#         sleep(1)
#         servo2.angle=angle
#         sleep(1)
#         servo3.angle=angle
#         sleep(1)
#         servo4.angle=angle
#         sleep(1)
# except KeyboardInterrupt:
#     print("stopped")
###############################################################################

## USING PIGPIO ###############################################################
pi = pigpio.pi()

try:
    while True:
        angle1=int(input("Enter base angle(frequency): 0 or 500-2500"))
        pi.set_servo_pulsewidth(14, angle1)
        sleep(1)
        pi.set_servo_pulsewidth(18, angle1)
        sleep(1)
        pi.set_servo_pulsewidth(25, angle1)
        sleep(1)
        pi.set_servo_pulsewidth(12, angle1)
        sleep(1)

except KeyboardInterrupt:
    print("Stopped")
###############################################################################

