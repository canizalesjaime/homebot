from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_control',
            executable='ultrasound',
            name='u',
            output='screen',
        ),
        # Node(
        #     package='robot_control',
        #     executable='teleop',
        #     name='t'
        # ),
        Node(
            package='robot_control',
            executable='motor',
            name='m'
        ),
            ]
        )