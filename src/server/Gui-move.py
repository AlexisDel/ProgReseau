import tkinter as tk
import random
import time
import os
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import cv2
from threading import Thread

from paho.mqtt import client as mqtt_client

#MQTT CONN
broker = 'broker.emqx.io' #192.168.0.125
port = 1883
topic = "python/ctrlrobot"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt()
#GUI


def sent(msg):
    
    client.loop_start()
    time.sleep(1)
    
    result = client.publish(topic, msg)
        
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    client.loop_stop()


def shoot():
    
    client.loop_start()
    time.sleep(1)
    
    msg = f"tir"
    result = client.publish(topic, msg)
        
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    client.loop_stop()

def key_press(event):
    key_map = {
        "z": "start",
        "q": "left",
        "d": "right",
        "s": "back",
        "t": "tir"
    }
    if event.keysym in key_map:
        sent(key_map[event.keysym])

def key_release(event):
    if event.keysym in ["z", "q", "d", "s"]:
        sent("stop")

""" def update_video():
    pipeline = (
        "udpsrc port=5000 caps=application/x-rtp,encoding-name=H264,payload=96 ! "
        "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("❌ Failed to open video stream")
        return

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 360))
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            video_label.imgtk = img
            video_label.config(image=img)
        time.sleep(0.03)
 """
root = ttk.Window(themename="flatly") 
root.title("Game Console")
root.geometry("300x300")

frame = ttk.Frame(root)
frame.pack(expand=True)

""" # === Video Feed Frame ===
video_label = ttk.Label(frame)
video_label.grid(row=0, column=0, columnspan=3, pady=10)
 """
btn_up = ttk.Button(frame, text="Haut",bootstyle="primary-outline")
btn_up.grid(row=0, column=1)
btn_up.bind("<ButtonPress>", lambda event: sent("start"))
btn_up.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_left = ttk.Button(frame, text="Gauche",bootstyle="primary-outline")
btn_left.grid(row=1, column=0)
btn_left.bind("<ButtonPress>", lambda event: sent("left"))
btn_left.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_right = ttk.Button(frame, text="Droite",bootstyle="primary-outline")
btn_right.grid(row=1, column=2)
btn_right.bind("<ButtonPress>", lambda event: sent("right"))
btn_right.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_down = ttk.Button(frame, text="Bas",bootstyle="primary-outline")
btn_down.grid(row=2, column=1)
btn_down.bind("<ButtonPress>", lambda event: sent("back"))
btn_down.bind("<ButtonRelease>", lambda event: sent("stop"))

current_dir = os.path.dirname(__file__)
img_path = os.path.join(current_dir, "power_button.png")

power_img = Image.open(img_path)
resample_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
power_img = power_img.resize((30, 30), resample_filter)
power_icon = ImageTk.PhotoImage(power_img)

canvas = tk.Canvas(frame, width=40, height=40, highlightthickness=0, bg="white", bd=0)
canvas.grid(row=4, column=2,  pady=(10, 0))

canvas.create_image(0, 0, anchor="nw", image=power_icon)

def on_click(event):
    sent("INIT")

canvas.bind("<Button-1>", on_click)


btn_shoot = ttk.Button(frame, text="Tirer", command=shoot)
btn_shoot.grid(row=4, column=1)


btn_scan = ttk.Button(frame, text="Scan")
btn_scan.grid(row=4, column=3)
btn_scan.bind("<ButtonPress>", lambda event: sent("scan"))

os.system('xset r off')
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

#Thread(target=update_video, daemon=True).start()

root.mainloop()


"""
root = ttk.Window(themename="flatly") 
root.title("Game Console")
root.geometry("720x600")

frame = ttk.Frame(root)
frame.pack(expand=True)

# === Video Feed Frame ===
video_label = ttk.Label(frame)
video_label.grid(row=0, column=0, columnspan=3, pady=10)

btn_up = ttk.Button(frame, text="Haut",bootstyle="primary-outline")
btn_up.grid(row=1, column=1)
btn_up.bind("<ButtonPress>", lambda event: sent("start"))
btn_up.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_left = ttk.Button(frame, text="Gauche",bootstyle="primary-outline")
btn_left.grid(row=2, column=0)
btn_left.bind("<ButtonPress>", lambda event: sent("left"))
btn_left.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_right = ttk.Button(frame, text="Droite",bootstyle="primary-outline")
btn_right.grid(row=2, column=2)
btn_right.bind("<ButtonPress>", lambda event: sent("right"))
btn_right.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_down = ttk.Button(frame, text="Bas",bootstyle="primary-outline")
btn_down.grid(row=3, column=1)
btn_down.bind("<ButtonPress>", lambda event: sent("back"))
btn_down.bind("<ButtonRelease>", lambda event: sent("stop"))

current_dir = os.path.dirname(__file__)
img_path = os.path.join(current_dir, "power_button.png")

power_img = Image.open(img_path)
resample_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
power_img = power_img.resize((30, 30), resample_filter)
power_icon = ImageTk.PhotoImage(power_img)

canvas = tk.Canvas(frame, width=40, height=40, highlightthickness=0, bg="white", bd=0)
canvas.grid(row=4, column=2,  pady=(10, 0))

canvas.create_image(0, 0, anchor="nw", image=power_icon)

def on_click(event):
    sent("INIT")

canvas.bind("<Button-1>", on_click)


btn_shoot = ttk.Button(frame, text="Tirer", command=shoot)
btn_shoot.grid(row=4, column=1)


btn_scan = ttk.Button(frame, text="Scan")
btn_scan.grid(row=4, column=2)
btn_scan.bind("<ButtonPress>", lambda event: sent("scan"))

os.system('xset r off')
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

Thread(target=update_video, daemon=True).start()


"""