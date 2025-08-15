import gpiod
import lgpio as GPIO


chip = gpiod.Chip('/dev/gpiochip0')
# gpios used in drivers_map
drivers_input_map ={"driverA_in1": chip.get_line(16), "driverA_in2": chip.get_line(33),
                    "driverB_in1": chip.get_line(22),"driverB_in2": chip.get_line(12) }
drivers_enable_pin_map ={"driverA_enA":25,"driverB_enB":14}

stby = chip.get_line(7)
stby.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)
stby.set_value(1)

for name, line in drivers_input_map.items():
    line.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)

h = GPIO.gpiochip_open(0)
for name, pin in drivers_enable_pin_map.items():
    GPIO.gpio_claim_output(h, pin) 

frequency =1000
curr_speed=75


###########################################################################
def move(cmd):
    global curr_speed
    print(cmd, "speed: ", curr_speed)

    if cmd == 'forward':
        set_motor([1, 0, 1, 0])
    elif cmd == 'backward':
        set_motor([0, 1, 0, 1])
    elif cmd == 'rotate_left':
        set_motor([0, 1, 1, 0])
    elif cmd == 'rotate_right':
        set_motor([1, 0, 0, 1])
    elif cmd == 'stop':
        set_motor([0, 0, 0, 0])
    elif cmd == 'increase':
        curr_speed=curr_speed+5
        set_speed(curr_speed)
    elif cmd == 'decrease':
        curr_speed=curr_speed-5
        set_speed(curr_speed)
    else:
        print("error worng command")

# python version >= 3.7, and dictionaries are ordered by insert
###########################################################################
def set_motor(motor_inputs):
    i = 0 
    for name, line in drivers_input_map.items():
        line.set_value(motor_inputs[i])
        i=i+1
    

###########################################################################
def release_lines():
    global stby
    for name, line in drivers_input_map.items():
        line.set_value(0)
        line.release()
    
    for name, pin in drivers_enable_pin_map.items():
        GPIO.tx_pwm(h, pin, frequency, 0)
    GPIO.gpiochip_close(h)

    stby.set_value(0)
    stby.release()


###############################################################################
def set_speed(percent):
    percent=min(max(percent,0),100)
    
    for name, pin in drivers_enable_pin_map.items():
        GPIO.tx_pwm(h, pin, frequency, percent)
         

###############################################################################
def main():
    try:
        set_speed(curr_speed)
        while True:
            cmd=input("enter one of the following - forward, backward, increase, decrease, rotate_left, rotate_right: ")
            move(cmd)
        
    finally:
        release_lines()


if __name__ == "__main__":
    main()