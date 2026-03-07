import serial


class LunarNode():
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
        print("Reading TF-Luna data...")

    def get_distance(self):
        if self.ser.in_waiting >= 9:
            data = self.ser.read(9)
            
            # TF-Luna frame starts with 0x59 0x59
            if data[0] == 0x59 and data[1] == 0x59:
                distance = data[2] + data[3] * 256
                strength = data[4] + data[5] * 256
                
            return distance # in cm


def main():
    node = LunarNode()
    try:
        while(True):
            print(node.get_distance())

    except KeyboardInterrupt:
        print("\nExiting...")
    
    # finally:
    #     node.free_gpio()

main()