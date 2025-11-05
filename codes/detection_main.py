import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import joblib
from PIL import Image, ImageTk
import serial
import time

# ========== Arduino Setup ==========
# Change 'COM3' to your Arduino port (check Device Manager)
try:
    arduino = serial.Serial('COM8', 9600, timeout=1)
    time.sleep(2)
    print(" Connected to Arduino on COM3")
except:
    arduino = None
    print("Arduino not connected! Continue without serial output.")

# ========== Model Setup ==========
model = joblib.load("speed_sign_model.pkl")
IMG_SIZE = (64, 64)

# ========== GUI Setup ==========
root = tk.Tk()
root.title("Speed Sign Detection & Arduino Alert")
root.geometry("900x700")
root.configure(bg="#222")

title_label = tk.Label(root, text="Speed Sign Detection System", font=("Arial", 22, "bold"), fg="white", bg="#222")
title_label.pack(pady=10)

frame_label = tk.Label(root, bg="#222")
frame_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 18, "bold"), fg="yellow", bg="#222")
result_label.pack(pady=10)

alert_label = tk.Label(root, text="", font=("Arial", 18, "bold"), fg="red", bg="#222")
alert_label.pack(pady=10)

# ========== Detection Logic ==========
def detect_sign(image_path):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Cannot read image file.")
        return None

    img_resized = cv2.resize(img, IMG_SIZE)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    flat = gray.flatten().reshape(1, -1)

    pred = model.predict(flat)[0]
    prob = model.predict_proba(flat)[0].max()

    if prob > 0.7:
        return pred, prob
    else:
        return None, prob

# ========== Upload & Display ==========
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select Speed Sign Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not file_path:
        return

    # Show image
    img = cv2.imread(file_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.resize(img_rgb, (400, 400))
    im_pil = Image.fromarray(img_rgb)
    imgtk = ImageTk.PhotoImage(image=im_pil)
    frame_label.config(image=imgtk)
    frame_label.image = imgtk

    # Detect sign
    pred, prob = detect_sign(file_path)

    if pred:
        result_label.config(text=f"Detected: Speed Limit {pred} km/h  ({prob*100:.1f}% confidence)")
        if pred < 60:
            alert_label.config(text=f" Decrease Speed to {pred} km/h", fg="red")
        else:
            alert_label.config(text=f" Safe Speed Limit: {pred} km/h", fg="green")

        # Send data to Arduino
        if arduino:
            try:
                arduino.write(f"{pred}\n".encode())
                print(f"Sent {pred} to Arduino")
            except:
                print("Error sending data to Arduino")

    else:
        result_label.config(text="No clear sign detected.")
        alert_label.config(text="")

# ========== Button ==========
upload_btn = tk.Button(
    root, text="📁 Upload Image", font=("Arial", 16, "bold"),
    bg="#4CAF50", fg="white", padx=20, pady=10, command=upload_image
)
upload_btn.pack(pady=20)

root.mainloop()

# Close serial connection on exit
if arduino:
    arduino.close()

