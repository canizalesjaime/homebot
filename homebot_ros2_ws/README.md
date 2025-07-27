# home_bot
* keep messing around with the frequency and duty_us for turning, find best values for l298n, then update motor control node, or add two more motors
* Make website(react): Add bio and teaching, stream video, control bot, gui for orientation(start with ros2 rviz) add flutter app?
* Add some ml with pytorch course(make an unsupervised grasping model?) and simple vision like yolo
* segmentation, stereo camera or ultrasound slam for 3d stuff
* add infared sensor to follow motion, and accelerometer, to arm
* ros open source
* add camera in ros2 to docker bot(still debugging) check the c++ camera packages
* tmux and neovim for better performance outside vscode
* solve power bank issue for pi 5
* build better base for robot with 3d printer
* make urdf file for homebot and arm, use dht table for arm frames
* make a 3d printed drone
* touch keyboard app for kubuntu
* design your own arm 
* fix tennis navigation
* try networking between computer, arm, and mini bot use ros_ip. Look into networking and firewalls
* autocad or freecad for designing


## steps to start
1. cd /workspaces/robotics/ros2_ws
2. colcon build
3. source install/setup.bash
4. ros2 run robot_control \<executable_name\>
5. ros2 launch robot_control \<executable_name\>
6. ros2 service call /capture_image std_srvs/srv/Trigger
7. xhost +local:root and xhost -local:root for rviz2
8. ros2 launch my_robot_description display.launch.py
