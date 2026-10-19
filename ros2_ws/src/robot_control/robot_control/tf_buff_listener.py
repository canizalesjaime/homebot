import numpy as np

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from tf_transformations import quaternion_matrix

class trans(Node):
    def __init__(self):
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def p_0_i(self, frame_i):
        frame_0='world'# reference frame is 0, end effector frame is i
        frame_i=frame_i[:-5]+"link"
        t=self.tf_buffer.lookup_transform(frame_0,frame_i,rclpy.time.Time())
        return np.array([t.transform.translation.x,
                         t.transform.translation.y,
                         t.transform.translation.z])


    def a_0_i(self,frame_i):
        #reference frame is 0, end effector frame is i,a_i^0={}^0R_i,a_i^{local}}
        frame_0='world'
        frame_i_link=frame_i[:-5]+"link"
        t=self.tf_buffer.lookup_transform(frame_0,frame_i_link,rclpy.time.Time())
        q=t.transform.rotation
        r = quaternion_matrix([q.x, q.y, q.z, q.w])[:3, :3]
        return r @ np.array(self.joints[frame_i])


    def old_jacobian(self):
        j = []
        p_i_list=np.array([self.p_0_i(joint) for joint in self.joints.keys()])
        p_e=p_i_list[-1]
        a_i_list=np.array([self.a_0_i(joint) for joint in self.joints.keys()])
        
        for i in range(len(self.joints)):
            j.append(np.cross(a_i_list[i],p_e-p_i_list[i]))

        j = np.column_stack(j)
        j = np.vstack((j, a_i_list.T))
        return j