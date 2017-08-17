MenuItemId = 1
class MenuItem:
    title = 'MenuItem'
    _textColor = (0, 255, 0)
    _backgroundColor = (100, 100, 100)
    _borderColor = (255,255,255)
    _action = None
    height = 30
    margin = 5
    _id = None
    parent = 0
    _actionType = None

    def __init__(self, title, id=None):
        global MenuItemId
        self.title = title
        #self._id = id
        self._id = MenuItemId
        MenuItemId += 1

    @property
    def textColor(self):
        return self._textColor

    @property
    def backgroundColor(self):
        return self._backgroundColor

    @property
    def borderColor(self):
        return self._borderColor

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

    def setBorderColor(self, color):
        if (not self._isColor(color)):
            raise ValueError('Invalid RGB color value!')
        else:
            self._borderColor = color

    def setAction(self, act, atype='mod'):
        """Set mod start function for this item"""
        self._action = act
        self._actionType = atype

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

    @property
    def actionType(self):
        return self._actionType
    

    def __gt__(self, other):
        return self._id > other.id
