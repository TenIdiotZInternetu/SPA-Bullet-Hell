import pygame
import platform
import os
from AppSettings import GAME

if platform.system() == "Linux":
    from gpiozero import MCP3008
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # spi = busio.SPI(clock=board.D11, MISO=board.D9, MOSI=board.D10)
    # cs = digitalio.DigitalInOut(board.D8)
    # mcp = MCP.MCP3008(spi, cs)
    


class UserInput():

    def __init__(self):
        self.JOYSTICK_UP = 0
        self.JOYSTICK_DOWN = 0
        self.JOYSTICK_LEFT = 0
        self.JOYSTICK_RIGHT = 0

        self.BUTTON_A = 0
        self.BUTTON_B = 0
        self.BUTTON_X = 0
        self.BUTTON_Y = 0

        self.BUTTON_START = 0
        self.BUTTON_SELECT = 0
        self.BUTTON_JOYSTICK = 0

        self.f = pygame.font.SysFont("Calibri", 40)

        if platform.system() == "Linux":
            self.update = self.updateRPi
        elif platform.system() == "Windows":
            self.update = self.updateWindows


    def updateWindows(self):
        keys = pygame.key.get_pressed()

        self.JOYSTICK_UP = 1 if keys[pygame.K_w] else 0
        self.JOYSTICK_DOWN = 1 if keys[pygame.K_s] else 0
        self.JOYSTICK_LEFT = 1 if keys[pygame.K_a] else 0
        self.JOYSTICK_RIGHT = 1 if keys[pygame.K_d] else 0

        self.BUTTON_A = bool(keys[pygame.K_k])
        self.BUTTON_B = bool(keys[pygame.K_l])
        self.BUTTON_X = bool(keys[pygame.K_j])
        self.BUTTON_Y = bool(keys[pygame.K_i])

        self.BUTTON_START = bool(keys[pygame.K_p])
        self.BUTTON_SELECT = bool(keys[pygame.K_o])
        self.BUTTON_JOYSTICK = bool(keys[pygame.K_SPACE])


    def updateRPi(self):
        keys = pygame.key.get_pressed()
        
        self.JOYSTICK_UP = 1 if keys[pygame.K_UP] else 0
        self.JOYSTICK_DOWN = 1 if keys[pygame.K_DOWN] else 0
        self.JOYSTICK_LEFT = 1 if keys[pygame.K_LEFT] else 0
        self.JOYSTICK_RIGHT = 1 if keys[pygame.K_RIGHT] else 0

        self.BUTTON_A = bool(keys[pygame.K_RETURN])
        self.BUTTON_B = bool(keys[pygame.K_l])
        self.BUTTON_X = bool(keys[pygame.K_SPACE])
        self.BUTTON_Y = bool(keys[pygame.K_i])

        self.BUTTON_START = bool(keys[pygame.K_ESCAPE])
        self.BUTTON_SELECT = bool(keys[pygame.K_TAB])
        self.BUTTON_JOYSTICK = bool(keys[pygame.K_z])


USERINPUT = UserInput()
