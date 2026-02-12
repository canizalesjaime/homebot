# mpu6050 GY-521 Module
# right-hand rule. Z is thumb, Y is toward VCC
# gyroscrope computes the change in angular velocity
# accelerometer computes acceleration(rate of change in velocity)
# 
# ADD TO WEBSITE 
 
from mpu6050 import mpu6050
import math

class Mpu6050Node():
    def __init__(self):
        self.sensor = mpu6050(0x68)


    def get_roll_pitch(self, accel):
        ax = accel['x']
        ay = accel['y']
        az = accel['z']

        # Convert to roll and pitch (in degrees)
        roll  = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

        return roll, pitch
    
    def sensor_data(self):
        accel = self.sensor.get_accel_data()
        gyro = self.sensor.get_gyro_data()
        temp = self.sensor.get_temp()

        print("Accelerometer data:", accel)
        print("Gyroscope data:", gyro)
        print("Temp:", temp)
        roll, pitch = self.get_roll_pitch(accel)
        print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°")

       

        print("linear_acceleration.x: ", accel['x'] * 9.80665)  # g to m/s^2
        print("linear_acceleration.y: ", accel['y'] * 9.80665)
        print("linear_acceleration.z: ", accel['z'] * 9.80665)

        print("angular_velocity.x: ", math.radians(gyro['x']))  # deg/s to rad/s
        print("angular_velocity.y: ", math.radians(gyro['y']))
        print("angular_velocity.z: ", math.radians(gyro['z']))

        # Optionally set covariance if known (identity = unknown)
        # linear_acceleration_covariance[0] = -1.0
        # angular_velocity_covariance[0] = -1.0

        # Publish temperature
        print("Temperature: ", temp)
        

def main(args=None):
    try:
        node = Mpu6050Node()
        while(True):
            node.sensor_data()
    except KeyboardInterrupt:
        pass
#    finally:
#main()
