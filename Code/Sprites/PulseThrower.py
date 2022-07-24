import os, sys, pathlib
import pygame
import math

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

filepath = pathlib.Path(__file__).parent

from AppSettings import GAME
from Sprites.Enemy import EnemySprite
from Sprites.BulletTypes import *
from Sprites.Powerups import *
import MovementPatterns as MP
from Vectors import VectorPlus
from AppSettings import ROOTDIR


class PulseThrower(EnemySprite):
    def __init__(self):
        super().__init__()
        self.image_clean = pygame.transform.flip(pygame.image.load(str(ROOTDIR/'Assets'/'Ships'/ "PulseThrower.png")).convert_alpha(), False, True)
        self.image = self.image_clean.copy()
        self.mask = pygame.mask.from_surface(self.image, 1)
        self.rect = self.image.get_rect(center = (1000, 1000))

        self.animations = {}

        self.set_defaults()


    def set_defaults(self):
        self.super_defaults()
        
        self.hp = 20
        self.shot_timer = 300
        

    
    def update(self):
        self.super_update()
        
        self.rot_vector = VectorPlus.from_angle(self.rotation) * (self.rect.height / 2 + 3)
        self.shot_timer -= 1
        
        if self.shot_timer == 0:
            self.shoot()
            self.shot_timer = 300
        

    def shoot(self):
        bullet = GAME.level.queues[HomingOrb].get()

        bullet.spawn((self.rect.centerx + self.rot_vector.x,
                      self.rect.centery + self.rot_vector.y))

        #bullet.rotate(self.rotation)
        #bullet.movement_pattern.change_angle(self.rotation)
        self.shot_timer = GAME.level.cycle


    def spawn(self, position, mp):
        self.super_spawn(position)
        self.movement_pattern = mp
        mp.init_vector()


    def die(self):
        GAME.level.UI.score_counter.update_score(400)

        powerup = GAME.level.queues[Powerup].get()
        powerup.spawn(self.rect.center)

        self.despawn()
        

    def set_turret_positions(self):
        self.rot_vector = VectorPlus.from_angle(self.rotation) * (self.rect.height / 2 + 3)
