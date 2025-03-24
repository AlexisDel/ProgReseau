import tkinter as tk
import random
import time
from paho.mqtt import client as mqtt_client

#MQTT CONN
broker = 'broker.emqx.io' #'192.168.0.125'
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

    result = client.publish(topic, msg)
        
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    client.loop_stop()


root = tk.Tk()
root.title("Interface de Mouvement")
root.geometry("300x300")

#root.geometry("600x500")
# video
video_frame = tk.Frame(root, bg="black")
video_frame.pack(side="top", fill="both", expand=True)
video_frame.pack(expand=True, side="top", fill="both",)
video_label = tk.Label(video_frame)
video_label.pack()

# controls
frame = tk.Frame(root)
frame.pack(expand=True)
btn_up = tk.Button(frame, text="Haut")
btn_up.grid(row=0, column=1)
btn_up.bind("<ButtonPress>", lambda event: sent("start"))
btn_up.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_left = tk.Button(frame, text="Gauche")
btn_left.grid(row=1, column=0)
btn_left.bind("<ButtonPress>", lambda event: sent("left"))
btn_left.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_right = tk.Button(frame, text="Droite")
btn_right.grid(row=1, column=2)
btn_right.bind("<ButtonPress>", lambda event: sent("right"))
btn_right.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_down = tk.Button(frame, text="Bas")
btn_down.grid(row=2, column=1)
btn_down.bind("<ButtonPress>", lambda event: sent("back"))
btn_down.bind("<ButtonRelease>", lambda event: sent("stop"))

btn_extra = tk.Button(frame, text="Extra")
btn_extra.grid(row=3, column=1)
btn_extra.bind("<ButtonPress>", lambda event: sent("Extra"))
btn_extra.bind("<ButtonRelease>", lambda event: sent("Extra"))
# update_video()
root.mainloop()



import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
from flask import Flask

VIDEO_URL = "http://ip@:5000/video_feed"
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
        response = requests.get(VIDEO_STREAM_URL, stream=True, timeout=1)
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
