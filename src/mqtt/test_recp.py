# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client
from src.server import move
import RPi.GPIO as GPIO
from src.rasptank import InfraLib
import uuid

broker = '192.168.0.125' #''broker.emqx.io
tankID = uuid.getnode()

port = 1883
topics = ["python/ctrlrobot", "tanks/id/init", "tanks/id/shots/in", "tanks/id/shots/out"]
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

def set_receive_infra(client):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    IR_RECEIVER = 15
    GPIO.setup(IR_RECEIVER, GPIO.IN)
    GPIO.add_event_detect(IR_RECEIVER, GPIO.FALLING, callback=lambda x: InfraLib.getSignal(IR_RECEIVER, client), bouncetime=100)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == "python/ctrlrobot":
            if "start" in msg.payload.decode("utf-8"):
                move.start()
            if "left" in msg.payload.decode("utf-8"):
                move.left()
            if "right" in msg.payload.decode("utf-8"):
                move.right()
            if "back" in msg.payload.decode("utf-8"):
                move.back()
            if "stop" in msg.payload.decode("utf-8"):
                move.stop()
            if "tir" in msg.payload.decode():
                os.system(f"sudo python3 ProgReseau/src/server/infra.py")
        if msg.topic == "tanks/id/init":
            if "TEAM BLUE" in msg.payload.decode():
                #TODO: add the code to make the LED blink blue
                pass
            if "TEAM RED" in msg.payload.decode():
                #TODO: add the code to make the LED blink red
                pass
        if msg.topic == "tanks/id/shots/in":
            if "SHOT" in msg.payload.decode():
                #TODO: add the code to make the LED blink red
                pass
            if "FLAG_LOST" in  msg.payload.decode():
                #TODO: add code when flag is lost
                pass
            if "ABORT_CATCHING_SHOT" in msg.payload.decode():
                #TODO: add code when the shot is aborted
                pass
        if msg.topic == "tanks/id/shots/out":
            if "FRIENDLY_FIRE" in msg.payload.decode():
                #TODO: add the code in case of friendly fire
                pass
            if "SHOT" in msg.payload.decode():
                #TODO: add the code in case of shot (flash green)
                pass


    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    #set_receive_infra(client)
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        move.destroy()
