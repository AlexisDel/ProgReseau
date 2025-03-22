import time
from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

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
    """Wipe color across display a pixel at a time."""
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

if __name__ == '__main__':
    try:
      setup()
      while 1:
        run()
      pass
    except KeyboardInterrupt:
      colorWipe(0, 0, 0)


