import pygame
import math
from copy import copy
import os

from pygame.math import Vector2


class VectorPlus(pygame.math.Vector2):
    def get_angle(vector):
        ref = pygame.Vector2(1, 0)
        dif = ref.angle_to(vector)

        return dif if dif > 0 else 360 + dif


    def get_perpendicular(vector):
        perp = copy(vector)
        perp.rotate_ip(90)
        return perp


    def from_angle(angle):
        angle = math.radians(angle)
        return VectorPlus(math.cos(angle), math.sin(angle)).normalize()


