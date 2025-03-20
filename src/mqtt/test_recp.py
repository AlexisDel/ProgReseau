

# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client
from src.server import move


broker = 'broker.emqx.io' #'192.168.0.125'
port = 1883
topic = "python/ctrlrobot"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt() -> mqtt_client:
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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if "start" in msg.payload.decode("utf-8"):
            move.start()
        elif "left" in msg.payload.decode("utf-8"):
            move.left()
        elif "right" in msg.payload.decode("utf-8"):
            move.right()
        elif "back" in msg.payload.decode("utf-8"):
            move.back()
        elif "stop" in msg.payload.decode("utf-8"):
            move.stop()

    client.subscribe(topic)
    
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
