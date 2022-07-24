import os, sys, pathlib
import pygame
from pygame.sprite import DirtySprite

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from UserInput import USERINPUT
from Sprites.BulletTypes import *
from AppSettings import GAME, ROOTDIR


class Player(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)

        # Na image je po nahraní obrázku dôležité zavolať funkciu convert_alpha()
        # Tá zmení obrázok na Pygamu ľahšie čítateľný formát. Mnohonásobne to zvyšuje rýchlosť procesov
        self.image = pygame.image.load(str(ROOTDIR/'Assets'/'Ships'/ "Player.png")).convert_alpha()

        # Umiestnenie lode a jej hitboxu na hracie pole
        self.rect = self.image.get_rect(center = (400, 300))
        self.hitbox = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 2, 5, 5)

        self.hp = 3                             # Body zdravia
        self.bombs = 2                          # Počet držaných bomb
        self.power_level = 0                    # Úroveň postavy, mení režim streľby

        self.i_frames = 0                       # Zostávajúci počet snímkov nezraniteľnosti
        self.bomb_is_active = False             # Stav použitia bomby
        self.bomb_timer = -1                    # Zostávajúci čas aktívnosti bomby

        self.movement_speed = 5                 # Rýchlosť pohybu postavy
        self.shooting_mode = self.bullet_basic1 # Režim streľby
        self.shot_timer = 0                     # Oneskorenie medzi vystrelenými projektilmi
        
        self.is_moving = False                  # Postava sa hýbe
        self.is_shooting = False                # Postava strieľa
        self.is_active = True                   # Postavou sa dá hýbať
        self.is_invincible = False              # Postava je nezraniteľná

        self.dirty = 2                          
        self.visible = 0
        self.alpha = 255

        


    def update(self):
        if not self.is_active: return
        
        self.control_player()

        if self.i_frames > 0:
            self.is_invincible = True
            self.i_frames -= 1

            if self.i_frames % 35 == 0: 
                self.alpha = 100
            else: self.alpha += 5

            if self.i_frames == 0:
                self.is_invincible = False
                self.bomb_is_active = False
                self.alpha = 255

            if self.bomb_timer > 0:
                self.bomb_timer -= 1

                if self.bomb_timer == 0: 
                    self.bomb_is_active = True

        if self.is_moving:
            self.rect = self.image.get_rect(center = self.rect.center)

        self.image.set_alpha(self.alpha)

        
    def control_player(self):
        original_pos = self.rect.center

        self.rect.top -= self.movement_speed * USERINPUT.JOYSTICK_UP
        self.rect.top += self.movement_speed * USERINPUT.JOYSTICK_DOWN

        if USERINPUT.JOYSTICK_LEFT > 0.1: 
            self.rect.left -= self.movement_speed * USERINPUT.JOYSTICK_LEFT
        
        if USERINPUT.JOYSTICK_RIGHT > 0.1: 
            self.rect.left += self.movement_speed * USERINPUT.JOYSTICK_RIGHT

        if USERINPUT.BUTTON_A:
            self.shooting_mode()

        if USERINPUT.BUTTON_B:
            self.release_bomb()

        if original_pos != self.rect.center: 
            self.is_moving = True
            self.hitbox = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 2, 5, 5)

    
    def take_damage(self):
        if self.is_invincible: return

        self.hp -= 1
        GAME.level.UI.update_item_count("hp")
        self.alpha = 100

        self.invincibility_timer = GAME.level.cycle
        self.is_invincible = True

        self.i_frames = 180


    def release_bomb(self):
        if self.is_invincible: return
        if self.bombs < 1: return

        self.bombs -= 1
        GAME.level.UI.update_item_count("bombs")
        self.alpha = 100

        self.invincibility_timer = GAME.level.cycle
        self.is_invincible = True

        self.i_frames = 300
        self.bomb_timer = 60

        GAME.level.UI.score_counter.update_score(-2000)


    def bullet_basic1(self):
        if GAME.level.cycle - self.shot_timer < 5:
            return

        bullet = GAME.level.queues[BulletBasicFriendly].get()
        bullet.spawn((self.rect.midleft[0] + 2, self.rect.centery))

        bullet = GAME.level.queues[BulletBasicFriendly].get()
        bullet.spawn((self.rect.midright[0] - 2, self.rect.centery))

        self.shot_timer = GAME.level.cycle


PLAYER = Player()


