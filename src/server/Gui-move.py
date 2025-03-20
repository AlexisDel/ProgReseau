import tkinter as tk
import random
import time

from paho.mqtt import client as mqtt_client

#MQTT CONN
broker = '192.168.0.125'
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


root = tk.Tk()  # Create the main window
def forward(n):
    
    client.loop_start()
    time.sleep(1)
    
    msg = f"{n}"
    result = client.publish(topic, msg)
        
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    client.loop_stop()
    

def backward():
    
    client.loop_start()
    time.sleep(1)
    
    msg = f"{4}"
    result = client.publish(topic, msg)
        
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    client.loop_stop()

# Create a TV remote UI
frame = tk.Frame(root)
frame.pack(expand=True)

btn_up = tk.Button(frame, text="Haut")
btn_up.grid(row=0, column=1)
btn_up.bind('<ButtonPress-1>',forward(1))
btn_up.bind('<ButtonRelease-1>',forward(2))

btn_left = tk.Button(frame, text="Gauche", command=None)
btn_left.grid(row=1, column=0)

btn_right = tk.Button(frame, text="Droite", command=None)
btn_right.grid(row=1, column=2)

btn_down = tk.Button(frame, text="Bas", command=backward)
btn_down.grid(row=2, column=1)

btn_extra = tk.Button(frame, text="Extra", command=None)
btn_extra.grid(row=3, column=1)



root.mainloop()


