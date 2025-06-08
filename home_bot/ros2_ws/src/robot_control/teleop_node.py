# robot_control/teleop_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
import curses

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.cmd_pub = self.create_publisher(String, 'cmd_motor', 10)
        self.distance = 100.0
        self.create_subscription(Float32, 'distance', self.distance_callback, 10)

    def distance_callback(self, msg):
        self.distance = msg.data

    def control_loop(self, stdscr):
        stdscr.nodelay(True)
        stdscr.addstr(0, 0, "Hold 'a' to move forward, 'z' backward, 'x' to stop. Ctrl+C to exit.")
        current_action = None

        while True:
            try:
                key = stdscr.getch()
                if key == ord('a') and self.distance > 8.0:
                    self.cmd_pub.publish(String(data='forward'))
                    current_action = 'forward'
                elif key == ord('z'):
                    self.cmd_pub.publish(String(data='backward'))
                    current_action = 'backward'
                elif key == ord('x') or key == -1:
                    if current_action:
                        self.cmd_pub.publish(String(data='stop'))
                        current_action = None
                stdscr.refresh()
            except KeyboardInterrupt:
                break

def main():
    rclpy.init()
    node = TeleopNode()
    curses.wrapper(node.control_loop)
    node.destroy_node()
    rclpy.shutdown()
