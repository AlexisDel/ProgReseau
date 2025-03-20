

# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client

broker = '192.168.0.125'
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
        if "1" in msg.payload.decode():
            os.system(f" sudo python3 ProgReseau/src/server/move.py 100 forward no 0.8")
        elif "2" in msg.payload.decode():
            os.system(f" sudo python3 ProgReseau/src/server/move.py 100")
        elif "3" in msg.payload.decode():
            os.system(f"sudo python3 ProgReseau/src/server/move.py 100 forward no 0.8")
        else:
            os.system("sudo python adeept_rasptank/server/LED.py")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
