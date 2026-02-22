# PWM Calibration 
# Wide pulse range for near-180° travel
# Adjust slightly per servo if needed
# note: since 50HZ, one cycle last 20 ms
# this is # of ticks out of 4096 to represent high
# 4096 comes from the PCA9685’s 12-bit PWM resolution, 
# and 65535 comes from CircuitPython’s 16-bit duty-cycle interface.
# pulses below are estimated, and in general should be calibrated

# ADD WEBSITE
# STORE PREV ANGLE

import time
import board
import busio
from adafruit_pca9685 import PCA9685


class SmallArmNode():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50


        self.SERVO_LIMITS = { 0: (10, 170), # base
            1: (10, 170),   # elbow
            3: (10, 170),   # shoulder
            4: (10, 170),   # gripper
        }

        self.SERVO_ANGLES = { 0: 90,   # base
                              1: 90,   # elbow
                              3: 90,   # shoulder
                              4: 90,   # gripper
        }

        for serv in self.SERVO_ANGLES:
            self.set_servo_angle(serv,90)


    def set_servo_angle(self,channel, angle):
        MIN_PULSE = 150   # ~0.75 ms, 0 degrees
        MAX_PULSE = 550   # ~2.7 ms, 180 degrees
        min_angle, max_angle = self.SERVO_LIMITS.get(channel, (0, 180))
        angle = max(min(angle, max_angle), min_angle)

        pulse = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
        duty = int(pulse / 4096 * 65535)
        self.pca.channels[channel].duty_cycle = duty
        self.SERVO_ANGLES[channel]=angle


    def move_smooth(self,channel, start, end, step=2, delay=0.02):
        if start < end:
            rng = range(start, end + 1, step)
        else:
            rng = range(start, end - 1, -step)

        for angle in rng:
            self.set_servo_angle(channel, angle)
            time.sleep(delay)
        #time.sleep(1)


    def straighten_arm(self):
        self.move_smooth(3,40,170)
        self.move_smooth(4,0,170)


    def pick_up_static_hacky(self):
        self.move_smooth(3,170,40)
        self.move_smooth(4,170,0)


    def rotate_base(self):
        while True:
            self.move_smooth(0,90,170)
            self.move_smooth(0,170,90)
            self.move_smooth(0,90,10)
            self.move_smooth(0,10,90)


    def set_angles_api(self, angles):
        for i,channel in enumerate(self.SERVO_ANGLES):
            self.move_smooth(channel, self.SERVO_ANGLES[channel],angles[i])

def main():
    try:
        node =SmallArmNode()
        node.rotate_base()

    finally:
        node.pca.deinit()
