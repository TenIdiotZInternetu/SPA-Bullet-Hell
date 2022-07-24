from abc import abstractclassmethod
import pygame
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from pygame.sprite import DirtySprite
from AppSettings import GAME, ROOTDIR
import Sprites.Player
import MovementPatterns as MP


class Bullet(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.dirty = 0
        self.rect = None
        self.destructable = True
        
        self.super_defaults()


    def super_defaults(self):
        self.rotation = 0

    
    def super_update(self):
        borders = GAME.level.playfield.rect
        self.dirty = 1

        if (self.rect.bottom + self.rect.height + 10 < borders.top
                or self.rect.top - self.rect.height - 10 > borders.bottom
                or self.rect.left + self.rect.width + 40 < borders.left
                or self.rect.right - self.rect.width - 10 > borders.right):

            self.despawn()


    def super_spawn(self, position):
        GAME.level.all_sprites.add(self)
        self.rect.center = position
        self.dirty = 1


    def rotate(self, angle):
        self.rotation += angle
        center = self.rect.center
        self.image = pygame.transform.rotate(self.image, -self.rotation + 90)
        self.image.get_rect(center = center)


class BulletBasic(Bullet):
    def __init__(self) -> None:
        Bullet.__init__(self)
        self.image = pygame.image.load(str(ROOTDIR/'Assets'/'Bullets'/ "Enemy_bullet.png")).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (1000, 1000))

    def update(self):
        self.super_update()
        self.rect.center = self.movement_pattern.update()


    def spawn(self, position, angle=90):
        self.super_spawn(position)
        self.movement_pattern = MP.Linear(self, angle, 1, 0.04)
        GAME.level.enemy_bullets_group.add(self)


    def despawn(self):
        GAME.level.queues[BulletBasic].put(self)
        GAME.level.enemy_bullets_group.remove(self)
        GAME.level.all_sprites.remove(self)

        self.super_defaults()


class BulletBasicFriendly(BulletBasic):
    def __init__(self):
        BulletBasic.__init__(self)
        self.image = pygame.image.load(str(ROOTDIR/'Assets'/'Bullets'/ "Player_bullet.png")).convert_alpha()
        self.movement_pattern = MP.Linear(self, 270, 10)
        
        self.damage = 1

    
    def spawn(self, position):
        self.super_spawn(position)
        GAME.level.player_bullets_group.add(self)
        

    def despawn(self):
        GAME.level.queues[BulletBasicFriendly].put(self)
        GAME.level.player_bullets_group.remove(self)
        GAME.level.all_sprites.remove(self)

        self.super_defaults()

        
class HomingOrb(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = pygame.image.load(str(ROOTDIR/'Assets'/'Placeholders'/ "homer.png")).convert_alpha()
        self.rect = self.image.get_rect(center = (1000, 1000))


    def update(self):
        self.super_update()
        self.rect.center = self.movement_pattern.update()


    def spawn(self, position):
        self.super_spawn(position)
        self.movement_pattern = MP.Chasing(self, 1.3, Sprites.Player.PLAYER, 150)
        GAME.level.enemy_bullets_group.add(self)

    
    def despawn(self):
        GAME.level.queues[HomingOrb].put(self)
        GAME.level.enemy_bullets_group.remove(self)
        GAME.level.all_sprites.remove(self)

        self.super_defaults()


class Bomb(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.destructable = False
        self.shell_img = pygame.image.load(str(ROOTDIR/'Assets'/'Bullets'/ "Bomb_Shell.png")).convert_alpha()
        self.aoe_img = pygame.image.load(str(ROOTDIR/'Assets'/'Bullets'/ "Bomb_AOE.png")).convert_alpha()

        self.shell_img = pygame.transform.scale(self.shell_img, (20,20))
        self.aoe_img = pygame.transform.scale(self.aoe_img, (100,100))

        self.set_defaults()
        

    def set_defaults(self):
        self.super_defaults()
        self.alpha = 255
        self.is_exploded = False
        self.image = self.shell_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (1000, 1000))


    def update(self):
        self.super_update()

        if not self.is_exploded:
            self.rect.center = self.movement_pattern.update()

            if self.movement_pattern.speed < 0.05:
                self.is_exploded = True
                self.image = self.aoe_img
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.aoe_img.get_rect(center = self.rect.center)

        if self.is_exploded and GAME.level.cycle % 3 == 0:
            self.alpha -= 3
            self.image.set_alpha(self.alpha)

        if self.alpha == 0:
            self.despawn()


    def spawn(self, position):
        self.super_spawn(position)
        self.movement_pattern = MP.Homing(self, 3, Sprites.Player.PLAYER, -0.03)
        GAME.level.enemy_bullets_group.add(self)


    def despawn(self):
        GAME.level.queues[Bomb].put(self)
        GAME.level.enemy_bullets_group.remove(self)
        GAME.level.all_sprites.remove(self)

        self.set_defaults()