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


class GatlingDrone(EnemySprite):
    def __init__(self):
        super().__init__()
        self.image_clean = pygame.transform.flip(pygame.image.load(str(ROOTDIR/'Assets'/'Ships'/ "GatlingDrone.png")).convert_alpha(), False, True)
        self.image = self.image_clean.copy()
        self.mask = pygame.mask.from_surface(self.image, 1)
        self.rect = self.image.get_rect(center = (1000, 1000))

        self.animations = {}

        self.set_defaults()
        self.used_turret = self.used_turret_gen()


    def set_defaults(self):
        self.super_defaults()
        
        self.hp = 30
        self.shot_timer = 180
        self.cooldown = 120

        self.is_cooling_down = True

    
    def update(self):
        self.super_update()

        if self.is_cooling_down: self.cooldown_state()
        else: self.shooting_state()


    def shooting_state(self):
        self.shot_timer -= 1
        
        if self.shot_timer % 5 == 0:
            self.shoot()

        if self.shot_timer <= 0:
            self.shot_timer = 180
            self.is_cooling_down = True


    def cooldown_state(self):
        self.cooldown -= 1

        if self.cooldown == 0:
            self.cooldown = 120
            self.is_cooling_down = False


    def shoot(self):
            bullet = GAME.level.queues[BulletBasic].get()
            turret_pos = self.turret_positions[next(self.used_turret)]

            bullet.spawn((self.rect.centerx + turret_pos.x,
                        self.rect.centery + turret_pos.y))

            bullet.rotate(self.rotation)
            bullet.movement_pattern.change_angle(self.rotation)


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
        self.turret_positions = ( VectorPlus.from_angle(self.rotation - 20) * (self.rect.height / 2 + 3),
                                  VectorPlus.from_angle(self.rotation) * (self.rect.height / 2 + 3),
                                  VectorPlus.from_angle(self.rotation + 20) * (self.rect.height / 2 + 3) )


    def used_turret_gen(self):
        increment = 1
        val = 0

        while 1:
            if val == 0: increment = 1
            if val == 2: increment = -1

            yield val
            val += increment

