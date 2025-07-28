## Ultrasonic HCSR04
* VCC -> PIN 2(5V)
* TRIG -> PIN 29 (GPIO 5)
* ECHO -> PIN 31 (GPIO 6) with voltage divider
* GND -> PIN 39 (GND)


## Accelerometer MPU6050 
* VCC -> PIN 1 (3.3V)
* GND -> PIN 6 (GND)
* SCL -> PIN 5 (GPIO 3 SCL)(I^2C)
* SDA -> PIN 3 (GPIO 2 SDA)(I^2C)


## L298N Motor Drvier 1
* GND -> LIPO Battery and PIN 34 (GND)
* +12V -> LIPO Battery
* ENA -> PIN 7(GPIO 4)
* IN1 -> PIN 11 (GPIO 17)
* IN2 -> PIN 13 (GPIO 27)
* IN3 -> PIN 16 (GPIO 23)
* IN4 -> PIN 18 (GPIO 24)
* ENB -> PIN 37 (GPIO 26)
* OUT1 -> LEFT MOTOR
* OUT2 -> LEFT MOTOR
* OUT3 -> RIGHT MOTOR
* OUT4 -> RIGHT MOTOR

## L298N Motor Drvier 2
* GND -> LIPO Battery and PIN 20 (GND)
* +12V -> LIPO Battery
* ENA -> PIN 22(GPIO 25)
* IN1 -> PIN 36 (GPIO 16)
* IN2 -> PIN 13 (GPIO 33)
* IN3 -> PIN 15 (GPIO 22)
* IN4 -> PIN 34 (GPIO 12)
* ENB -> PIN 8 (GPIO 14)
* OUT1 -> LEFT MOTOR
* OUT2 -> LEFT MOTOR
* OUT3 -> RIGHT MOTOR
* OUT4 -> RIGHT MOTOR
