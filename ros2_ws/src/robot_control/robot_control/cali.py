import math

#central_axis, shoulder, elbow, wrist, gripper1, gripper2(10 is open)
offset =  [-1,.3,2,1.34,1,0]#offset at 10 degrees for each joint
direction = [1, 1, -1, -1, -1, 1]


def convert_viz2real_angles(viz_angs_rads):
    real_angs_rads=[0,0,0,0,0,0]
    for i, ang in enumerate(viz_angs_rads):
        real_angs_rads[i]=math.radians(10)+direction[i]*(ang-offset[i])
    return real_angs_rads


def convert_real2viz_angles(real_angs_deg):
    viz_angs_rads=[0,0,0,0,0,0]
    for i, ang in enumerate(real_angs_deg):
        viz_angs_rads[i]=direction[i]*math.radians(ang-10)+offset[i]
    return viz_angs_rads