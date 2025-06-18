# main_gui.py
import tkinter as tk
from tkinter import messagebox
from capture_faces import capture_faces
from train_model import train
from recognize_faces import recognize

def start_capture():
    user_id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()

    if not (user_id.isdigit() and age.isdigit() and name):
        messagebox.showerror("Input Error", "Please enter valid ID, Name, and Age.")
        return

    capture_faces(int(user_id), name, int(age))
    messagebox.showinfo("Success", "Face capture completed!")

def start_training():
    train()
    messagebox.showinfo("Success", "Model trained successfully!")

def start_recognition():
    recognize()

# GUI Layout
root = tk.Tk()
root.title("Face Recognition System")

tk.Label(root, text="Enter User ID:", font=('Helvetica', 12)).pack(pady=5)
entry_id = tk.Entry(root, font=('Helvetica', 12))
entry_id.pack(pady=5)

tk.Label(root, text="Enter Name:", font=('Helvetica', 12)).pack(pady=5)
entry_name = tk.Entry(root, font=('Helvetica', 12))
entry_name.pack(pady=5)

tk.Label(root, text="Enter Age:", font=('Helvetica', 12)).pack(pady=5)
entry_age = tk.Entry(root, font=('Helvetica', 12))
entry_age.pack(pady=5)

tk.Button(root, text="Capture Face", command=start_capture, font=('Helvetica', 12)).pack(pady=10)
tk.Button(root, text="Train Model", command=start_training, font=('Helvetica', 12)).pack(pady=10)
tk.Button(root, text="Recognize Face", command=start_recognition, font=('Helvetica', 12)).pack(pady=10)

root.mainloop()
