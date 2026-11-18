import math
import time
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.action import ActionServer, CancelResponse, GoalResponse


import robot_control.paths
from robot_control.kinematics_math import load_kinematic_chain,inverse_kinematics_position, get_joint_limits
from arm import Arm 
from robot_interfaces.action import MoveArm
from robot_interfaces.srv import CalculateIK

from robot_control.cali import convert_viz2real_angles, convert_real2viz_angles


class ArmNode(Node):
    def __init__(self):
        super().__init__('arm_node')
        
        self.joint_pub = self.create_publisher(JointState,"/joint_states",10)

        self.joints = {"central_axis_joint":[0,0,1], # joint name, axis of rotation
                       "shoulder_joint":[0,1,0],
                       "elbow_joint":[0,1,0],
                       "wrist_joint":[1,0,0],
                       "gripper1_joint":[0,0,1],
                       "gripper2_joint":[1,0,0]}
        
        self.declare_parameter("simulate", True)
        self.simulate = self.get_parameter("simulate").value
        self.arm = Arm("big", simulate=self.simulate)
        self.get_logger().info(f"Arm mode: {'SIMULATION' if self.simulate else 'HARDWARE'}")

        self.curr_angles= [ang[1][1] for ang in self.arm.get_servo_angles().items()]
        self.timer = self.create_timer(0.05,self.publish_joint_states) #20hz
        self.kinematic_chain=load_kinematic_chain("/workspaces/homebot/ros2_ws/src/arm_description/urdf/arm.urdf.xacro")

        self.move_arm_server = ActionServer(self,MoveArm,'move_arm',
            execute_callback=self.execute_move_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

        self.ik_service = self.create_service(CalculateIK,'calculate_ik',self.ik_callback)

        urdf_lower, urdf_upper = get_joint_limits(self.kinematic_chain)

        servo_lower = np.array(convert_real2viz_angles([10] * 6))

        servo_upper = np.array(convert_real2viz_angles([170] * 6))

        physical_lower = np.minimum(servo_lower, servo_upper)
        physical_upper = np.maximum(servo_lower, servo_upper)

        self.lower_limits = np.maximum(urdf_lower, physical_lower)
        self.upper_limits = np.minimum(urdf_upper, physical_upper)

        if np.any(self.lower_limits >= self.upper_limits):
            raise ValueError("URDF and physical servo limits are incompatible")


    # Action server callbacks
    def goal_callback(self, goal_request):
        if len(goal_request.angles) != 6:
            self.get_logger().warn("Expected exactly 6 angles")
            return GoalResponse.REJECT

        return GoalResponse.ACCEPT


    def cancel_callback(self, goal_handle):
        return CancelResponse.REJECT


    def execute_move_callback(self, goal_handle):
        goal_angles = list(goal_handle.request.angles)
        self.get_logger().info(f"Moving arm to {goal_angles}")
        result = MoveArm.Result()

        try:
            self.move_smooth(goal_angles, goal_handle)
            goal_handle.succeed()
            result.success = True
            result.message = "Arm movement completed"
        except Exception as e:
            goal_handle.abort()
            result.success = False
            result.message = str(e)

        return result


    def move_smooth(self, goal_angles_deg, goal_handle=None):
        curr_angles_deg=self.arm.get_servo_angles()
        step=2

        # Calculate total number of movement steps
        total_steps = 0
        for i, joint in enumerate(curr_angles_deg):
            curr_angle = curr_angles_deg[joint][1]
            end_angle = goal_angles_deg[i]
            total_steps += len(range(curr_angle,
                end_angle + 1 if curr_angle < end_angle else end_angle - 1,
                step if curr_angle < end_angle else -step))

        completed_steps = 0

        for i,joint in enumerate(curr_angles_deg):
            curr_angle=curr_angles_deg[joint][1]
            end_angle=goal_angles_deg[i]
            if curr_angle < end_angle:
                rng = range(curr_angle, end_angle + 1, step)
            else:
                rng = range(curr_angle, end_angle - 1, -step)

            for angle in rng:
                self.arm.set_servo_angle(joint, angle)
                self.curr_angles[i]=angle
                time.sleep(0.02)

                completed_steps += 1

                if goal_handle is not None:
                    feedback = MoveArm.Feedback()
                    feedback.progress = float(completed_steps/total_steps*100.0)
                    goal_handle.publish_feedback(feedback)

        self.curr_angles=[ang[1][1] for ang in self.arm.get_servo_angles().items()]
    

    def publish_joint_states(self):       
        arm_msg = JointState()
        arm_msg.header.stamp = self.get_clock().now().to_msg()
        arm_msg.name = list(self.joints)
        arm_msg.position = convert_real2viz_angles(self.curr_angles)        
        self.joint_pub.publish(arm_msg)  


    def ik_callback(self, request, response):
        p_desired = np.array([request.x,request.y,request.z], dtype=float)

        try:
            q_curr = convert_real2viz_angles(self.curr_angles)

            # Calculate IK with joint limits.,Returns URDF joint angles in radians, or None.
            solution_viz = inverse_kinematics_position(q_curr,p_desired,self.kinematic_chain,self.lower_limits,self.upper_limits)

            if solution_viz is None:
                response.success = False
                response.joint_angles = []
                response.message = "No valid IK solution found"
                return response

            # Convert URDF joint angles to physical servo angles.
            # Result is still in radians.
            solution_real = convert_viz2real_angles(solution_viz)

            # Final safety check using physical servo limits.
            lower = math.radians(10)
            upper = math.radians(170)
            eps = 1e-6

            if any(
                not math.isfinite(angle)
                or angle < lower - eps
                or angle > upper + eps
                for angle in solution_real
            ):
                response.success = False
                response.joint_angles = []
                response.message = "IK solution violates servo limits"
                return response

            print("IK solution (servo radians):", solution_real)

            response.success = True
            response.joint_angles = [float(q) for q in solution_real]
            response.message = "IK solution calculated"

        except Exception as e:
            response.success = False
            response.joint_angles = []
            response.message = str(e)

        return response

        
    def destroy_node(self):
        super().destroy_node()
        self.get_logger().info('Servo Controller Node stopped and GPIO released.')


def main(args=None):
    rclpy.init(args=args)
    node = ArmNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
