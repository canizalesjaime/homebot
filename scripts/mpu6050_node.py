# mpu6050 GY-521 Module
# right-hand rule. from inputs to chip(is postive  x-axis)
# gyroscrope computes the change in angular velocity
# accelerometer computes acceleration(rate of change in velocity) 

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Header
from mpu6050 import mpu6050
import math

class Mpu6050Node(Node):
    def __init__(self):
        super().__init__('mpu6050_node')

        self.sensor = mpu6050(0x68)

        self.imu_pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.temp_pub = self.create_publisher(Temperature, 'imu/temperature', 10)

        self.timer = self.create_timer(1.0, self.publish_sensor_data)

        self.get_logger().info("MPU6050 node started.")


    def get_roll_pitch(self, accel):
        ax = accel['x']
        ay = accel['y']
        az = accel['z']

        # Convert to roll and pitch (in degrees)
        roll  = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

        return roll, pitch
    
    def publish_sensor_data(self):
        accel = self.sensor.get_accel_data()
        gyro = self.sensor.get_gyro_data()
        temp = self.sensor.get_temp()

        print("Accelerometer data:", accel)
        print("Gyroscope data:", gyro)
        print("Temp:", temp)
        roll, pitch = self.get_roll_pitch(accel)
        print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°")

        # Populate IMU message
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = "imu_link"

        imu_msg.linear_acceleration.x = accel['x'] * 9.80665  # g to m/s^2
        imu_msg.linear_acceleration.y = accel['y'] * 9.80665
        imu_msg.linear_acceleration.z = accel['z'] * 9.80665

        imu_msg.angular_velocity.x = math.radians(gyro['x'])  # deg/s to rad/s
        imu_msg.angular_velocity.y = math.radians(gyro['y'])
        imu_msg.angular_velocity.z = math.radians(gyro['z'])

        # Optionally set covariance if known (identity = unknown)
        imu_msg.linear_acceleration_covariance[0] = -1.0
        imu_msg.angular_velocity_covariance[0] = -1.0

        self.imu_pub.publish(imu_msg)

        # Publish temperature
        temp_msg = Temperature()
        temp_msg.header = imu_msg.header
        temp_msg.temperature = temp
        self.temp_pub.publish(temp_msg)



def main(args=None):
    rclpy.init(args=args)
    node = Mpu6050Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
