import random
import paho.mqtt.client as mqtt
import time
import threading
import os
import sys

#blueTeamQRCode = "0x4d61792074686520666f726365206265207769746820796f7521"
#redTeamQRCode = "0x596f7520646f6e2774206b6e6f772074686520706f776572206f6620746865206461726b207369646521"

qr_codes = {"RED": "Hello_World", "BLUE": "Hello_World"}
weapons = {"0xf1": "Laser Gun"}

def assignToTeam(id):
    if sum(x['color'] == "RED" for x in participants.values()) < sum(x['color'] == "BLUE" for x in participants.values()):
        addToRedTeam(id)
    elif sum(x['color'] == "RED" for x in participants.values()) > sum(x['color'] == "BLUE" for x in participants.values()):
        addToBlueTeam(id)
    else:
        if random.choice(["RED", "BLUE"]) == "RED":
            addToRedTeam(id)
        else:
            addToBlueTeam(id)

    client.publish("tanks/"+id+"/init", "END")


def addToBlueTeam(id):
    participants[id] = {"color": "BLUE", "flag": False, "catching": False}
    client.publish("tanks/"+id+"/init", "TEAM BLUE")
    client.publish("tanks/"+id+"/init", "QR_CODE "+qr_codes["BLUE"])
    print("Rasptank "+id+" is BLUE")

def addToRedTeam(id):
    participants[id] = {"color": "RED", "flag": False, "catching": False}
    client.publish("tanks/"+id+"/init", "TEAM RED")
    client.publish("tanks/"+id+"/init", "QR_CODE "+qr_codes["RED"])
    print("Rasptank "+id+" is RED")


def giveFlag(id, topic):
    global flag
    for i in range(5):
        time.sleep(1)
        if not participants[id]["catching"]:
            return
    participants[id]["flag"] = True
    participants[id]["catching"] = False
    client.publish(topic, "FLAG_CATCHED")
    print(id + " captured the flag")


def processData(client, userdata, message):
    global flag
    querry = str(message.payload.decode("utf-8")).split(" ")

    if message.topic == "init":
        if querry[0] == "INIT":
            if initPhase:
                assignToTeam(querry[1])
            else:
                client.publish(f"tanks/{querry[1]}/init", "GAME_ALREADY_STARTED")
    else:
        # Split topic into parts and extract components
        topic_parts = message.topic.split('/')
        participant_id = topic_parts[1]  # Second element is always the ID
        subtopic = topic_parts[2] if len(topic_parts) > 2 else ''  # Third element is the subtopic

        if participant_id in participants.keys():
            if subtopic == "flag":
                if querry[0] == "ENTER_FLAG_AREA":
                    if not any(participants[p]["flag"] for p in participants.keys()):
                        client.publish(message.topic, "START_CATCHING")
                        print(f"{participant_id} start catching the flag")
                        participants[participant_id]["catching"] = True
                        threading.Thread(target=giveFlag, args=[participant_id, message.topic]).start()
                    elif participants[participant_id]["flag"]:
                        client.publish(message.topic, "ALREADY_GOT")
                        print(f"{participant_id} has already the flag")
                    else:
                        client.publish(message.topic, "NOT_ONBASE")
                        print(f"Hey {participant_id}, there is no flag here anymore")

                elif querry[0] == "EXIT_FLAG_AREA":
                    if participants[participant_id]["catching"]:
                        client.publish(message.topic, "ABORT_CATCHING_EXIT")
                        print(f"{participant_id} abort catching the flag, you exited the flag area")
                        participants[participant_id]["catching"] = False

            elif subtopic == "shots":
                if querry[0] == "SHOT_BY":
                    shot = querry[1][:4]
                    shooter = "0x" + querry[1][4:]
                    if shooter in participants.keys():
                        if participants[participant_id]["color"] != participants[shooter]["color"]:
                            client.publish(f"{message.topic}/in", "SHOT")
                            client.publish(f"tanks/{shooter}/shots/out", "SHOT")
                            print(f"{participant_id} shot by {shooter} with {weapons[shot]}")

                            # Flag check
                            if participants[participant_id]["catching"]:
                                client.publish(f"tanks/{participant_id}/flag", "ABORT_CATCHING_SHOT")
                                print(f"{participant_id} abort catching the flag, you got shot")
                                participants[participant_id]["catching"] = False
                            if participants[participant_id]["flag"]:
                                client.publish(f"tanks/{participant_id}/flag", "FLAG_LOST")
                                print(f"{participant_id} you lost the flag")
                                participants[participant_id]["flag"] = False
                        else:
                            if participant_id != shooter:
                                client.publish(f"tanks/{shooter}/shots/out", "FRIENDLY_FIRE")
                                print(f"Carefull {shooter}, friendly fire")

            elif subtopic == "qr_code":
                if querry[0] == "QR_CODE":
                    qr = querry[1]
                    if qr == qr_codes.get(participants[participant_id]["color"]):
                        client.publish(message.topic, "SCAN_SUCCESSFUL")
                        if participants[participant_id]["flag"]:
                            client.publish(f"tanks/{participant_id}/flag", "FLAG_DEPOSITED")
                            participants[participant_id]["flag"] = False
                            # Winner check
                            scores[participants[participant_id]["color"]] += 1
                            print(f"RED : {scores['RED']} // BLUE : {scores['BLUE']}")
                            if scores[participants[participant_id]["color"]] == 1:
                                for id in participants.keys():
                                    client.publish(f"tanks/{id}/flag", f"WIN {participants[participant_id]['color']}")
                        else:
                            client.publish(f"tanks/{participant_id}/flag", "NO_FLAG")
                            print(f"{participant_id}, there is no flag to deposit")
                    else:
                        client.publish(message.topic, "SCAN_FAILED")


def start_game():
    print("Welcome to World of Rasptank")
    input("Initialisation phase, press Enter to continue...\n")
    initPhase = False
    print("Initialisation phase finished")

def new_game():
    os.system('clear')
    scores = {"RED":0, "BLUE":0}
    print("New Game")


# Main
if __name__ == "__main__":

    initPhase = True
    participants = {}
    scores = {"RED":0, "BLUE":0}

    client = mqtt.Client()
    client.connect("192.168.0.100")

    client.subscribe("init")
    client.subscribe("tanks/+/flag")
    client.subscribe("tanks/+/shots")
    client.subscribe("tanks/+/qr_code")
    client.loop_start()
    client.on_message = processData

    start_game()

    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        client.loop_stop()
