import uuid
from src.rasptank import InfraLib
import RPi.GPIO as GPIO


def shoot():
    print(f"I'm {uuid.getnode()} ans i shoot")
    InfraLib.IRBlast(uuid.getnode(), "LASER")
    
if __name__ == '__main__':
    shoot()