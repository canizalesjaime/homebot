#from gpiozero import AngularServo
import gpiod
import pigpio
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

motor_map={"base_gpio":14,"shoulder_gpio":18,"arm_gpio":25,"gripper_gpio":12}

def degrees_to_pulse(deg):
    if not 0 <= deg <= 180:
        raise ValueError("angle must be between 0 and 180")

    return int(500+(deg/180)*(2000))
            

try:
    pi.set_servo_pulsewidth(motor_map["shoulder_gpio"], degrees_to_pulse(100))
    sleep(1)
    while True:
        pi.set_servo_pulsewidth(motor_map["arm_gpio"], degrees_to_pulse(0))
        sleep(1)
        pi.set_servo_pulsewidth(motor_map["arm_gpio"], degrees_to_pulse(90))
        sleep(1)
        pi.set_servo_pulsewidth(motor_map["gripper_gpio"], degrees_to_pulse(0)) #closed
        sleep(1)
        pi.set_servo_pulsewidth(motor_map["gripper_gpio"], degrees_to_pulse(90))
        sleep(1)
        
except KeyboardInterrupt:
    print("Stopped")

finally:
    for key, val in motor_map.items():
        pi.set_servo_pulsewidth(val,0)

###############################################################################

