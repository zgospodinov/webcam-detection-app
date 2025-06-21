import cv2
import time

video_capture = cv2.VideoCapture(0)
time.sleep(1)


while True:
    check, frame = video_capture.read()
    if not check:
        print("Failed to capture image")
        break
    cv2.imshow("Webcam Feed", frame)
    
    key = cv2.waitKey(1)
    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

video_capture.release()


