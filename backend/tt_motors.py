# PWM is used to control motor speed. Duty cycle(speed) is the percentage of 
# time high per cycle. If high -> motor on if low motor -> off.
# The more time the the signal is high during a cycle the faster the speed.
import time
import lgpio as GPIO
import math


class TtMotors():
    def __init__(self):
        self.h = GPIO.gpiochip_open(0)
        self.driver_map={"a_in1":17,"a_in2":27,"b_in1":23,"b_in2":24,
                     "stby":25, "enA":12, "enB":13}

        for name, pin in self.driver_map.items():
            GPIO.gpio_claim_output(self.h, pin)
        GPIO.gpio_write(self.h, self.driver_map["stby"], 1)

        self.encoder_pins={"left_a":5, "left_b":6, "right_a":16, "right_b":26}        
        GPIO.gpio_claim_alert(self.h, self.encoder_pins["left_a"], GPIO.RISING_EDGE)
        GPIO.gpio_claim_input(self.h, self.encoder_pins["left_b"])
        GPIO.gpio_claim_alert(self.h, self.encoder_pins["right_a"], GPIO.RISING_EDGE)
        GPIO.gpio_claim_input(self.h, self.encoder_pins["right_b"])
        
        #GPIO.gpio_set_debounce_micros(self.h, self.encoder_pins["left_a"], 1000)
        #GPIO.gpio_set_debounce_micros(self.h, self.encoder_pins["right_a"], 1000)

        self.ticks_per_wheel_rev = 1080 # 12 PPR × 90:1 gearbox
        self.frequency=1000
        self.curr_speed=50
        self.set_speed(self.curr_speed)

        self.left_ticks = 0
        self.right_ticks = 0

        # Values used to calculate velocity
        self.previous_left_ticks = 0
        self.previous_right_ticks = 0
        self.previous_time = time.monotonic()

        # Encoder callbacks
        # Manufacturer's example uses rising edge of A. B determines direction.
        self.left_callback = GPIO.callback(
            self.h,
            self.encoder_pins["left_a"],
            GPIO.RISING_EDGE,
            self.left_encoder_event
        )

        self.right_callback = GPIO.callback(
            self.h,
            self.encoder_pins["right_a"],
            GPIO.RISING_EDGE,
            self.right_encoder_event
        )

    ###########################################################################
    def move(self,cmd):
        if cmd == 'f':
            self.set_motor([1, 0, 1, 0])
        elif cmd == 'b':
            self.set_motor([0, 1, 0, 1])
        elif cmd == 'rl':
            self.set_motor([1, 0, 0, 1])
        elif cmd == 'rr':
            self.set_motor([0, 1, 1, 0])
        elif cmd == 'l':
            self.set_motor([1,0,0,0])
        elif cmd == 'r':
            self.set_motor([0,0,1,0])
        elif cmd == 'i':
            self.curr_speed=self.set_speed(self.curr_speed+5)
        elif cmd == 'd':
            self.curr_speed=self.set_speed(self.curr_speed-5)
        else:
            self.set_motor([0, 0, 0, 0])


    ###########################################################################
    def set_motor(self,motor_inputs):
        GPIO.gpio_write(self.h, self.driver_map["a_in1"], motor_inputs[0])
        GPIO.gpio_write(self.h, self.driver_map["a_in2"], motor_inputs[1])
        GPIO.gpio_write(self.h, self.driver_map["b_in1"], motor_inputs[2])
        GPIO.gpio_write(self.h, self.driver_map["b_in2"], motor_inputs[3])
        

    ###########################################################################
    def set_speed(self,percent):
        percent=min(max(percent,0),100)
        GPIO.tx_pwm(self.h, self.driver_map["enA"], self.frequency, percent)
        GPIO.tx_pwm(self.h, self.driver_map["enB"], self.frequency, percent)
        return percent

    
    # Encoder callbacks########################################################
    def left_encoder_event(self, chip, gpio, level, timestamp):
        if GPIO.gpio_read(self.h, self.encoder_pins["left_b"]) == 0:
            self.left_ticks += 1
        else:
            self.left_ticks -= 1

    ###########################################################################
    def right_encoder_event(self, chip, gpio, level, timestamp):
        if GPIO.gpio_read(self.h, self.encoder_pins["right_b"]) == 0:
            self.right_ticks += 1
        else:
            self.right_ticks -= 1

    ###########################################################################
    def get_ticks(self):
        return self.left_ticks, self.right_ticks

    ###########################################################################
    def get_wheel_velocities(self): # angular
        current_time = time.monotonic()

        current_left_ticks = self.left_ticks
        current_right_ticks = self.right_ticks

        dt = current_time - self.previous_time

        if dt <= 0:
            return 0.0, 0.0

        # Number of ticks since last measurement
        left_delta_ticks = current_left_ticks - self.previous_left_ticks
        right_delta_ticks = current_right_ticks - self.previous_right_ticks

        # Save current values for next measurement
        self.previous_left_ticks = current_left_ticks
        self.previous_right_ticks = current_right_ticks
        self.previous_time = current_time

        left_revolutions = left_delta_ticks / self.ticks_per_wheel_rev
        right_revolutions = right_delta_ticks / self.ticks_per_wheel_rev  

        # revolutions → radians
        left_angle = left_revolutions * 2.0 * math.pi
        right_angle = right_revolutions * 2.0 * math.pi

        # radians → radians/second
        left_velocity = left_angle / dt
        right_velocity = right_angle / dt

        return left_velocity, right_velocity

    ###########################################################################
    def reset_ticks(self):
        self.left_ticks = 0
        self.right_ticks = 0

        self.previous_left_ticks = 0
        self.previous_right_ticks = 0

        self.previous_time = time.monotonic()

    ###########################################################################
    def release_lines(self):
        self.move("s")

        GPIO.tx_pwm(self.h, self.driver_map["enA"], self.frequency, 0)
        GPIO.tx_pwm(self.h, self.driver_map["enB"], self.frequency, 0)
        GPIO.gpio_write(self.h, self.driver_map["stby"], 0)

        self.left_callback.cancel()
        self.right_callback.cancel()

        GPIO.gpiochip_close(self.h)


###############################################################################
def main():
    motor=None
    try:
        motor=TtMotors()
        while True:
            cmd=input("Enter -- f(forward), b(back), left(l), right(r), i(increase), d(decrease), stop(any other key): ")
            motor.move(cmd)
            left_tick, right_tick = motor.get_ticks() 
            print(f"total # of wheel revolutions(left,right): ({left_tick/motor.ticks_per_wheel_rev}, {right_tick/motor.ticks_per_wheel_rev})")
            lw, rw = motor.get_wheel_velocities()
            print(f"speed: {motor.curr_speed}. Velocity Vector(left, right) r/s: ({lw},{rw})")
        
    finally:
        if motor is not None:
            motor.release_lines()


if __name__ == '__main__':
    main()