import uuid
import time
tankID = uuid.getnode()
client = None


###########################
#   CODE INFRAROUGE       #
###########################

import InfraLib
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# IR Receiver
IR_RECEIVER = 15
GPIO.setup(IR_RECEIVER, GPIO.IN)
GPIO.add_event_detect(IR_RECEIVER, GPIO.FALLING, callback=lambda x: InfraLib.getSignal(IR_RECEIVER, client), bouncetime=100)


while True:
    time.sleep(1)
    print("SHOT")
    InfraLib.IRBlast(tankID, "LASER")
