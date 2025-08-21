# To Do
1. convert FROM l298n motor driver to tb6612 motor driver 
2. autocad or freecad for designing: drone, arm, homebot base, pcb board 
3. Finish website: Add bio and teaching, add flutter app?
4. Add some ml with pytorch course(make an unsupervised grasping model?) and simple vision like yolo
5. automate git push for ci/cd  
6. add camera in ros2 to docker bot(still debugging) check the c++ camera packages
7. make urdf file for homebot and arm, use dht table for arm frames 
8. fix tennis navigation
9. try networking between computer, arm, and mini bot use ros_ip. Look into networking and firewalls. add arm to ros2 setup to check comm(understand rotations and pick up hacky sack ball) 
10. separate git for robot? (Upload vid.) arm pic, servo specs 
11. add infared sensor to follow motion, and accelerometer, to arm
12. tmux and neovim for better performance outside vscode
13. segmentation, stereo camera or ultrasound slam for 3d stuff 
14. touch keyboard app for kubuntu
15. ros open source
16. build computer


## steps to start
1. ros2 run robot_control \<executable_name\>
2. ros2 launch robot_control \<executable_name\>
3. ros2 service call /capture_image std_srvs/srv/Trigger
4. xhost +local:root and xhost -local:root for rviz2
5. ros2 launch my_robot_description display.launch.py

## useful commands
* docker rmi $(docker images -q)

