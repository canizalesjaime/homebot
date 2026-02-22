import time
import board
import busio
from adafruit_pca9685 import PCA9685


class SmallArmNode():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50

        self.SERVO_ANGLES = { 0: 90,   # base
                            #   1: 90,   # elbow
                            #   3: 90,   # shoulder
                            #   4: 90,   # gripper
        }

        for serv in self.SERVO_ANGLES:
            self.set_servo_angle(serv,90)


    def set_servo_angle(self,channel, angle):
        MIN_PULSE = 150   # ~0.75 ms, 0 degrees
        MAX_PULSE = 550   # ~2.7 ms, 180 degrees
        min_angle, max_angle = (10,170)
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


    def rotate_base(self):
        while True:
            self.move_smooth(0,90,170)
            self.move_smooth(0,170,90)
            self.move_smooth(0,90,10)
            self.move_smooth(0,10,90)



def main():
    try:
        node =SmallArmNode()
        node.rotate_base()

    finally:
        node.pca.deinit()

main()
