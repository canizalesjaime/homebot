import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class ArmTeleopNode(Node):
    def __init__(self):
        super().__init__('arm_teleop_node')
        self.angles_pub = self.create_publisher(Int32MultiArray,'cmd_arm', 10)
        #self.timer = self.create_timer(1.0, self.publish_angles)

          
    def publish_angles(self):
        angles=int(input("Enter angle: "))
        msg = Int32MultiArray()
        msg.data=[angles for i in range(6)]
        #msg.data=[int(angle) for angle in angles.split(',')]
        if len(msg.data) == 6:
            self.angles_pub.publish(msg)
   

def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleopNode()

    try:
        #rclpy.spin(node)
        while(True):
            node.publish_angles()

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
