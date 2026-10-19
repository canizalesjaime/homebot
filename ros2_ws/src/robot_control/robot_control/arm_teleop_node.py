import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from robot_interfaces.srv import CalculateIK
from robot_interfaces.action import MoveArm


class ArmTeleopNode(Node):
    def __init__(self):
        super().__init__('arm_teleop_node')

        self.ik_client = self.create_client(CalculateIK, 'calculate_ik')

        self.move_client = ActionClient(self, MoveArm, 'move_arm')

        while not self.ik_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for IK service...')

        while not self.move_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for MoveArm action server...')


    def move_to_position(self):
        x = float(input("Enter x (meters): "))
        y = float(input("Enter y (meters): "))
        z = float(input("Enter z (meters): "))

        request = CalculateIK.Request()
        request.x = x
        request.y = y
        request.z = z

        future = self.ik_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        if response is None:
            self.get_logger().error(f'IK service failed: {future.exception()}')
            return

        if not response.success:
            self.get_logger().error(response.message)
            return

        angles_deg = [round(math.degrees(q))for q in response.joint_angles]

        print("IK solution (degrees):", angles_deg)

        # Validate against actual servo limits before moving
        if len(angles_deg) != 6:
            self.get_logger().error("Expected 6 joint angles")
            return

        # Assumes your servo and URDF angle conventions match
        # and all six servos accept commands between 0 and 180.
        # if any(angle < 0 or angle > 180 for angle in angles_deg):
        #     self.get_logger().error(f"IK solution outside servo limits: {angles_deg}")
        #     return

        confirmation = input("Move arm to these angles? [y/N]: ")
        if confirmation.strip().lower() != 'y':
            print("Movement cancelled")
            return

        # Send the angles to the MoveArm action server
        goal = MoveArm.Goal()
        goal.angles = angles_deg

        send_future = self.move_client.send_goal_async(goal,
            feedback_callback=self.feedback_callback)

        rclpy.spin_until_future_complete(self, send_future)

        goal_handle = send_future.result()

        if goal_handle is None:
            self.get_logger().error(f"Action goal failed: {send_future.exception()}")
            return

        if not goal_handle.accepted:
            self.get_logger().error("Movement goal rejected")
            return

        print("Movement goal accepted")

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result_response = result_future.result()

        if result_response is None:
            self.get_logger().error(f"Movement failed: {result_future.exception()}")
            return

        result = result_response.result

        print("Success:", result.success)
        print("Message:", result.message)

    def feedback_callback(self, feedback_msg):
        progress = feedback_msg.feedback.progress
        print(f"Movement progress: {progress:.1f}%")


def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleopNode()

    try:
        while rclpy.ok():
            node.move_to_position()

    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
