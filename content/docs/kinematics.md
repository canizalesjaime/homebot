# Forward Kinematics
Given the joint values (input)(angles or displacements), where is the end effector(output)?

${}^{0}T_{n}={}^{0}T_{1}\,{}^{1}T_{2}\,{}^{2}T_{3} \cdots {}^{n-1}T_{n}$

In other words, where is robot in 3d space give the joint angles?​

# Inverse Kinematics
Given the desired end effector pose, what joint values produce it?

${}^{0}T_{n}(\theta_1,\theta_2,\ldots,\theta_n)=T_{\text{desired}}$

command robot to move to Tdesired


## Forward Kinematics for homebot
Pretty much just the odometry computation. 
### Algorithm to get odometry
* Use encoders to count the ticks of tt motors
* According to documentation provided by manufacturer of the tt motors, 1080 ticks equals one full rotation(of the motor and therefore wheel) 
* Given the circumference of the wheel(can be obtained from radius = 0.0205 m), we can compute
the distance traveled by each wheel # of rotations times (distance covered by each wheel per rotaion=circumference)
* Assuming where ever the robot starts (its 6d pose) is the origin, we can compute the linear and angular
velocity of each wheel(radians per second), and convert that to the linear and angular velocity of the robot. Linear velocity of the robot is just the average velocity of the left and right wheel. The angular velocity is the ratio of the physical distance between the two wheels and the difference of the right and left wheel(since each reduces the others angular speed, and if equal no angular velocity).  
* Once we have the linear and angular velocity of the robot, we use eulers integration to obtain its (x,y,z) position and orientation, relative to whatever starting point(integrate because velocity is the derivative of position). Usually we do not consider its z position, because the robot is only moving along the xy plane(floor), and for the same reason with orientation, we only need the orientation angle along the z-axis. 
* In ros, you must assign a frequency(hz) to how often you update position and orientation based on algorithm above.


## Forward Kinematics(big arm)
### joint 1(base_link)
* wP1 - center of rotational plane of joint 1 = (40.35,103,92.75) (x,y,z)
* joint 1 is parallel to worlds xz plane

### joint 2(shoulder)
* joint 1 to joint 2: roll=0 pitch=90
* wP2 - center of rotational plane of joint 2 = (28.85, 161.45,92.87) (x,y,z)
* parallel to xy plane
* wP2 - wP1=(-11.50, 58.45,0) (in mm)
* using pythagoreas theorem, we get L12 = sqrt(-11.5^2+58.45^2+0^2)=59.57mm (I measured 60.325mm)

### joint 3(elbow)
* I need to measure from joint 2 to joint 3 in real world or rviz
* wP3 - ? 
* wP3 - wp1 ?

## fixing reference frame
* the stl files were drawn in a way that makes it seem like world frame has a roll of -90 degrees, 
but in reality its just that up is defined in the y direction of the arm.
* since this is the case, for simplicity we will make joint 1 the origin of frame {0}. joint 1 is located at wp1=(40.35,103,92.75), so for every other point we consider we must subtract wp1 from it.
* make physical up become $z_{\text{robot}}:$
$$
R_x(90^\circ)
=
\begin{bmatrix}
1&0&0\\
0&0&-1\\
0&1&0
\end{bmatrix}.
$$

* Some intuition on how the axes are beiong transformed: 
$$
\boxed{
\begin{aligned}
x_0 &= +x_{CAD}\\
y_0 &= -z_{CAD}\\
z_0 &= +y_{CAD}.
\end{aligned}}
$$

* final formula(applies to all points in cad): $P_{J1}^{robot}=R_x(90^\circ)\left(P_{J1}^{CAD}-P_{J1}^{CAD}\right)$