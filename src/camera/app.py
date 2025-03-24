#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import threading
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


root = tk.Tk()
root.title("Interface de Mouvement")

root.geometry("600x500")
# video
video_frame = tk.Frame(root, bg="black")
video_frame.pack(side="top", fill="both", expand=True)
video_frame.pack(expand=True, side="top", fill="both",)
video_label = tk.Label(video_frame)
video_label.pack()


VIDEO_URL = "http://192.168.0.107:5000/video_feed"
app = Flask(__name__)

def run_flask():
    #from app import app
    app.run(host='0.0.0.0', threaded=True)

def run_video_thread():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

# Function to update the video feed in Tkinter
def update_video():
    try:
        response = requests.get(VIDEO_URL, stream=True, timeout=1)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((400, 300))  # Resize the image to fit GUI
            img = ImageTk.PhotoImage(img)
            video_label.config(image=img)
            video_label.image = img
    except Exception as e:
        print("⚠️ Video stream error:", e)

    root.after(50, update_video)  # Update every 50ms
