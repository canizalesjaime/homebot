#ros2 topic pub /servo_angles std_msgs/Int32MultiArray "data: [90, 90, 90, 90]"
import math
import time
import numpy as np

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import JointState
from tf2_ros import Buffer, TransformListener

import robot_control.paths
from arm import ArmNode 

class ArmRos(Node):
    def __init__(self):
        super().__init__('arm_ros')
        self.angle_sub = self.create_subscription(Int32MultiArray,'cmd_arm',
                                                  self.angle_callback, 10)
        
        self.joint_pub = self.create_publisher(JointState,"/joint_states",10)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.joints = {"base_joint":[0,0,1], # joint name, axis of rotation
                       "shoulder_joint":[0,1,0],
                       "elbow_joint":[0,1,0],
                       "wrist_joint":[1,0,0],
                       "gripper1_joint":[0,0,1],
                       "gripper2_joint":[1,0,0]}
        self.arm = ArmNode("big")
        self.arm_msg([90,90,90,90,90,90]) # start position


    def move_smooth(self, goal_angles_deg):
        curr_angles_deg=self.arm.get_servo_angles()
        step=2
        for i,joint in enumerate(curr_angles_deg):
            curr_angle=curr_angles_deg[joint][1]
            end_angle=goal_angles_deg[i]
            if curr_angle < end_angle:
                rng = range(curr_angle, end_angle + 1, step)
            else:
                rng = range(curr_angle, end_angle - 1, -step)

            for angle in rng:
                self.arm.set_servo_angle(joint, angle)
                self.arm_msg(goal_angles_deg)
                time.sleep(0.02)
        
    
    def arm_msg(self, angles_deg):       
        arm_msg = JointState()
        arm_msg.header.stamp = self.get_clock().now().to_msg()
        arm_msg.name = self.joints.keys
        arm_msg.position = [math.radians(i) for i in angles_deg]
        self.joint_pub.publish(arm_msg)  


    def angle_callback(self, msg):
        self.move_smooth(msg.data)


    def inverse_kinematics_position(self, p_desired):
        J=self.jacobian()


    def p_0_i(self, frame_i):
        frame_0='world'# reference frame is 0, end effector frame is i
        t=self.tf_buffer.lookup_transform(frame_0,frame_i,rclpy.time.Time())
        return [t.transform.translation.x,t.translation.y,t.transform.translation.z]


    def a_0_i(self,frame_i):
        frame_0='world'# reference frame is 0, end effector frame is i
        #a_i^0 = {}^0R_i,a_i^{local}}
        t=self.tf_buffer.lookup_transform(frame_0,frame_i,rclpy.time.Time())
        r=t.transform.rotation
        return r @ self.joints[frame_i]


    def jacobian(self):
        p_i_list=[self.p_0_i(joint) for joint in self.joints.keys]
        p_e=p_i_list[-1]

        a_i_list=[self.a_0_i(joint) for joint in self.joints.keys]

        j = [np.cross(a_i_list[i],p_e-p_i_list[i]) for i in range(len(self.joints))]
        # somehow stack j ontop of a_i_list like an sql union

        
    def destroy_node(self):
        super().destroy_node()
        self.get_logger().info('Servo Controller Node stopped and GPIO released.')



def main(args=None):
    rclpy.init(args=args)
    node = ArmRos()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
