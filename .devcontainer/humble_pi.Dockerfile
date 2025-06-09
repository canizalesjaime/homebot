FROM arm64v8/debian:bookworm

# Set locale and time zone
RUN apt update && apt install -y locales tzdata && \
    locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install lgpio and build tools
RUN apt update && apt install -y \
    lgpio-dev \
    build-essential \
    cmake \
    git \
    wget \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    libpython3-dev \
    libyaml-dev

# Initialize rosdep
RUN rosdep init && rosdep update

# Set up ROS 2 workspace
WORKDIR /opt/ros2_ws
RUN git clone https://github.com/ros2/ros2.git -b humble .

RUN ./src/ros2/scripts/rosinstall_generator.py \
    ros_base --rosdistro humble --deps --tar > humble.rosinstall && \
    vcs import src < humble.rosinstall

# Install ROS 2 dependencies
RUN rosdep install --from-paths src --ignore-src --rosdistro humble -y

# Build ROS 2
RUN colcon build --symlink-install

# Source environment
ENV ROS_DISTRO=humble
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros2_ws/install/setup.bash" >> ~/.bashrc
