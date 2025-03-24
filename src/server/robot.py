# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client
from src.server import move, LED, infra, detectLine
import RPi.GPIO as GPIO
from src.rasptank import InfraLib
import uuid
from threading import Thread

broker = '192.168.0.125' #''broker.emqx.io
tankID = uuid.getnode()

port = 1883
topics = ["python/ctrlrobot", 
          f"tanks/{tankID}/init", 
          f"tanks/{tankID}/shots/in", 
          f"tanks/{tankID}/shots/out", 
          f"tanks/{tankID}/flag",
          f"tanks/{tankID}/qr_code"
          ]
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
    IR_RECEIVER = 15
    GPIO.setup(IR_RECEIVER, GPIO.IN)
    while True:
        shooter = InfraLib.getSignal(IR_RECEIVER)
        print(shooter)
        client.publish('tanks/id/shots', f'SHOT_BY {shooter}')

def set_motor():
    Motor_A_EN    = 7
    Motor_B_EN    = 11

    Motor_A_Pin1  = 8
    Motor_A_Pin2  = 10
    Motor_B_Pin1  = 13
    Motor_B_Pin2  = 12
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)

    move.motorStop()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode("utf-8")
        print(f"Received `{message}` from `{msg.topic}` topic")
        if msg.topic == "python/ctrlrobot":
            if "start" in message:
                move.start()
            if "left" in message:
                move.left()
            if "right" in message:
                move.right()
            if "back" in message:
                move.back()
            if "stop" in message:
                move.stop()
            if "tir" in message:
                infra.shoot()
                led.blink(r=255, g=0, b=0, time_sec=0.2)
        if msg.topic == f"tanks/{tankID}/init":
            if "TEAM BLUE" in message:
                led.blink(r=0, g=0, b=255, time_sec=1)
            if "TEAM RED" in msg.payload.decode():
                led.blink(r=255, g=0, b=0, time_sec=1)
        if msg.topic == f"tanks/{tankID}/shots/in":
            if "SHOT" in message:
                led.blink_shot()
        if msg.topic == f"tanks/{tankID}/shots/out":
            if "FRIENDLY_FIRE" in message:
                led.blink(0.5)
            if "SHOT" in message:
                led.blink(r=0,g=255,b=0, time_sec=1)
        if msg.topic == f"tanks/{tankID}/flag":
            #TODO: fill in the blanks
            if "START_CATCHING" in message:
                pass
            if "FLAG_CATCHED" in message:
                pass
            if "ABORT_CATCHING_EXIT" in message:
                pass
            if "ABORT_CATCHING_SHOT" in message:
                led.blink(r=255, g=0, b=0, time_sec=1)
                pass
            if "FLAG_LOST" in  message:
                led.blink(r=255, g=0, b=0, time_sec=1)
            if "WIN_BLUE" in message:
                pass
            if "WIN_RED" in message:
                pass
        if msg.topic == f"tanks/{tankID}/qr_code" :
            if "SCAN_SUCCESSFUL" in message:
                pass
            if "SCAN_FAILED" in message:
                pass
            if "FLAG_DEPOSITED" in message:
                pass
            if "NO_FLAG" in message:
                pass
        

    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    Thread(set_receive_infra, client)
    set_motor()
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        move.destroy()
