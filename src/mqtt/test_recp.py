# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client
from src.server import move, infra
from src.server.LED import LED
import RPi.GPIO as GPIO
from src.rasptank import InfraLib
import uuid
from threading import Thread

broker = '192.168.0.125' #''broker.emqx.io
tankID = uuid.getnode()

port = 1883
topics = ["python/ctrlrobot", "tanks/id/init", "tanks/id/shots/in", "tanks/id/shots/out"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

led = LED()

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
    while True:
        shooter = InfraLib.getSignal(IR_RECEIVER)
        if shooter:
            shooter = str(shooter)[2:]
            print(f"on était shooter par {shooter}")
            client.publish('tanks/id/shots', f'SHOT_BY {shooter}')

def set_motor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    

    move.motorStop()


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
                print(f"on est : {tankID} ")
                infra.shoot()
                led.blink(r=255, g=0, b=0, time_sec=0.2)
        if msg.topic == "tanks/id/init":
            if "TEAM BLUE" in msg.payload.decode():
                led.blink(r=0, g=0, b=255, time_sec=1)
            if "TEAM RED" in msg.payload.decode():
                led.blink(r=255, g=0, b=0, time_sec=1)
        if msg.topic == "tanks/id/shots/in":
            if "SHOT" in msg.payload.decode():
                led.blink_shot()
            if "FLAG_LOST" in  msg.payload.decode():
                led.blink(r=255, g=0, b=0, time_sec=1)
            if "ABORT_CATCHING_SHOT" in msg.payload.decode():
                led.blink(r=255, g=0, b=0, time_sec=1)
                pass
        if msg.topic == "tanks/id/shots/out":
            if "FRIENDLY_FIRE" in msg.payload.decode():
                led.blink(0.5)
            if "SHOT" in msg.payload.decode():
                led.blink(r=0,g=255,b=0, time_sec=1)


    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    t1 = Thread(target=set_receive_infra, args=(client,))
    t1.start()
    #set_motor()
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        move.destroy()
