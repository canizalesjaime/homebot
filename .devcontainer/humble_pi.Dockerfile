FROM jaimec21/jazzy_pi:latest
# FROM ros:jazzy

# RUN apt-get update && apt-get install -y \
#     ros-jazzy-rviz2 \
#     ros-jazzy-joint-state-publisher-gui \
#     ros-jazzy-xacro \
#     x11-apps \
#     && rm -rf /var/lib/apt/lists/*

# RUN apt update && apt upgrade -y
# RUN apt install -y \
#  python3-lgpio \
#  gpiod \
#  libgpiod-dev \
#  python3-libgpiod \
#  ros-jazzy-cv-bridge \
#  python3-opencv \
#  python3-pip \
#  python3-smbus \
#  i2c-tools \
#  libcap-dev\
#  libcamera-dev \
#  libcamera-tools  \
#  python3-libcamera \
#  python3-pyqt6
# RUN pip3 install mpu6050-raspberrypi picamera2 --break-system-packages
# RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
# RUN echo "source /workspaces/robotics/homebot_ros2_ws/install/setup.bash" >> ~/.bashrc
