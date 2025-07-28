import lgpio as GPIO
import gpiod
import time
import threading
import sys
import curses

# Set pins
TRIG = 5
ECHO = 6

chip = gpiod.Chip('/dev/gpiochip0')

# Set motor pins
in1_line = chip.get_line(17)
in2_line = chip.get_line(27)
in3_line = chip.get_line(23)
in4_line = chip.get_line(24)


in1_line2 = chip.get_line(16)
in2_line2 = chip.get_line(13)
in3_line2 = chip.get_line(22)
in4_line2 = chip.get_line(12)


# Request output lines
for line in [in1_line, in2_line, in3_line, in4_line, in1_line2, in2_line2, in3_line2, in4_line2]:
    line.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)

# Motor control functions
def motor_right_backward(): in1_line.set_value(1); in2_line.set_value(0); in1_line2.set_value(0); in2_line2.set_value(1)
def motor_left_backward(): in3_line.set_value(1); in4_line.set_value(0); in3_line2.set_value(0); in4_line2.set_value(1)
def motor_right_forward(): in1_line.set_value(0); in2_line.set_value(1); in1_line2.set_value(1); in2_line2.set_value(0)
def motor_left_forward(): in3_line.set_value(0); in4_line.set_value(1); in3_line2.set_value(1); in4_line2.set_value(0)
def motor_stop():
    in1_line.set_value(0); in2_line.set_value(0)
    in3_line.set_value(0); in4_line.set_value(0)
    in1_line2.set_value(0); in2_line2.set_value(0)
    in3_line2.set_value(0); in4_line2.set_value(0)

def turn_left():
    in3_line.set_value(0); in4_line.set_value(0)  # Stop left motor
    in3_line2.set_value(0); in4_line2.set_value(0)
    motor_right_forward()

def turn_right():
    in1_line.set_value(0); in2_line.set_value(0)  # Stop right motor
    in1_line2.set_value(0); in2_line2.set_value(0)
    motor_left_forward()

def rotate_left():
    motor_right_forward()
    motor_left_backward()

def rotate_right():
    motor_right_backward()
    motor_left_forward()

# Setup GPIO for ultrasonic
h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h, TRIG)
GPIO.gpio_claim_input(h, ECHO)

PWM_FREQUENCY = 1000  # Hz
PWM_PERIOD_US = int(1_000_000 / PWM_FREQUENCY)  # = 1000 µs for 1 kHz

GPIO.gpio_claim_output(h, 4)
GPIO.gpio_claim_output(h, 26)
GPIO.gpio_claim_output(h, 14)
GPIO.gpio_claim_output(h, 25)


def set_speed(percent):
    percent = max(0, min(percent, 100))
    duty_us = int((percent / 100.0) * PWM_PERIOD_US)
    
    GPIO.tx_pwm(h, 4, PWM_FREQUENCY, percent)
    GPIO.tx_pwm(h, 26, PWM_FREQUENCY, percent)
    GPIO.tx_pwm(h, 14, PWM_FREQUENCY, percent)
    GPIO.tx_pwm(h, 25, PWM_FREQUENCY, percent)

def stop_pwm():
    GPIO.tx_pwm(h, 4, PWM_FREQUENCY, 0)
    GPIO.tx_pwm(h, 26, PWM_FREQUENCY, 0)
    GPIO.tx_pwm(h, 14, PWM_FREQUENCY, 0)
    GPIO.tx_pwm(h, 25, PWM_FREQUENCY, 0)

def get_distance():
    GPIO.gpio_write(h, TRIG, 0)
    time.sleep(0.0002)
    GPIO.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    GPIO.gpio_write(h, TRIG, 0)

    start = time.time()
    while GPIO.gpio_read(h, ECHO) == 0:
        start = time.time()
    while GPIO.gpio_read(h, ECHO) == 1:
        end = time.time()

    duration = end - start
    distance = duration * 17150  # cm
    return round(distance / 2.54, 2)  # return inches

# Shared state
current_action = None
dist = 0
action_lock = threading.Lock()

def distance_monitor():
    global current_action, dist
    while True:
        dist = get_distance()
        with action_lock:
            if current_action == 'forward' and dist <= 11.0:
                print("Obstacle detected! Stopping.")
                motor_stop()
                current_action = None
        time.sleep(0.2)

# Start distance monitoring thread
monitor_thread = threading.Thread(target=distance_monitor, daemon=True)
monitor_thread.start()

def curses_input_control():
    global current_action

    def control_loop(stdscr):
        global current_action
        stdscr.nodelay(True)
        stdscr.clear()
        stdscr.addstr(0, 0, "Controls: 'a'=forward, 'z'=backward, 'x'=stop, 'j'=left, 'l'=right, 'q'=rotate left, 'e'=rotate right. Ctrl+C to exit.")
        stdscr.refresh()

        while True:
            try:
                key = stdscr.getch()

                with action_lock:
                    if key == ord('a'):
                        if current_action != 'forward' and dist > 8:
                            stdscr.addstr(1, 0, "Moving forward        ")
                            motor_right_forward()
                            motor_left_forward()
                            current_action = 'forward'
                    elif key == ord('z'):
                        if current_action != 'backward':
                            stdscr.addstr(1, 0, "Moving backward       ")
                            motor_right_backward()
                            motor_left_backward()
                            current_action = 'backward'
                    elif key == ord('x'):
                        stdscr.addstr(1, 0, "Stopped               ")
                        motor_stop()
                        current_action = None
                    elif key == ord('j'):
                        stdscr.addstr(1, 0, "Turning left          ")
                        turn_left()
                        current_action = 'left'
                    elif key == ord('l'):
                        stdscr.addstr(1, 0, "Turning right         ")
                        turn_right()
                        current_action = 'right'
                    elif key == ord('q'):
                        stdscr.addstr(1, 0, "Rotating left         ")
                        rotate_left()
                        current_action = 'rotate_left'
                    elif key == ord('e'):
                        stdscr.addstr(1, 0, "Rotating right        ")
                        rotate_right()
                        current_action = 'rotate_right'
                    elif key == -1:
                        if current_action is not None:
                            stdscr.addstr(1, 0, "Key released. Stopping.")
                            motor_stop()
                            current_action = None

                stdscr.refresh()
                time.sleep(0.05)

            except KeyboardInterrupt:
                break

    curses.wrapper(control_loop)

try:
    set_speed(75)
    curses_input_control()

except KeyboardInterrupt:
    print("\nExiting...")
    motor_stop()
    GPIO.gpiochip_close(h)

finally:
    in1_line.release()
    in2_line.release()
    in3_line.release()
    in4_line.release()
    in1_line2.release()
    in2_line2.release()
    in3_line2.release()
    in4_line2.release()
    stop_pwm()
