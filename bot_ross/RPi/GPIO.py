BOARD = 1
OUT = 1
IN = 1
LOW = 1
BCM = 1

def setmode(a):
    print(a)

def setup(a, b):
    print(a)

def output(a, b):
    print(a)

def cleanup():
    print('mock GPIO cleaned up')

def setmode(a):
    print(a)

def setwarnings(flag):
    print('mock GPIO set warnings')

def input(pin, something=False):
    return True
