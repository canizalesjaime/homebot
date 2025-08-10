# To Do
* Make website(react): Add bio and teaching, stream video, control bot, gui for orientation(start with ros2 rviz) add flutter app?
* Add some ml with pytorch course(make an unsupervised grasping model?) and simple vision like yolo
* segmentation, stereo camera or ultrasound slam for 3d stuff
* add infared sensor to follow motion, and accelerometer, to arm
* ros open source
* add camera in ros2 to docker bot(still debugging) check the c++ camera packages
* tmux and neovim for better performance outside vscode
* make urdf file for homebot and arm, use dht table for arm frames
* touch keyboard app for kubuntu
* fix tennis navigation
* try networking between computer, arm, and mini bot use ros_ip. Look into networking and firewalls. add arm to ros2 setup to check comm(understand rotations and pick up hacky sack ball)
* autocad or freecad for designing: drone, arm, homebot base, pcb board
* separate git for robot? (Upload vid.) arm pic, servo specs 
* convert FROM l298n motor driver to tb6612 motor driver
* automate git push for ci/cd


## steps to start
1. ros2 run robot_control \<executable_name\>
2. ros2 launch robot_control \<executable_name\>
3. ros2 service call /capture_image std_srvs/srv/Trigger
4. xhost +local:root and xhost -local:root for rviz2
5. ros2 launch my_robot_description display.launch.py

## useful commands
1. docker rmi $(docker images -q)

