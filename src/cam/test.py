from tkinter import *
import cv2
from PIL import Image, ImageTk

# sudo apt-get install libx264-dev libjpeg-dev
# sudo apt-get install gstreamer1.0-tools
# gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    else:
        print("⚠️ Warning: No frame received from stream!")

    video_label.after(10, update_frame)


VIDEO_URL = "http://127.0.0.1:5000/video_feed" 
root = Tk()
root.title('Model Definition')
root.resizable(width=FALSE, height=FALSE)
root.geometry("1500x900")

video_frame = Frame(root, bg='black', width=1100, height=900, padx=3, pady=3).grid(column = 0, row=0)
video_label = Label(video_frame, bg="black")
video_label.grid(row=0, column=0, sticky="nsew")
cap = cv2.VideoCapture(VIDEO_URL)
update_frame()

controls_frame = Frame(root, bg='green', width=400, height=900, padx=3, pady=3).grid(column = 1, row=0)


root.mainloop()

cap.release()