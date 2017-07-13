import ui
import time
import mod

def createMenu():
    m = ui.menu
    m.screen = ui.Screen

    item = ui.MenuItem('Punainen', id=0)
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,0,0))
    m.addItem(item)

    item = ui.MenuItem('Vihrea', id=1)
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,255,0))
    m.addItem(item)

    item = ui.MenuItem('Kello', id=2)
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,0,255))
    item.setAction(mod.clock.start)
    m.addItem(item)

    m.draw()

def main():
    createMenu()
    time.sleep(1)
    ui.menu.selectItem(2)

if __name__ == '__main__':
    main()
    while True:
        pass
