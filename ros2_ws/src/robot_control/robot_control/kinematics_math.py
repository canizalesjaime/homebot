import np
import xacro
import xml.etree.ElementTree as ET

def load_kinematic_chain(urdf_path):
    """Load the ordered world-to-end-effector joint chain from urdf file."""
    #root = ET.parse(urdf_path).getroot()
    #root = xacro.process_file(urdf_path).documentElement
    root = ET.fromstring(xacro.process_file(urdf_path).toxml())

    joints_by_child = {}

    for joint in root.findall("joint"):
        child = joint.find("child").get("link")
        joints_by_child[child] = joint

    chain = []
    link = "gripper2_link"

    while link != "world":
        if link not in joints_by_child:
            raise ValueError(f"No joint connects {link} toward world")

        joint = joints_by_child[link]
        chain.append(joint)
        link = joint.find("parent").get("link")

    return list(reversed(chain))


def jacobian(q):
    p_i_list=np.array([self.p_0_i(joint) for joint in self.joints.keys()])
    p_e=p_i_list[-1]
    
    a_i_list=np.array([self.a_0_i(joint) for joint in self.joints.keys()])
    
    j = []
    for i in range(len(self.joints)):
        j.append(np.cross(a_i_list[i],p_e-p_i_list[i]))

    j = np.column_stack(j)
    j = np.vstack((j, a_i_list.T))
    return j


def make_transform(xyz, rpy):
    """Create a 4x4 transformation from URDF xyz and rpy."""
    roll, pitch, yaw = rpy

    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)

    Rx = np.array([
        [1, 0, 0],
        [0, cr, -sr],
        [0, sr, cr]
    ])

    Ry = np.array([
        [cp, 0, sp],
        [0, 1, 0],
        [-sp, 0, cp]
    ])

    Rz = np.array([
        [cy, -sy, 0],
        [sy, cy, 0],
        [0, 0, 1]
    ])

    T = np.eye(4)
    T[:3, :3] = Rz @ Ry @ Rx
    T[:3, 3] = xyz

    return T


def axis_rotation(axis, angle):
        """Create a 4x4 rotation about an arbitrary joint axis."""
        axis = np.asarray(axis, dtype=float)
        axis = axis / np.linalg.norm(axis)

        x, y, z = axis
        c = np.cos(angle)
        s = np.sin(angle)
        v = 1 - c

        R = np.array([
            [c + x*x*v, x*y*v - z*s, x*z*v + y*s],
            [y*x*v + z*s, c + y*y*v, y*z*v - x*s],
            [z*x*v - y*s, z*y*v + x*s, c + z*z*v]
        ])

        T = np.eye(4)
        T[:3, :3] = R

        return T


def forward_kinematics(q):
    """Calculate world-to-gripper2_link transform for joint angles q."""
    T = np.eye(4)
    angle_index = 0

    for joint in self.kinematic_chain:
        origin = joint.find("origin")

        xyz = np.zeros(3)
        rpy = np.zeros(3)

        if origin is not None:
            xyz = np.fromstring(origin.get("xyz", "0 0 0"), sep=" ")
            rpy = np.fromstring(origin.get("rpy", "0 0 0"), sep=" ")

        T = T @ self.make_transform(xyz, rpy)

        joint_type = joint.get("type")

        if joint_type in ("revolute", "continuous"):
            axis_element = joint.find("axis")
            axis = np.array([1.0, 0.0, 0.0])

            if axis_element is not None:
                axis = np.fromstring(axis_element.get("xyz", "1 0 0"), sep=" ")

            if angle_index >= len(q):
                raise ValueError("Not enough joint angles")

            T = T @ self.axis_rotation(axis, q[angle_index])
            angle_index += 1

        elif joint_type != "fixed":
            raise NotImplementedError(f"Unsupported joint type: {joint_type}")

    if angle_index != len(q):
        raise ValueError(f"Expected {angle_index} joint angles, got {len(q)}")

    return T


def inverse_kinematics_position(p_desired):
    J = jacobian()
    p_curr = self.p_0_i("gripper2_joint")
    p_err = p_desired - p_curr
    J_v = J[:3, :6]
    delta_q = np.linalg.pinv(J_v) @ p_err
    alpha = 0.1
    q_curr = np.radians(np.array(self.curr_angles[:6], dtype=float))
    q_new = q_curr + alpha * delta_q

    # Test forward kinematics at the current configuration
    T = forward_kinematics(q_curr)
    p_fk = T[:3, 3]

    print("TF position:", p_curr)
    print("FK position:", p_fk)
    print("Difference:", np.linalg.norm(p_curr - p_fk))

    return q_new