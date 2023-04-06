import time


###########################
#   CODE FLAG AREA        #
###########################
import RPi.GPIO as GPIO

def enterFlagArea(channel):
    """
    Send flag zone related data to the server
    """
    if GPIO.input(LINE_PIN_MIDDLE) == GPIO.LOW:
        print("ENTER_FLAG_AREA")
        #client.publish("tanks/"+hex(tankID)+"/flag","ENTER_FLAG_AREA")
    else:
        print("EXIT_FLAG_AREA")
        #client.publish("tanks/"+hex(tankID)+"/flag", "EXIT_FLAG_AREA")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Tracking Module
LINE_PIN_MIDDLE = 36
GPIO.setup(LINE_PIN_MIDDLE,GPIO.IN)
GPIO.add_event_detect(LINE_PIN_MIDDLE, GPIO.BOTH, callback=enterFlagArea, bouncetime=100)

while True:
    time.sleep(0.1)
    
