""" import tkinter as tk
  
# Create a GUI app 


root = tk.Tk()
root.title("Interface de Mouvement")
root.geometry("1000x1000")
  
# Constructing the first frame, frame1 
controls_frame = tk.Frame(root, width=3000, height=1000).grid(row=0, column=0) 
controls_frame.pack(expand=True)

# Displaying the frame1 in row 0 and column 0 
  
# Constructing the button b1 in frame1 
btn_up = tk.Button(controls_frame, text="Haut")
btn_left = tk.Button(controls_frame, text="Gauche")

btn_right = tk.Button(controls_frame, text="Droite")
btn_down = tk.Button(controls_frame, text="Bas")
btn_extra = tk.Button(controls_frame, text="Extra")

  
# Constructing the second frame, frame2 
video_frame = tk.Frame(root, bg="black")
# Displaying the frame2 in row 0 and column 1 
video_frame.grid(row=0, column=1) 
#video_frame.pack(expand=True)
# Constructing the button in frame2 

# Make the loop for displaying app 
root.mainloop()  """

from tkinter import *
import cv2
from PIL import Image, ImageTk


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

controls_frame = Frame(root, bg='green', width=400, height=900, padx=3, pady=3).grid(column = 1, row=0)
video_frame = Frame(root, bg='black', width=1100, height=900, padx=3, pady=3).grid(column = 0, row=0)
video_label = Label(video_frame, bg="black")
video_label.grid(row=0, column=0, sticky="nsew")


""" video_stream= HtmlFrame(video_frame)
video_stream.load_website(VIDEO_URL) """

cap = cv2.VideoCapture(VIDEO_URL)

update_frame()

root.mainloop()

cap.release()