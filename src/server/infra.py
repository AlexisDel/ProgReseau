import uuid
from rasptank import InfraLib


def shoot():
    InfraLib.IRBlast(uuid.getnode(), "LASER")

if __name__ == '__main__':
    shoot()