import RPi.GPIO as GPIO

import ui
import time
import mod

# Use physical buttons
buttons = True
btnlist = {
    12: 'RIGHT',    # 4 on keypad
    13: 'LEFT',     # 3 on keypad
    15: 'DOWN',     # 2 on keypad
    16: 'UP'        # 1 on keypad
}

def createMenu():
    m = ui.menu
    m.screen = ui.Screen


    item = ui.MenuItem('Nopeus')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,0,0))
    item.active = True
    m.addItem(item)

    item = ui.MenuItem('Sää')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,255,0))
    m.addItem(item)

    item = ui.MenuItem('Kello')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,0,255))
    item.setAction(mod.clock.start)
    m.addItem(item)

    asetukset = ui.MenuItem('Asetukset')
    asetukset.setTextColor((0,0,0))
    asetukset.setBackgroundColor((255,255,0))
    m.addItem(asetukset)

    kelloasetus = ui.MenuItem('Kello')
    kelloasetus.setTextColor((0,0,0))
    kelloasetus.setBackgroundColor((255,255,0))
    kelloasetus.parent = asetukset.id
    m.addItem(kelloasetus)

    item = ui.MenuItem('Tunnit')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,255,0))
    item.parent = kelloasetus.id
    m.addItem(item)

    item = ui.MenuItem('Minuutit')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,255,0))
    item.parent = kelloasetus.id
    m.addItem(item)

    item = ui.MenuItem('Nopeus')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,255,0))
    item.parent = asetukset.id
    m.addItem(item)

    m.draw()


def initButtons():
    GPIO.setmode(GPIO.BOARD)
    for btn in btnlist.keys():
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def main():
    createMenu()
    initButtons()
    time.sleep(2)
    


if __name__ == '__main__':
    main()

    while True:
        if (buttons):
            try:
                for btn in btnlist.keys():
                    if (GPIO.input(btn) == False):
                        direction = btnlist[btn]
                        if (direction == 'UP'):
                            ui.menu.Up()
                        elif (direction == 'DOWN'):
                            ui.menu.Down()
                        elif (direction == 'LEFT'):
                            ui.menu.Left()
                        elif (direction == 'RIGHT'):
                            ui.menu.Right()
                        time.sleep(0.5)

            except Exception as e:
                print('Buttons error:', e)

        else:
            inp = input('Valinta: ')
            if(inp.upper() == 'W'):
                ui.menu.Up()
            elif(inp.upper() == 'A'):
                ui.menu.Left()
            elif(inp.upper() == 'S'):
                ui.menu.Down()
            elif(inp.upper() == 'D'):
                ui.menu.Right()
            else:
                print('invalid')


