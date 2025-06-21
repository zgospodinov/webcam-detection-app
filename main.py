import cv2
import time
from emailing import send_email
import os
import glob
from threading import Thread


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

video_capture = cv2.VideoCapture(0)
time.sleep(1)


first_frame = None
status_list = []
count = 1



while True:
    status = 0
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
        rectangle =  cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1
            cv2.imwrite(f"{SCRIPT_DIR}/images/frame_{count}.jpg", frame)
            count += 1

            all_images = glob.glob(f"{SCRIPT_DIR}/images/*.jpg")
            image_index = int(len(all_images) / 2)
            image_with_object = all_images[image_index] 
        
            
    status_list.append(status)
    status_list = status_list[-2:]
    
    if status_list[0] == 1 and status_list[1] == 0:
        print("Movement detected!")
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        email_thread.start()

        

        first_frame = None
        status_list = []
        count = 1

    cv2.imshow("Webcam Feed", frame)

    key = cv2.waitKey(1)
    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

video_capture.release()



