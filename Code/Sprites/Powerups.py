from abc import abstractclassmethod
import pygame
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Sprites.Player import PLAYER
from AppSettings import GAME, ROOTDIR
from pygame.sprite import DirtySprite
import MovementPatterns as MP


class Upgrade(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = pygame.image.load(str(ROOTDIR/'Assets'/'Placeholders'/ 'powerup.png')).convert_alpha()
        self.rect = self.image.get_rect(center = (1000, 1000))

        self.movement_pattern = MP.Linear(self, 90, 1)

        self.is_moving = True

    
    def update(self):
        borders = GAME.level.playfield.rect
        self.dirty = 1

        if (self.rect.bottom + self.rect.height + 10 < borders.top
                or self.rect.top - self.rect.height - 10 > borders.bottom
                or self.rect.left + self.rect.width + 10 < borders.left
                or self.rect.right - self.rect.width - 10 > borders.right):
            self.despawn()

        if self.is_moving:
            self.rect.center = self.movement_pattern.update()


    def spawn(self, position):
        GAME.level.powerups_group.add(self)
        GAME.level.all_sprites.add(self)
        GAME.level.all_sprites.change_layer(self, 1)
        
        self.rect.center = position
        self.dirty = 1


    def despawn(self):
        GAME.level.queues[type(self)].put(self)
        GAME.level.powerups_group.remove(self)
        GAME.level.all_sprites.remove(self)

    
    @abstractclassmethod
    def use(self):
        pass


class HPup(Upgrade):
    def __init__(self):
        Upgrade.__init__(self)


    def use(self):
        PLAYER.hp = min(5, PLAYER.hp + 1)
        GAME.level.UI.update_item_count("hp")
        self.despawn()


class Bombup(Upgrade):
    def __init__(self):
        Upgrade.__init__(self)


    def use(self):
        PLAYER.bombs = min(5, PLAYER.bombs + 1)
        GAME.level.UI.update_item_count("bombs")
        self.despawn()


class Powerup(Upgrade):
    def __init__(self):
        Upgrade.__init__(self)
        self.movement_pattern = MP.Linear(self, 90, 3, 0.05)


    def use(self):
        PLAYER.power_level = min(200, PLAYER.power_level + 1)
        GAME.level.UI.power_gauge.update_power()
        self.despawn() 

        