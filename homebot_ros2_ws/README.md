# To Do
1. homebot: urdf file, setup tb6612 motor driver, add yolo, fix tennis navigation, add camera in ros2 to docker, check the c++ camera packages, CSI camera support in Docker is tricky; often easier to stream the camera via host and have the ROS node access /dev/video0 inside the container. segmentation, stereo camera, ultrasound slam, lidar slam for 3d stuff 
2. autocad or freecad for designing: drone, optimal homebot base, pcb board 
3. House keeping: Finish website-Add bio and teaching, add flutter app, automate git push for ci/cd, aws? separate git for robot? Upload vid, arm pic, servo specs,  add notes for electronics
4. arm: urdf file, dht table for arm frames, add infared sensor to follow motion, and accelerometer, add to ros2 setup to check comm, understand rotations to pick up hacky sack ball, using pytorch course make an unsupervised grasping model, use jetson orin(check out study material on nvidia)
5. try networking between computer, arm, and homebot use ros_ip. Look into networking and firewalls.    
6. tmux and neovim for better performance outside vscode
7. touch keyboard app for kubuntu
8. contribute to ros open source



## steps to start
1. ros2 run robot_control \<executable_name\>
2. ros2 launch robot_control \<executable_name\>
3. ros2 service call /capture_image std_srvs/srv/Trigger
4. xhost +local:root and xhost -local:root for rviz2
5. ros2 launch my_robot_description display.launch.py

## useful commands
* docker rmi $(docker images -q)

