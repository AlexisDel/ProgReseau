from rpi_ws281x import *
import RPi.GPIO as GPIO
from src.server.robot import tankID

line_pin_right = 35  # led 1
line_pin_middle = 36  # led 2
line_pin_left = 38  # led 3

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
            
def detect_zone_capture(client,verbose=False):
    setup()
    was_in_capture_zone = False
  
    while True:
        rsensor = GPIO.input(line_pin_right)
        lsensor = GPIO.input(line_pin_left)
        msensor = GPIO.input(line_pin_middle)
        if verbose:
            print('LF3: %d   LF2: %d   LF1: %d\n'%(rsensor,msensor,lsensor))
        if lsensor==0 and msensor == 0 and rsensor == 0:
            if not was_in_capture_zone:
                was_in_capture_zone = True                
                client.publish(f"tanks/{tankID}/flag", "ENTER_FLAG_AREA")
                print("Zone de capture détectée!")

        else :
            if was_in_capture_zone:
                was_in_capture_zone = False
                client.publish(f"tanks/{tankID}/flag", "EXIT_FLAG_AREA")
                print("Zone de capture quittée!")