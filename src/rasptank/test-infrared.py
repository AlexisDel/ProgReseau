import Adafruit_PCA9685
import curses
import json
from time import sleep, time
import subprocess
from rpi_ws281x import *
import RPi.GPIO as GPIO
import InfraLib
import threading
import uuid
import textwrap

tests_status = {
    'servo': {
        'arm': 0,
        'front_arm': 0,
        'canon': 0
    },
    'camera': 0,
    'motor': {
        'left_motor': 0,
        'right_motor': 0
    },
    'LED': 0,
    'Infrared_LED': 0,
    'Infrared_Receiver': 0,
    'Tracking_module': 0
}

def draw_instructions(instructions_win, instructions):
    instructions_win.clear()
    instructions_win.box()
    title = "Instructions"
    max_width = instructions_win.getmaxyx()[1] - 2  # Subtract 2 for border padding
    start_x_title = max(1, (max_width - len(title)) // 2)
    instructions_win.addstr(0, start_x_title, title)

    y_position = 1  # Starting Y position for the text
    for instruction in instructions:
        wrapped_text = textwrap.wrap(instruction, max_width)
        for line in wrapped_text:
            instructions_win.addstr(y_position, 1, line)
            y_position += 1  # Move to the next line after printing

    instructions_win.refresh()

    
def draw_status(status_win):
    status_win.clear()
    status_win.box()
    title = "Status"
    start_x_title = max(1, (status_win.getmaxyx()[1] - len(title)) // 2)
    status_win.addstr(0, start_x_title, title)
    y = 1
    for test_category, tests in tests_status.items():
        
        if type(tests) == dict:
            status_win.addstr(y, 1, f"{test_category.capitalize()}")
            y += 1
            for test, status in tests.items():
                symbol = '✅' if status == 1 else ('❌' if status == -1 else ' ')
                status_win.addstr(y, 3, f"{test.capitalize()}: {symbol}")
                y += 1
        
        if type(tests) == int:
            symbol = '✅' if tests == 1 else ('❌' if tests == -1 else ' ')
            status_win.addstr(y, 1, f"{test_category.capitalize()}: {symbol}")
            y += 1
        
        y += 1
             
    status_win.refresh()
    
def testInfraLED(instructions_win, status_win, again=False):
    
    if not again:
        draw_instructions(instructions_win,
        ["Infrared LED Testing Phase:",
        "Point your phone's camera towards the infrared LED, you should see it blink for about 5 seconds",
        "NB: The light intensity is very low. Ensure your phone is perfectly aligned with the LED.",
        "Press any key to start."]
        )
        instructions_win.getch()
    else:
        draw_instructions(instructions_win,
        ["Infrared LED Testing Phase:",
        "Point your phone's camera towards the infrared LED, you should see it blink for about 3 seconds",
        "NB: The light intensity is very low. Ensure your phone is perfectly aligned with the LED."]
        )
    
    start_time = time()  
    while time() - start_time < 3:
        InfraLib.IRBlast(uuid.getnode(), "LASER")
        sleep(0.5)
        
    draw_instructions(instructions_win,
        ["Infrared LED Testing Phase:",
        "Did it work? Press y/n",
        "Press r to do it again",
        "Press c to continue (you migth not be able to see the light)"]
    )
    key = instructions_win.getch()
    
    if key == ord('y'):
        tests_status["Infrared_LED"] = 1
    elif key == ord('n'):
        tests_status["Infrared_LED"] = -1
    elif key == ord('r'):
        testInfraLED(instructions_win, status_win, again=True)
    elif key == ord('c'):
        pass
    else:
        key = instructions_win.getch()
    
    draw_status(status_win)
    
    
def testInfraReceiver(instructions_win, status_win):
    
    draw_instructions(instructions_win,
        ["Infrared Receiver Testing Phase:",
        "Point IR LED towards the IR receiver",
        "Press any key to start."]
    )
    instructions_win.getch()
    
    def listen_for_signal():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        IR_RECEIVER = 15
        GPIO.setup(IR_RECEIVER, GPIO.IN)
        
        ir_receiver_working = False
        start_time = time()
        while time() - start_time < 2:
            shooter_value = InfraLib.getSignal(IR_RECEIVER)
            if shooter_value == "0xf1" + hex(uuid.getnode())[2:]:
                ir_receiver_working = True   
                break
            
        if ir_receiver_working == True:
            tests_status["Infrared_Receiver"] = 1
            draw_instructions(instructions_win,
                ["Infrared Receiver Testing Phase:",
                "It's working",
                "Press any key to continue."]
            )
        else:
            tests_status["Infrared_Receiver"] = -1
            draw_instructions(instructions_win,
                ["Infrared Receiver Testing Phase:",
                "It's not working",
                "Press any key to continue."]
            )
            
        GPIO.cleanup()
        draw_status(status_win)
        instructions_win.getch()
        
    listening_thread = threading.Thread(target=listen_for_signal)
    listening_thread.start()
    InfraLib.IRBlast(uuid.getnode(), "LASER")
    listening_thread.join()
        

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.mousemask(0)

    h, w = stdscr.getmaxyx()
    instructions_win = curses.newwin(h, w // 2, 0, 0)
    status_win = curses.newwin(h, w // 2, 0, w // 2)
    
    
    draw_instructions(instructions_win,
    ["This program aims to test every functionality of the robot.",
     "Each component will be tested sequentially.",
     "Press any key to start."]
    )
    draw_status(status_win)
    instructions_win.getch()
    
    #testServos(instructions_win, status_win)
    testInfraLED(instructions_win, status_win)
    testInfraReceiver(instructions_win, status_win)
    
    sleep(0.2)

    stdscr.addstr(h - 1, 0, "Test complete. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)