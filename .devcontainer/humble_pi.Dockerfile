FROM ros:jazzy


RUN apt update && apt upgrade -y
RUN apt install python3-lgpio -y
RUN apt install -y gpiod libgpiod-dev python3-libgpiod


# RUN source /opt/ros/jazzy/setup.bash && \
# mkdir -p ~/ros2_ws/src/ && \
# cd ~/ros2_ws && \
# colcon build && \
# echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /workspaces/robotics/home_bot/ros2_ws/install/setup.bash" >> ~/.bashrc

## steps to start
# 1. cd /workspaces/robotics/home_bot/ros2_ws
# 2. colcon build
# 3. source install/setup.bash
# 4. ros2 run robot_control <executable_name> #in setup.py for executable name 
