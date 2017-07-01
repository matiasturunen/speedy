import pygame

class Menu:
    _items = []
    screen = None
    itemSpacing = 5
    itemLeft = 5

    def addItem(self, menuItem):
        self._items.append(menuItem)

    def draw(self):
        if (self.screen is None):
            print('No screen to draw at!')
            return
        
        y0 = 5
        for i in self._items:
            # Menu box
            self.screen.rect(self.itemLeft, y0, 
                self.screen.SCREEN_WIDTH(), i.height, 
                i.backgroundColor()
            )

            # Actual text
            self.screen.text(i.title, 
                (self.itemLeft + i.margin, y0 + i.margin),
                color=i.textColor(),
                font=pygame.font.SysFont('sans-serif', i.fontHeight())
            )

            y0 += i.height + self.itemSpacing
            print('Paint', i.title)