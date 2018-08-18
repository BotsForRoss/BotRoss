from xbox import Joystick

if __name__ == '__main__':
    xbox = Joystick()
    while not xbox.Back():
        print('Left X/Y: {}, {}'.format(xbox.leftX(), xbox.leftY()), end='')
