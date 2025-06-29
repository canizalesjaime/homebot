import lgpio
import time

h = lgpio.gpiochip_open(0)
SERVO_PIN = 18  # GPIO number
FREQ = 50       # Servo expects 50 Hz

def set_servo_pulse_us(pulse_width_us):
    duty_percent = (pulse_width_us / 20000) * 100
    print(f"Setting pulse width: {pulse_width_us} µs ({duty_percent:.2f}%)")
    lgpio.tx_pwm(h, SERVO_PIN, FREQ, duty_percent)

try:
    while True:
        set_servo_pulse_us(1000)  # ~0°
        time.sleep(1)
        set_servo_pulse_us(2000)  # ~180°
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping")
    lgpio.tx_pwm(h, SERVO_PIN, 0, 0)
    lgpio.gpiochip_close(h)


# import pigpio
# import time

# pi = pigpio.pi()

# # Use GPIO18
# SERVO_PIN = 13

# while True:
#     pi.set_servo_pulsewidth(SERVO_PIN, 1000)
#     time.sleep(1)
#     pi.set_servo_pulsewidth(SERVO_PIN, 2000)
#     time.sleep(1)
