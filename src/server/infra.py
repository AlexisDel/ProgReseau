import uuid
from src.rasptank import InfraLib
import RPi.GPIO as GPIO


def shoot():
    InfraLib.IRBlast(uuid.getnode(), "LASER")
    
if __name__ == '__main__':
    shoot()