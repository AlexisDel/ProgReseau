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
def forward():
    
    client.loop_start()
    time.sleep(1)
    
    msg = f"{3}"
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
turn_on = tk.Button(root, text="FORWARD", command=forward)
turn_on.pack()

turn_off = tk.Button(root, text="BACKWARD", command=backward)
turn_off.pack()

volume = tk.Label(root, text="VOLUME")
volume.pack()

vol_up = tk.Button(root, text="+")
vol_up.pack()

vol_down = tk.Button(root, text="-")
vol_down.pack()


root.mainloop()


