from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
import ssl
import imghdr
import glob
import os

def clean_images():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    all_images = glob.glob(f"{SCRIPT_DIR}/images/*.jpg")
    for image in all_images:
        os.remove(image)

def send_email(image_with_object):
    load_dotenv()

    print("Sending email...")
    host = "smtp.gmail.com"
    port = 465  # For SSL

    user_name = os.getenv("EMAIL_USERNAME")
    password = os.getenv("APP_EMAIL_KEY")

    if not user_name or not password:
        raise ValueError("Email credentials not found in .env file. Please check your .env file configuration.")

    context = ssl.create_default_context()

    msg = EmailMessage()
    msg['From'] = user_name
    msg['To'] = user_name
    msg['Subject'] = 'Movement detected on your webcam!'
    msg.set_content("Movement detected on your webcam! Please check the attached image for details.")

    # Attach the image
    with open(image_with_object, 'rb') as img_file:
        img_data = img_file.read()
        img_name = os.path.basename(image_with_object)
        msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data), filename=img_name)

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user_name, password)
        server.send_message(msg)

        clean_images()


if __name__ == "__main__":
    clean_images()