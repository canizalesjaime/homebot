import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from arm_interfaces.srv import SetArmAngles


class ArmTeleopNode(Node):
    def __init__(self):
        super().__init__('arm_teleop_node')
        #self.angles_pub = self.create_publisher(Int32MultiArray,'cmd_arm', 10)
        
        self.client = self.create_client(SetArmAngles,'set_arm_angles')      
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for arm service...')


    def send_angles(self):
        angles = int(input("Enter angle: "))
        request = SetArmAngles.Request()
        request.angles = [angles for _ in range(6)]
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        if response is not None:
            print("Success:", response.success)
            print("Message:", response.message)
        else:
            self.get_logger().error(f'Service call failed: {future.exception()}')


def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleopNode()

    try:
        while rclpy.ok():
            node.send_angles()

    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
