import serial


class LunarNode():
    def __init__(self):
        self.ser = serial.Serial("/dev/serial0", 115200, timeout=1)
        print("Reading TF-Luna data...")

    def get_distance(self):
        print(self.ser.in_waiting)
        while self.ser.in_waiting >= 9:
            data = self.ser.read(9)
            if self.ser.read(1)[0] ==0x59:
                if self.ser.read(1)[0]==0x59:
                    data=self.ser.read(7)
                    distance=data[0]+data[1]*256
                    return distance
            # TF-Luna frame starts with 0x59 0x59
            #if data[0] == 0x59 and data[1] == 0x59:
            #    distance = data[2] + data[3] * 256
            #    strength = data[4] + data[5] * 256
                
            return None # in cm


def main():
    node = LunarNode()
    try:
        while(True):
            d=node.get_distance()
            if d!=None:
                print(d)

    except KeyboardInterrupt:
        print("\nExiting...")
    
    # finally:
    #     node.free_gpio()

main()
