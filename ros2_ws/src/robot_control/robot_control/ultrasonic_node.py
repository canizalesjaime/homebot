import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import lgpio as GPIO
import time

TRIG = 5
ECHO = 6

class UltrasonicNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_node')
        self.publisher_ = self.create_publisher(Float32, 'distance', 10)
        self.timer = self.create_timer(0.2, self.timer_callback)
        self.h = GPIO.gpiochip_open(0)
        GPIO.gpio_claim_output(self.h, TRIG)
        GPIO.gpio_claim_input(self.h, ECHO)

    def timer_callback(self):
        dist = self.get_distance()
        print(dist)
        msg = Float32()
        msg.data = dist
        self.publisher_.publish(msg)

    def get_distance(self):
        GPIO.gpio_write(self.h, TRIG, 0)
        time.sleep(0.0002)
        GPIO.gpio_write(self.h, TRIG, 1)
        time.sleep(0.00001)
        GPIO.gpio_write(self.h, TRIG, 0)

        start = time.time()
        while GPIO.gpio_read(self.h, ECHO) == 0:
            start = time.time()
        while GPIO.gpio_read(self.h, ECHO) == 1:
            end = time.time()

        duration = end - start
        distance_cm = duration * 17150
        return round(distance_cm / 2.54, 2)  # inches

def main():
    rclpy.init()
    node = UltrasonicNode()
    rclpy.spin(node)
    GPIO.gpiochip_close(node.h)
    node.destroy_node()
    rclpy.shutdown()
