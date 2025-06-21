FROM ros:jazzy

RUN apt update && apt upgrade -y
RUN apt install -y \
 python3-lgpio \
 gpiod \
 libgpiod-dev \
 python3-libgpiod \
 ros-jazzy-cv-bridge \
 python3-opencv \
 python3-pip \
 python3-smbus \
 i2c-tools \
 libcap-dev\
 libcamera-dev \
 libcamera-tools  \
 python3-libcamera \
 python3-pyqt6
RUN pip3 install mpu6050-raspberrypi --break-system-packages
RUN pip3 install picamera --break-system-packages
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /workspaces/robotics/homebot_ros2_ws/install/setup.bash" >> ~/.bashrc



# RUN sudo apt install python3.10-venv python3.10-distutils
# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.10
# RUN python3.10 -m pip install picamera2 --break-system-packages