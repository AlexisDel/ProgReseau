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

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    #motor.setup()

# Define functions which animate LEDs in various ways.
def colorWipe( R, G, B):
    color = Color(R,G,B)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    print('LF3: %d   LF2: %d   LF1: %d\n'%(status_right,status_middle,status_left))
    if status_left == 1 :
        strip.setPixelColor(0, Color(0, 0, 255))
    else:
        strip.setPixelColor(0, Color(0, 0, 0))
    if status_middle == 1:
        strip.setPixelColor(1, Color(1, 0, 255))
    else:
        strip.setPixelColor(1, Color(1, 0, 0))
    if  status_right == 1:
        strip.setPixelColor(2, Color(2, 0, 255)) 
    else:
        strip.setPixelColor(2, Color(0, 0, 0))
    strip.show()

""" if __name__ == '__main__':
    try:
      setup()
      while 1:
        run()
      pass
    except KeyboardInterrupt:
      colorWipe(0, 0, 0)
 """

launch_capture = False
stop_thread = False

def set_led_color(R, G, B):
    color = Color(R, G, B)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

            
def detect_zone_capture():
  global launch_capture, stop_thread
  setup()
  while not launch_capture:
      rsensor = GPIO.input(line_pin_right)
      lsensor = GPIO.input(line_pin_left)
      msensor = GPIO.input(line_pin_middle)

      if rsensor==0 and lsensor == 0 and msensor == 0:
        launch_capture = True
        print("Zone de capture détectée!")
        set_led_color(0,0,255)
        start_capture()
        """ if not launch_capture:
                launch_capture = True
                print("Zone de capture détectée!")
                set_led_color(0,0,255)
                start_capture() """
      """ else:
        launch_capture = False """

# 5 sec countdown to capture flag
def start_capture():
  global launch_capture
  set_led_color(255,255,0)
  for i in range(5):
     time.sleep(1)
     print(f"{5-i}")
     if not( GPIO.input(line_pin_right) == 0 and GPIO.input(line_pin_left) == 0 and GPIO.input(line_pin_middle) == 0):
         launch_capture = False
         print(f"left capture zone")
         return
  print(f"Drapeau capturée!")
  set_led_color(0,255,0)
  #launch_capture = False



def start_detection():
    detection_thread = threading.Thread(target=detect_zone_capture, daemon=True)
    detection_thread.start()
    print("thread start function should be started?")
    detection_thread.join()

detect_zone_capture()