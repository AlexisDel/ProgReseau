import time
from rpi_ws281x import *
import threading
import RPi.GPIO as GPIO
#if you want to be able to get the flag and check if you're hit at the same time the stuff needs to be in separate threads, so that you can keep listening and do the actions/listen for more


# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      
# DMA channel to use for generating signal (try 10) ; used to send LED data efficiently without interfering with other raspberry pi tasks
# Higher DMA channels (like 10 or 5) reduce conflicts with audio and other processes, if it's flickering try 5 or 1
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest // for less power consumption lower this
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


line_pin_right = 19 # led 1
line_pin_middle = 16 # led 2
line_pin_left = 20 # led 3


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)

launch_capture = False
stop_thread = False
stop_thread = False
            
def detect_zone_capture(verbose=False):
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
                print("Zone de capture détectée!")
                #TODO publish to server
                start_capture() # wait
        else :
            if was_in_capture_zone:
                was_in_capture_zone = False
                #TODO publish exit area


  
# 5 sec countdown to capture flag
def start_capture():
  for i in range(5):
     time.sleep(1)
     print(f"{5-i}")
     if not( GPIO.input(line_pin_right) == 0 and GPIO.input(line_pin_left) == 0 and GPIO.input(line_pin_middle) == 0):
         return
  print(f"Drapeau capturée!")
  return True



def start_detection():
    detection_thread = threading.Thread(target=detect_zone_capture, daemon=True)
    detection_thread.start()
    print("thread start function should be started?")
    detection_thread.join()
