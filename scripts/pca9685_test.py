import time
import board
import busio
from adafruit_pca9685 import PCA9685

# ------------------ I2C + PCA9685 ------------------
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# ------------------ PWM Calibration ------------------
# Wide pulse range for near-180° travel
# Adjust slightly per servo if needed
MIN_PULSE = 150   # ~0.75 ms
MAX_PULSE = 550   # ~2.7 ms

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
    min_angle, max_angle = SERVO_LIMITS.get(channel, (0, 180))
    angle = max(min(angle, max_angle), min_angle)

    pulse = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    duty = int(pulse / 4096 * 65535)
    pca.channels[channel].duty_cycle = duty


def move_smooth(channel, start, end, step=2, delay=0.02):
    if start < end:
        rng = range(start, end + 1, step)
    else:
        rng = range(start, end - 1, -step)

    for angle in rng:
        set_servo_angle(channel, angle)
        time.sleep(delay)


def move_servo(channel):
    min_angle, max_angle = SERVO_LIMITS.get(channel, (0, 180))
    move_smooth(channel, min_angle, max_angle)
    time.sleep(0.5)
    move_smooth(channel, max_angle, min_angle)
    time.sleep(0.5)

# ------------------ Run ------------------
try:
    # move_servo(0)  # wrist roll
    # move_servo(1)  # gripper - BROKE
    # move_servo(3)  # wrist pitch
    # move_servo(4)  # elbow
    # move_servo(5)  # shoulder
    # move_servo(7)  # base

    #for i in range(0,50,10):
    #    set_servo_angle(1,i)

    set_servo_angle(1,70)
    time.sleep(3)
    set_servo_angle(1,0)    
    #set_servo_angle(1,170)
    pca.deinit()

finally:
    pca.deinit()
