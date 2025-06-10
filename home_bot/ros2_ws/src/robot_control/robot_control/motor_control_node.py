# robot_control/motor_control_node.py
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
        #self.create_subscription(Float32, 'distance', self.cmd_callback, 10)

        chip = gpiod.Chip('/dev/gpiochip0')
        self.in1 = chip.get_line(17)
        self.in2 = chip.get_line(27)
        self.in3 = chip.get_line(23)
        self.in4 = chip.get_line(24)
        for line in [self.in1, self.in2, self.in3, self.in4]:
            line.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)

        self.h = GPIO.gpiochip_open(0)
        GPIO.gpio_claim_output(self.h, 4)
        GPIO.gpio_claim_output(self.h, 26)
        self.frequency =1000
        self.set_speed(100)

    def cmd_callback(self, msg):
        cmd = msg.data
        print(cmd)
        # key=input("Enter a for forward, z for backwards, and any other key to stop")
        # if key == 'a' and cmd > 8:
        #     self.set_motor(0, 1, 0, 1)
        # elif key == 'z':
        #     self.set_motor(1, 0, 1, 0)
        # else:
        #     self.set_motor(0, 0, 0, 0)
        
        if cmd == 'forward':
            self.set_motor(0, 1, 0, 1)
        elif cmd == 'backward':
            self.set_motor(1, 0, 1, 0)
        elif cmd == 'stop':
            self.set_motor(0, 0, 0, 0)
        else:
            self.get_logger().warn(f'Unknown command: {cmd}')


    def set_motor(self, i1, i2, i3, i4):
        self.in1.set_value(i1)
        self.in2.set_value(i2)
        self.in3.set_value(i3)
        self.in4.set_value(i4)

    def release_lines(self):
        self.in1.release()
        self.in2.release()
        self.in3.release()
        self.in4.release()
        GPIO.tx_pwm(self.h, 4, self.frequency, 0)
        GPIO.tx_pwm(self.h, 26, self.frequency, 0)
        GPIO.gpiochip_close(self.h)

    def set_speed(self,percent):
        if percent < 0:
            percent = 0
        if percent > 100:
            percent = 100
        
        GPIO.tx_pwm(self.h, 4, self.frequency, percent)
        GPIO.tx_pwm(self.h, 26,self.frequency, percent)

         

def main():
    rclpy.init()
    node = MotorControlNode()
    rclpy.spin(node)
    node.release_lines()
    node.destroy_node()
    rclpy.shutdown()
