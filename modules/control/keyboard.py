from misc.getch import _Getch


class Keyboard():
    """Navigate the robosub using keyboard controls
    w: forwards
    a: counter-clockwise
    s: backwards
    d: clockwise
    q: left
    e: right
    r: up
    f: down
    [0-9]: power
    m: muliplier
    x: exit
    """

    def __init__(self):
        self.is_killswitch_on = False

    def getch(self):
        """Gets keyboard input if killswitch is plugged in"""

        getch = _Getch()
        accepted = ['w', 'a', 's', 'd', 'q', 'e', 'r', 'f']
        response = ''
        char = 0
        power = 1
        multiplier = 1

        if self.is_killswitch_on:
            print(
                '\
                \nw: forwards\
                \na: counter-clockwise\
                \ns: backwards\
                \nd: clockwise\
                \nq: left\
                \ne: right\
                \nr: up\
                \nf: down\
                \n[0-9]: power\
                \nm: muliplier\
                \nx: exit')

            while char != 'x':
                char = getch()

                if char in accepted:
                    self.navigate(char, power, multiplier)
                elif char.isdigit():
                    power = char
                    print('power is changed to %s' % power)
                elif char == 'm':
                    while not response.isdigit():
                        response = raw_input('\nEnter a number for multiplier: ')

                    multiplier = response
                    response = ''
                    print('multiplier is changed to %s' % multiplier)

        else:
            print('Magnet is not plugged in.')

    def navigate(self, char, power, multiplier):
        """Navigates robosub with given character input, power, and multiplier"""

        if char == 'w':
            print('forwards')
        elif char == 'a':
            print('counter-clockwise')
        elif char == 's':
            print('backwards')
        elif char == 'd':
            print('clockwise')
        elif char == 'q':
            print('left')
        elif char == 'e':
            print('right')
        elif char == 'r':
            print('up')
        elif char == 'f':
            print('down')

    def start(self):
        """Allows keyboard navigation when killswitch is plugged in"""

        self.is_killswitch_on = True

    def stop(self):
        """Stops keyboard navigation when killswitch is unplugged"""

        self.is_killswitch_on = False
