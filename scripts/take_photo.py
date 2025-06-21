import cv2
import time

# Open the default camera (usually /dev/video0)
cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)


if not cap.isOpened():
    print("❌ Failed to open camera.")
else:
    ret, frame = cap.read()
    if ret:
        filename = f"snapshot_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Saved image as {filename}")
    else:
        print("⚠️ Failed to capture image.")

cap.release()