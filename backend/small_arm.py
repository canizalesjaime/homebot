# ADD TO WEBSITE 

import time
import board
import busio
from adafruit_pca9685 import PCA9685

# ------------------ I2C + PCA9685 ------------------
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# ------------------ Per-servo angle limits ------------------
SERVO_LIMITS = {
    0: (10, 170),   # base
    1: (10, 170),   # elbow
    3: (10, 170),   # shoulder
    4: (10, 170),   # gripper
   
}

# ------------------ Servo Functions ------------------
def set_servo_angle(channel, angle):
    # PWM Calibration 
    # Wide pulse range for near-180° travel
    # Adjust slightly per servo if needed
    # note: since 50HZ, one cycle last 20 ms
    # this is # of ticks out of 4096 to represent high
    # 4096 comes from the PCA9685’s 12-bit PWM resolution, 
    # and 65535 comes from CircuitPython’s 16-bit duty-cycle interface.
    # pulses below are estimated, and in general should be calibrated
    MIN_PULSE = 150   # ~0.75 ms, 0 degrees
    MAX_PULSE = 550   # ~2.7 ms, 180 degrees
    min_angle, max_angle = SERVO_LIMITS.get(channel, (0, 180))
    angle = max(min(angle, max_angle), min_angle)

    pulse = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    duty = int(pulse / 4096 * 65535)
    pca.channels[channel].duty_cycle = duty

# ------------------ Servo Functions ------------------
def move_smooth(channel, start, end, step=2, delay=0.02):
    if start < end:
        rng = range(start, end + 1, step)
    else:
        rng = range(start, end - 1, -step)

    for angle in rng:
        set_servo_angle(channel, angle)
        time.sleep(delay)
    time.sleep(2)

# ------------------ Servo Functions ------------------
def move_servo_full_range(channel):
    min_angle, max_angle = SERVO_LIMITS.get(channel, (0, 180))
    move_smooth(channel, min_angle, max_angle)
    time.sleep(2)

# ------------------ Servo Functions ------------------
def straighten_arm():
    move_smooth(3,40,170)
    move_smooth(4,0,170)

# ------------------ Servo Functions ------------------
def pick_up_static_hacky():
    move_smooth(3,170,40)
    move_smooth(4,170,0)

# ------------------ Run ------------------
try:
    pick_up_static_hacky()
    straighten_arm()

finally:
    pca.deinit()
