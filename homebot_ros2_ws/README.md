# To Do
1. homebot: urdf file, fix tennis navigation, refactor new code to ros2, add camera in ros2 to docker, check the c++ camera packages, CSI camera support in Docker is tricky; often easier to stream the camera via host and have the ROS node access /dev/video0 inside the container. segmentation, stereo camera, lidar slam for 3d stuff  
2. House keeping: database for objects seen with dates(web dev course), print in autocad plexi connectors, connect i2c to powerboard for use by pca9865 and mpu6050, automate git push for ci/cd, aws? separate git for robot? add notes for electronics
3. arm: urdf file, dht table for arm frames, add infared sensor to follow motion, and accelerometer, add to ros2 setup to check comm, communicate with camera for grasping, using pytorch course make an unsupervised grasping model, use jetson orin(check out study material on nvidia(test with olama))
4. try networking between computer, arm, and homebot use ros_ip. Look into networking and firewalls and other security features.    


# later
1. tmux and neovim for better performance outside vscode
2. touch keyboard app for kubuntu
3. contribute to ros open source
4. add flutter app
5. autocad or freecad for designing: drone,  pcb board

## steps to start
1. cd /workspaces/robotics/homebot_ros2_ws && colcon build && source install/setup.bash
2. ros2 run robot_control \<executable_name\>
3. ros2 launch robot_control \<executable_name\>
4. ros2 service call /capture_image std_srvs/srv/Trigger
5. xhost +local:root and xhost -local:root for rviz2
6. ros2 launch my_robot_description display.launch.py

or 
1. docker build -f ./node_psql.Dockerfile -t ros2-setup .
2. docker run -it --rm \
  --init \
  --privileged \
  --net=host \
  --device=/dev/gpiomem \
  --device=/dev/mem \
  --device=/dev/ttyAMA0 \
  --cap-add=SYS_RAWIO \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /sys/class/gpio:/sys/class/gpio:cached \
  -v /dev:/dev \
  -v /run:/run \
  --name ros2-container \
  -v /c/Users/Caniz/repos/robotics:/workspace \
  jaimec21/robot-dashboard:latest \
  /bin/bash

