import serial

# Open UART (Pi 4 default)
ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

print("Reading TF-Luna data...")

while True:
    if ser.in_waiting >= 9:
        data = ser.read(9)
        
        # TF-Luna frame starts with 0x59 0x59
        if data[0] == 0x59 and data[1] == 0x59:
            distance = data[2] + data[3] * 256
            strength = data[4] + data[5] * 256
            
            print(f"Distance: {distance} cm | Strength: {strength}")
