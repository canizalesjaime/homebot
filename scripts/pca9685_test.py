import time
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def set_servo_angle(channel, angle):
    # Typical servo pulse range
    min_pulse = 150   # 0°
    max_pulse = 600   # 180°

    pulse = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
    pca.channels[channel].duty_cycle = int(pulse / 4096 * 65535)

def move_servo(channel):
    set_servo_angle(channel, 0)
    time.sleep(1)
    set_servo_angle(channel, 90)
    time.sleep(1)
    set_servo_angle(channel, 180)
    time.sleep(1)


#move_servo(0) #wrist roll (3)
#move_servo(1) #gripper(weird) (1)
#move_servo(3) #wrist pitch (2)
#move_servo(4) #didnt move
#move_servo(5) #shoulder (5)
#move_servo(7)  #base (6)

pca.deinit()
