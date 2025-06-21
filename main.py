import cv2
import time

video_capture = cv2.VideoCapture(0)
time.sleep(1)


first_frame = None

while True:
    check, frame = video_capture.read()
    if not check:
        print("Failed to capture image")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gaussian = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    if first_frame is None:
        first_frame = gray_frame_gaussian
        # continue

    delta_frame = cv2.absdiff(first_frame, gray_frame_gaussian)
    thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]
    diLated_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours, check = cv2.findContours(diLated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    cv2.imshow("Webcam Feed", frame)

    key = cv2.waitKey(1)
    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

video_capture.release()


