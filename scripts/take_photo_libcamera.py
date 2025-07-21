from picamera2 import Picamera2, Preview
from time import sleep

picam2 = Picamera2()

# Set up the configuration once
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

def live_video():
    picam2.start_preview(Preview.QTGL)  # Show video window (requires X11)
    picam2.start()
    sleep(5)
    picam2.stop_preview()
    picam2.stop()

def capture_image():
    picam2.start()
    sleep(2)  # Let camera warm up
    picam2.capture_file("test_image.jpg")
    picam2.stop()

capture_image()
picam2.close()
