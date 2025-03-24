import tkinter as tk
import random
import time

from paho.mqtt import client as mqtt_client

#MQTT CONN
broker = 'broker.emqx.io'#'192.168.0.125' #
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


root = tk.Tk()
root.title("Interface de Mouvement")
root.geometry("300x300")
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

btn_extra = tk.Button(frame, text="INIT")
btn_extra.grid(row=4, column=2, command=lambda event: sent("INIT"))

btn_shoot = tk.Button(frame, text="Tirer", command=shoot)
btn_shoot.grid(row=4, column=1)

root.mainloop()

