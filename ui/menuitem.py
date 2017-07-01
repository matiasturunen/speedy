class MenuItem:
    title = 'MenuItem'
    _textColor = (0, 255, 0)
    _backgroundColor = (100, 100, 100)
    _action = None
    height = 30
    margin = 5

    def __init__(self, title):
        self.title = title

    def textColor(self):
        return self._textColor

    def backgroundColor(self):
        return self._backgroundColor

    def action(self):
        if (self._action is not None):
            self._action()

    def setTextColor(self, color):
        if (not self._isColor(color)):
            raise ValueError('Invalid RGB color value!')
        else:
            self._textColor = color

    def setBackgroundColor(self, color):
        if (not self._isColor(color)):
            raise ValueError('Invalid RGB color value!')
        else:
            self._backgroundColor = color        

    def _isColor(self, color):
        # Check if color is valid
        if (len(color) == 3):
            for c in color:
                c = int(c)
                if (c < 0 or c > 255):
                    return False
            return True
        else:
            return False

    def fontHeight(self):
        """Get maximum font height that can be used in this item"""
        return self.height - (2 * self.margin)


