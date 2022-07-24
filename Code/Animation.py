import os, sys
import pygame
from pygame.sprite import Sprite

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME


class Animation(Sprite):
    def __init__(self, source_folder):
        Sprite.__init__(self)
        self.frames = [pygame.image.load(f) for f in [i for i in os.listdir(source_folder) if os.isfile(os.join(source_folder, i))]]
        # self.get_frames(source_folder, file_name)
        self.current = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center = (200, 200))
        self.playing = True

    # def get_frames(self, source_folder, file_name):
    #     frames_amount = len([file for file in os.listdir(source_folder)])

    #     for i in range(1, frames_amount):
    #         self.frames.append(pygame.image.load(source_folder + "\\" + file_name + " (" + str(i) + ").png"))

    def update(self):
        if self.playing:
            self.current +=1

            if self.current == len(self.frames):
                self.current = 0

            self.image = self.frames[self.current]