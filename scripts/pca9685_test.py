import time
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# def set_servo_angle(channel, angle):
#     # Typical servo pulse range
#     min_pulse = 150   # 0°
#     max_pulse = 600   # 180°

#     pulse = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
#     pca.channels[channel].duty_cycle = int(pulse / 4096 * 65535)

# def move_servo(channel):
#     set_servo_angle(channel, 0)
#     time.sleep(1)
#     #set_servo_angle(channel, 90)
#     time.sleep(1)
#     set_servo_angle(channel, 180)
#     time.sleep(1)



# ------------------ Servo calibration ------------------
# Safe PWM range for MG90S and MG995
MIN_PULSE = 205   # ~1.0 ms
MAX_PULSE = 410   # ~2.0 ms

# Per-servo angle limits (adjust if needed)
SERVO_LIMITS = {
    0: (10, 170),   # MG90S
    1: (10, 170),   # MG90S
    3: (10, 170),   # MG90S
    4: (20, 160),   # MG995
    5: (20, 160),   # MG995
    7: (20, 160),   # MG995
}

# ------------------ Servo functions ------------------
def set_servo_angle(channel, angle):
    min_angle, max_angle = SERVO_LIMITS.get(channel, (10, 170))
    angle = max(min(angle, max_angle), min_angle)

    pulse = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    duty = int(pulse / 4096 * 65535)
    pca.channels[channel].duty_cycle = duty


def move_servo(channel):
    min_angle, max_angle = SERVO_LIMITS.get(channel, (10, 170))

    move_smooth(channel, min_angle, max_angle)
    time.sleep(0.5)
    move_smooth(channel, max_angle, min_angle)
    time.sleep(0.5)


def move_smooth(channel, start, end, step=2, delay=0.02):
    if start < end:
        rng = range(start, end + 1, step)
    else:
        rng = range(start, end - 1, -step)

    for angle in rng:
        set_servo_angle(channel, angle)
        time.sleep(delay)

# ------------------ Run ------------------
# #move_servo(0) #wrist roll (3)
#move_servo(1) #gripper(weird) (1)
# #move_servo(3) #wrist pitch (2)
# #move_servo(4) #elbow(4) fix wires 
move_servo(4) #shoulder (5) fix wires
# #move_servo(7)  #base (6)

pca.deinit()
