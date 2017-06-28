class MenuItem:
    title = 'MenuItem'
    _textColor = (0, 255, 0)
    _backgroundColor = (100, 100, 100)

    def __init__(self, title):
        self.title = title

    def textColor(self):
        return self.textColor

    def backgroundColor(self):
        return self._backgroundColor

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