import time
import threading
import sys
import curses
from motor_node import MotorNode
from ultrasonic import UltrasonicNode


# Shared state
current_action = None
dist = 0
action_lock = threading.Lock()
motor=MotorNode()
ultra = UltrasonicNode()
stop_event=threading.Event()


def distance_monitor():
    global current_action, dist, motor, ultra
    while not stop_event.is_set():
        dist = ultra.get_distance()
        with action_lock:
            if current_action == 'forward' and dist <= 11.0:
                print("Obstacle detected! Stopping.")
                motor.move("s")
                current_action = None
        time.sleep(0.2)


# Start distance monitoring thread
monitor_thread = threading.Thread(target=distance_monitor, daemon=True)
monitor_thread.start()


def curses_input_control():
    global current_action, motor, ultra

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
                            motor.move("f")
                            current_action = 'forward'
                    elif key == ord('z'):
                        if current_action != 'backward':
                            stdscr.addstr(1, 0, "Moving backward       ")
                            motor.move("b")
                            current_action = 'backward'
                    elif key == ord('x'):
                        stdscr.addstr(1, 0, "Stopped               ")
                        motor.move("s")
                        current_action = None
                    elif key == ord('j'):
                        stdscr.addstr(1, 0, "Turning left          ")
                        motor.move("l")
                        current_action = 'left'
                    elif key == ord('l'):
                        stdscr.addstr(1, 0, "Turning right         ")
                        motor.move("r")
                        current_action = 'right'
                    elif key == ord('q'):
                        stdscr.addstr(1, 0, "Rotating left         ")
                        motor.move("rl")
                        current_action = 'rotate_left'
                    elif key == ord('e'):
                        stdscr.addstr(1, 0, "Rotating right        ")
                        motor.move("rr")
                        current_action = 'rotate_right'
                    elif key == -1:
                        if current_action is not None:
                            stdscr.addstr(1, 0, "Key released. Stopping.")
                            motor.move("s")
                            current_action = None

                stdscr.refresh()
                time.sleep(0.05)

            except KeyboardInterrupt:
                break

    curses.wrapper(control_loop)


try:
    curses_input_control()

except KeyboardInterrupt:
    print("\nExiting...")
   
finally:
    stop_event.set()
    monitor_thread.join()
    motor.release_lines()
    ultra.free_gpio()

