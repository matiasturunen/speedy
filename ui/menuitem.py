class MenuItem:
    title = 'MenuItem'
    _textColor = (0, 255, 0)
    _backgroundColor = (100, 100, 100)
    _action = None
    height = 30
    margin = 5
    _id = None

    def __init__(self, title, id=None):
        self.title = title
        self._id = id

    @property
    def textColor(self):
        return self._textColor

    @property
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

    def setAction(self, act):
        self._action = act

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

    @property
    def fontHeight(self):
        """Get maximum font height that can be used in this item"""
        return self.height - (2 * self.margin)

    @property
    def id(self):
        return self._id


