# robot_control/motor_control_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import gpiod

class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control_node')

        self.cmd_sub = self.create_subscription(String, 'cmd_motor', self.cmd_callback, 10)

        chip = gpiod.Chip('/dev/gpiochip0')
        self.in1 = chip.get_line(17)
        self.in2 = chip.get_line(27)
        self.in3 = chip.get_line(23)
        self.in4 = chip.get_line(24)
        for line in [self.in1, self.in2, self.in3, self.in4]:
            line.request(consumer='motor_control', type=gpiod.LINE_REQ_DIR_OUT)

    def cmd_callback(self, msg):
        cmd = msg.data
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

def main():
    rclpy.init()
    node = MotorControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
