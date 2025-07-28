import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
import curses
import gpiod
import lgpio as GPIO


class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control_node')

        self.cmd_sub = self.create_subscription(String, 'cmd_motor', self.cmd_callback, 10)

        chip = gpiod.Chip('/dev/gpiochip0')
        # gpios used in drivers_map
        self.drivers_input_map ={"driver1_in1": chip.get_line(17), "driver1_in2": chip.get_line(27),
                           "driver1_in3": chip.get_line(23),"driver1_in4": chip.get_line(24),
                           "driver2_in1": chip.get_line(16), "driver2_in2": chip.get_line(13),
                           "driver2_in3": chip.get_line(22),"driver2_in4": chip.get_line(12)} 

        self.drivers_enable_pin_map ={"driver1_enA":4,"driver1_enB":26,
                                      "driver2_enA":25,"driver2_enB":14}
        
        for name, line in self.drivers_input_map.items():
            line.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)

        self.h = GPIO.gpiochip_open(0)
        for name, pin in self.drivers_enable_pin_map.items():
            GPIO.gpio_claim_output(self.h, pin) 

        self.frequency =1000
        self.set_speed(100)


    ###########################################################################
    def cmd_callback(self, msg):
        cmd = msg.data
        print(cmd)

        if cmd == 'forward':
            self.set_motor([0, 1, 0, 1, 1, 0, 1, 0])
        elif cmd == 'backward':
            self.set_motor([1, 0, 1, 0, 0, 1, 0, 1])
        elif cmd == 'rotate_left':
            self.set_motor([1, 0, 0, 1, 1, 0, 0, 1])
        elif cmd == 'rotate_right':
            self.set_motor([0, 1, 1, 0, 1, 0, 0, 1])
        elif cmd == 'stop':
            self.set_motor([0, 0, 0, 0, 0, 0, 0, 0])
        else:
            self.get_logger().warn(f'Unknown command: {cmd}')

    # python version >= 3.7, and dictionaries are ordered by insert
    ###########################################################################
    def set_motor(self, motor_inputs):
        i = 0 
        for name, line in self.drivers_input_map.items():
            line.set_value(motor_inputs[i])
            i=i+1
        

    ###########################################################################
    def release_lines(self):
        for name, line in self.drivers_input_map.items():
            line.release()
        
        for name, pin in self.drivers_enable_pin_map.items():
            GPIO.tx_pwm(self.h, pin, self.frequency, 0)
        GPIO.gpiochip_close(self.h)


    ###########################################################################
    def set_speed(self,percent):
        percent=min(max(percent,0),100)
        
        for name, pin in self.drivers_enable_pin_map.items():
            GPIO.tx_pwm(self.h, pin, self.frequency, percent)
         

###############################################################################
def main():
    rclpy.init()
    node = MotorControlNode()
    rclpy.spin(node)
    node.release_lines()
    node.destroy_node()
    rclpy.shutdown()
