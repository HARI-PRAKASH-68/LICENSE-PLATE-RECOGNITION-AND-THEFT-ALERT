import cv2
import dlib
import pytesseract
import tkinter as tk
from PIL import Image, ImageTk
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import sqlite3


# Initialize Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# List of authorized vehicle numbers
authorized_vehicle_numbers = ["ABC123", "XYZ456", "123ABC", "12AB34CD"]
def send_email(detected_plate):
    sender_email = "harilicenseplaterecognition@gmail.com"  # Change this to your email
    subject = "License Plate Detected"
    body = f"License Plate {detected_plate} was detected at {time.strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        conn = sqlite3.connect("license.db")
        c = conn.cursor()
        c.execute("SELECT email FROM users")  
        recipient_emails = c.fetchall() 
        conn.close()
        for recipient_email in recipient_emails:
            recipient_email = recipient_email[0]
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Initiate TLS connection
                server.login(sender_email, "xhrs qfxn kokv muhu")  
                server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        #print("SMTP error:", e)
        return None
    except sqlite3.Error as e:
        #print("Database error:", e)
        return None

# Function to detect license plate using Tesseract OCR
def read_license_plate_tesseract(license_plate):
    (thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
    extracted_text = pytesseract.image_to_string(license_plate)
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', extracted_text)
    return cleaned_text

# Function to search for vehicles and detect license plates
def search_vehicle(frame, plat_detector, search_option=None):
    blur = cv2.GaussianBlur(frame,(7,7),0)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    canny_edge = cv2.Canny(gray_image, 0.1, 0.2)
    contours, _ = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    detected_plate = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = gray_image[y:y + h, x:x + w]
            text_tesseract = read_license_plate_tesseract(license_plate)
            search_option_upper = search_option.upper() if search_option else None
            text_upper = text_tesseract.upper()

            if search_option_upper is not None and text_upper == search_option_upper:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                frame = cv2.putText(frame, f"Plate: {text_tesseract}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                detected_plate = text_tesseract
                send_email(detected_plate)
            else:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                frame = cv2.putText(frame, f"Plate: {text_tesseract}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    return frame, detected_plate

class LicensePlateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Detection")

        # Initialize variables
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)
        self.plat_detector = dlib.get_frontal_face_detector()
        self.search_option_var = tk.StringVar()
        self.detected_plate = None

        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Logout", menu=file_menu)
        file_menu.add_command(label="Confirm", command=self.logout)

        # Search option entry
        search_label = tk.Label(self.root, text="Search Vehicle Number:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        search_entry = tk.Entry(self.root, textvariable=self.search_option_var)
        search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        search_button = tk.Button(self.root, text="Search", command=self.search)
        search_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # Video frame
        self.video_frame = tk.Label(self.root)
        self.video_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Start video processing
        self.processing = False
        self.update_video_feed()

    def search(self):
        if not self.processing:
            self.processing = True
            self.update_video_feed()
            if self.processing:
                self.search(self)

    def logout(self):
        self.processing = False
        self.cap.release()
        self.root.destroy()

    def update_video_feed(self):
        if self.processing:
            ret, frame = self.cap.read()
            if ret:
                processed_frame, self.detected_plate = search_vehicle(frame, self.plat_detector, search_option=self.search_option_var.get())
            if ret and processed_frame is not None:
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(image=img)
                self.video_frame.img_tk = img_tk
                self.video_frame.config(image=img_tk)
                if self.detected_plate:
                    send_email(self.detected_plate)
            self.root.after(10, self.update_video_feed)


# Create the main application window
root = tk.Tk()
root.wm_state('zoomed')
app = LicensePlateApp(root)
root.mainloop()
