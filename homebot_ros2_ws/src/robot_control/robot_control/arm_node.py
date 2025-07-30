import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import pigpio

class ServoController(Node):
    def __init__(self):
        super().__init__('servo_controller')
        self.subscription = self.create_subscription(
            Int32MultiArray,
            'servo_angles',  # Topic name
            self.listener_callback,
            10
        )

        self.pi = pigpio.pi()
        self.motor_map = {
            "base": 14,
            "shoulder": 18,
            "elbow": 25,
            "gripper": 12
        }

        self.get_logger().info('Servo Controller Node has started.')

    def degrees_to_pulse(self, deg):
        if not 0 <= deg <= 180:
            raise ValueError("angle must be between 0 and 180")
        return int(500 + (deg / 180) * 2000)

    def listener_callback(self, msg):
        try:
            angles = msg.data
            if len(angles) != 4:
                self.get_logger().warn('Expected 4 angles [base, shoulder, elbow, gripper], got {}'.format(len(angles)))
                return

            for angle, joint in zip(angles, self.motor_map):
                gpio_pin = self.motor_map[joint]
                pulse = self.degrees_to_pulse(angle)
                self.pi.set_servo_pulsewidth(gpio_pin, pulse)

            self.get_logger().info(f'Updated servos to angles: {angles}')
        except Exception as e:
            self.get_logger().error(f"Failed to move servos: {e}")

    def destroy_node(self):
        super().destroy_node()
        for pin in self.motor_map.values():
            self.pi.set_servo_pulsewidth(pin, 0)
        self.pi.stop()
        self.get_logger().info('Servo Controller Node stopped and GPIO released.')

def main(args=None):
    rclpy.init(args=args)
    node = ServoController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
