import pygame

class Node:
    nex = None
    prev = None
    item = None

    def __init__(self, item):
        self.nex = None
        self.prev = None
        self.item = item


class Menu:
    _items = []
    screen = None
    itemSpacing = 5
    itemLeft = 5
    itemRight = 5
    _currentLevel = 0
    _currentItemId = None
    _activeMods = []

    def addItem(self, menuItem):
        self._items.append(menuItem)
        if(self._currentItemId == None):
            self._currentItemId = menuItem.id
        
    def draw(self):
        """Draw current menu level to screen
        """
        if (self.screen is None):
            print('No screen to draw at!')
            return
        
        y0 = 5
        itemBorderWidth = 2
        itemWidth = self.screen.SCREEN_WIDTH - self.itemLeft - self.itemRight
        print('Current item:', self._currentItemId)
        for i in self._items:
            if (i.parent != self._currentLevel):
                # Skip all that are not in current level
                continue
            # Menu box
            self.screen.rect(self.itemLeft, y0, 
                itemWidth, i.height, 
                i.backgroundColor
            )

            if (i.id == self._currentItemId):
                # white border
                self.screen.rect(self.itemLeft, y0, 
                    itemWidth-itemBorderWidth, i.height-itemBorderWidth+1, 
                    i.borderColor, borderWidth=itemBorderWidth
                )

            # Actual text
            self.screen.text(i.title, 
                (self.itemLeft + i.margin, y0 + i.margin),
                color=i.textColor,
                font=pygame.font.SysFont('sans-serif', i.fontHeight)
            )

            y0 += i.height + self.itemSpacing
            print('Paint', i.title, 'id:',i.id, 'parent:',i.parent)

    def selectItem(self, id):
        for i in self._items:
            if (i.id == id):
                i.action()
                return
        print('Invalid id')
        return

    def _getPrevItem(self, id, level):
        arr = sorted(self._items)

        prev = None
        for i in arr:
            if (i.parent != level):
                continue # Skip all that are not in current level
            if (i.id == id and prev == None): #First item
                return i
            elif (i.id == id):
                return prev
            prev = i

    def _getNextItem(self, id, level):
        arr = sorted(self._items, reverse=True)

        prev = None
        for i in arr:
            if (i.parent != level):
                continue # Skip all that are not in current level
            if (i.id == id and prev == None): #First item is sorted arr, but actually last
                return i
            elif (i.id == id):
                return prev
            prev = i

    def _getItemChilds(self, id):
        childs = []
        for i in self._items:
            if (i.parent == id):
                childs.append(i)
        return childs

    def _getItem(self, id):
        for i in self._items:
            if (i.id == id):
                return i

    def Up(self):
        self._currentItemId = self._getPrevItem(self._currentItemId, self._currentLevel).id
        self.draw()

    def Down(self):
        self._currentItemId = self._getNextItem(self._currentItemId, self._currentLevel).id
        self.draw()

    def Left(self):
        if (self.modActive):
            for m in self._activeMods:
                m.stop()
            self.draw()
        else:
            if (self._currentLevel != 0):
                item = self._getItem(self._currentItemId)
                self._currentLevel = item.parent
            self.draw()

    def Right(self):
        childs = self._getItemChilds(self._currentItemId)
        if (len(childs) == 0):
            self._modActive = True
            self.selectItem(self._currentItemId)
        else:
            self._currentLevel = self._currentItemId
            self.draw()

    @property
    def modActive(self):
        return len(self._activeMods) == 0

menu = Menu()
