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
    0: (10, 170),   # wrist roll (MG90S)
    1: (10, 170),   # gripper (MG90S)
    3: (10, 170),   # wrist pitch (MG90S)
    4: (20, 160),   # elbow (MG995)
    5: (20, 160),   # shoulder (MG995)
    7: (20, 160),   # base (MG995)
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
    for s in SERVO_LIMITS: 
        set_servo_angle(s,10)
        time.sleep(2)     
    move_smooth(1,10,70) 
    move_smooth(7,10,170) 

# ------------------ Servo Functions ------------------
def pick_up_static_hacky():
    move_smooth(3,10,130)
    move_smooth(5,10,80)
    move_smooth(0,10,80)
    move_smooth(1,70,10)

# ------------------ Run ------------------
try:
    straighten_arm()
    pick_up_static_hacky()

finally:
    pca.deinit()
