import pygame
import sys
import os

# some useful constants
from pygame.locals import *

class FBScreen:
    # Screen size
    # Default for Adafruit PiTFT 2.2 (P2315)
    _SCREEN_WIDTH = 320
    _SCREEN_HEIGHT = 240

    screen = None

    def __init__(self):
        # Init the Screen

        os.putenv('SDL_FBDEV', '/dev/fb1')

        # select working framebuffer driver
        drivers = ['fbcon', 'directfb', 'svgalib']
        driverFound = False

        for driver in drivers:
            # make sure that env-var for SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)

            # Try to init display with current driver
            try:
                pygame.display.init()
            except pygame.error:
                print('driver %s failed.' % driver)
                continue

            # Found working driver
            driverFound = True
            print('Using driver %s.' % driver)
            break

        if not driverFound:
            raise Exception('No suitable video driver found')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))

        # Set display to screen dimensions and enable fullscreen
        self.screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT), pygame.FULLSCREEN)

        # Clear screen
        self.screen.fill((0,0,0))

        # Init fonts
        pygame.font.init()

        # Hide mouse
        pygame.mouse.set_visible(False)

        # Render the screen
        pygame.display.update()

    @property
    def SCREEN_WIDTH(self):
        return self._SCREEN_WIDTH

    @property
    def SCREEN_HEIGHT(self):
        return self._SCREEN_HEIGHT

    def __del__(self):
        # TODO: Make sure that pygame closes itself correctly...
        pass

    def rect(self, left, top, width, height, color, autoUpdate=True):
        """Draw rectanle to screen.

        Keyword arguments:
        left -- rectangle left edge
        top -- rectangle top edge
        width -- rectangle width
        height -- rectangle height
        color -- background color, tuple (r,g,b)
        autoUpdate -- If True, screen is updated after drawing
        """
        pygame.draw.rect(self.screen, color, (left, top, width, height))
        if (autoUpdate):
            pygame.display.update()

    def text(self, text, position=(0,0), color=(255,255,255), fontSize=15, font=None, autoUpdate=True):
        """Draw text to screen.

        Keyword arguments:
        text -- Actual text to draw
        position -- Position of text from top-left corner. (X,Y)
        color -- Text color, tuple (r,g,b)
        fontSize -- Size of font. Not used if font is set
        font -- Pygame font to use. Default pygame.font.SysFont("monospace", 15)
        """

        if (font is None):
            font = pygame.font.SysFont('monospace', fontSize, True)

        label = font.render(text, True, color)
        self.screen.blit(label, position)

        if (autoUpdate):
            pygame.display.update()

    def clear(self, autoUpdate=True):
        self.screen.fill((0,0,0))
        if (autoUpdate):
            pygame.display.update()

    def fill(self, color=(0,0,0), autoUpdate=True):
        self.screen.fill(color)
        if (autoUpdate):
            pygame.display.update()


# Make screen importable
Screen = FBScreen()