import ui
import time

def createMenu():
    m = ui.Menu()
    m.screen = ui.Screen

    item = ui.MenuItem('Punainen')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((255,0,0))
    m.addItem(item)

    item = ui.MenuItem('Vihreä')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,255,0))
    m.addItem(item)

    item = ui.MenuItem('Sininen')
    item.setTextColor((0,0,0))
    item.setBackgroundColor((0,0,255))
    m.addItem(item)

    m.draw()

def main():
    createMenu()

if __name__ == '__main__':
    main()
    time.sleep(5)
