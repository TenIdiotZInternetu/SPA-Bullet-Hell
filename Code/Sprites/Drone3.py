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


class Drone3(EnemySprite):
    def __init__(self):
        super().__init__()
        self.image_clean = pygame.transform.flip(pygame.image.load(str(ROOTDIR/'Assets'/'Ships'/ "Player.png")).convert_alpha(), False, True)
        self.image = self.image_clean.copy()
        self.mask = pygame.mask.from_surface(self.image, 1)
        self.rect = self.image.get_rect(center = (1000, 1000))

        self.animations = {}

        self.set_defaults()


    def set_defaults(self):
        self.super_defaults()
        
        self.hp = 15
        self.shot_timer = 60

    
    def update(self):
        self.super_update()
        
        self.shot_timer -= 1
        
        if self.shot_timer == 0:
            
            self.shoot()
            self.shot_timer = 60


    def shoot(self):
        angles = (-40, 0, 40)

        for i in range(3):
            bullet = GAME.level.queues[BulletBasic].get()
            turret_pos = self.turret_vectors[i]
        
            bullet.spawn((self.rect.centerx + turret_pos.x,
                        self.rect.centery + turret_pos.y))

            bullet.rotate(self.rotation + angles[i])
            bullet.movement_pattern.change_angle(self.rotation + angles[i])


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
        self.turret_vectors = ( VectorPlus.from_angle(self.rotation - 40)  * (self.rect.height / 2 + 3),
                                VectorPlus.from_angle(self.rotation)  * (self.rect.height / 2 + 3),
                                VectorPlus.from_angle(self.rotation + 40)  * (self.rect.height / 2 + 3) )

