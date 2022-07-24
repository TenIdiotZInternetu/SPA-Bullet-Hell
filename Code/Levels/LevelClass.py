
import os, sys
import pygame
import queue
import time
import random
import subprocess

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Sprites.Player import PLAYER
from AppSettings import GAME
from UserInput import USERINPUT
from UI.LevelUI import LevelUI
from Sprites.BulletTypes import *
from Levels.Playfield import Playfield
from Sprites.Powerups import *
from Vectors import Vector2
from UI.PauseMenu import PauseMenu

from Sprites.Drone1 import Drone1
from Sprites.Drone2 import Drone2
from Sprites.DroneTurret import GatlingDrone
from Sprites.Minethrower import Minethrower
from Sprites.PulseThrower import PulseThrower



class Level():
    def __init__(self, id):
        self.id = id - 1
        self.UI = LevelUI()

        PLAYER.visible = 1

        self.all_sprites = pygame.sprite.LayeredDirty(PLAYER)
        self.queues = {}

        self.player_group = pygame.sprite.LayeredDirty(PLAYER)
        self.enemies_group = pygame.sprite.LayeredDirty()
        self.player_bullets_group = pygame.sprite.LayeredDirty()
        self.enemy_bullets_group = pygame.sprite.LayeredDirty()
        self.powerups_group = pygame.sprite.LayeredDirty()

        self.playfield = Playfield()

        self.cycle = 0
        self.is_running = True
        self.is_paused = False
        self.is_finished = False
        self.is_exited = False

        self.stage_events = [
            self.stage_1_events
        ]

        load_assets = [
            self.load_assets_stage_1
        ]

        self.load_assets = load_assets[self.id]

        self.all_sprites.clear(self.playfield.image, self.playfield.bg)

        self.t = time.time()


    def launch_stage(self):
        while self.is_running:
            GAME.CLOCK.tick(GAME.FPS)
            USERINPUT.update()

            if self.is_paused: PauseMenu.show()

            self.update_loop()
            self.stage_events[self.id]()
            self.detect_collisions()
            self.draw_on_screen()

            self.cycle += 1


    def update_loop(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            if USERINPUT.BUTTON_START:
                pygame.display.quit()
                subprocess.call("python3 /home/pi/GUI/Startup.py", shell=True)
                pygame.quit()

            
            self.all_sprites.update()

            if PLAYER.bomb_is_active:
                if self.cycle % 5  == 0:
                    for enemy in self.enemies_group:
                        enemy.take_damage(4)

                bullets = self.enemy_bullets_group.sprites()

                if len(bullets) > 0 and self.cycle % 2  == 0:
                    bullets[random.randint(0, len(bullets) - 1)].despawn()

            self.UI.score_counter.update_score(PLAYER.hp)


    def detect_collisions(self):
        for enemy in self.enemies_group:
            for bullet in pygame.sprite.spritecollide(enemy, self.player_bullets_group, False, collided=pygame.sprite.collide_mask):
                enemy.take_damage(bullet.damage)

                if bullet.destructable: bullet.despawn()

            if (pygame.Rect.colliderect(PLAYER.hitbox, enemy)
                and not PLAYER.is_invincible):
                enemy.take_damage(50)
                PLAYER.take_damage()

        for bullet in self.enemy_bullets_group:
            if pygame.Rect.colliderect(PLAYER.hitbox, bullet):
                PLAYER.take_damage()
                
                if bullet.destructable: bullet.despawn()

        for powerup in self.powerups_group:
            if pygame.Rect.colliderect(PLAYER.rect, powerup):
                powerup.use()


        if PLAYER.rect.bottom > self.playfield.rect.height: PLAYER.rect.bottom = self.playfield.rect.height
        if PLAYER.rect.top < 0: PLAYER.rect.top = 0
        if PLAYER.rect.left < 0: PLAYER.rect.left = 0
        if PLAYER.rect.right > self.playfield.rect.width: PLAYER.rect.right = self.playfield.rect.width

    
    def draw_on_screen(self):
        self.all_sprites.draw(self.playfield.image)
        rects = self.playfield.draw()
        pygame.display.update(rects)

        rects = self.UI.draw(GAME.SCREEN)
        pygame.display.update(rects)

    
    def load_asset(self, sprite_class, count):
        self.queues[sprite_class] = queue.Queue()

        for i in range(count):
            self.queues[sprite_class].put(sprite_class())


    # ----- Stage Specific -------------------------------------------------------- #
    def load_assets_stage_1(self):
        self.load_asset(BulletBasic, 200)
        self.load_asset(BulletBasicFriendly, 40)
        self.load_asset(HomingOrb, 40)
        self.load_asset(Bomb, 5)

        self.load_asset(Drone1, 50)
        self.load_asset(Drone2, 25)
        self.load_asset(GatlingDrone, 25)

        self.load_asset(Minethrower, 5)
        self.load_asset(PulseThrower, 20)

        self.load_asset(Powerup, 100)
        self.load_asset(HPup, 3)
        self.load_asset(Bombup, 3)

        self.gatling = None


    def stage_1_events(self):

        if self.cycle % 20 == 0 and self.cycle < 120:
            enemy = enemy = self.queues[Drone1].get()
            enemy.spawn((100, 200), MP.Sine(enemy, 350, 0.75, 60, 2))
            enemy.rotate([20])

        if self.cycle % 20 == 0 and self.cycle > 100 and self.cycle < 220:
            enemy = enemy = self.queues[Drone1].get()
            enemy.spawn((380, 250), MP.Sine(enemy, 190, 0.75, 60, 2))
            enemy.rotate([-20])

        if self.cycle == 9:
            enemy = self.queues[Minethrower].get()
            enemy.spawn((250, 120), MP.Linear(enemy, 0, 0))

        if self.cycle % 600 == 0 and self.cycle < 1800:
            pf = self.playfield.rect

            enemy = self.queues[PulseThrower].get()
            enemy.spawn((pf.centerx, 40), MP.Sine(enemy, 90, 0, pf.width / 2 - 15, 0.5))

            enemy = self.queues[PulseThrower].get()
            enemy.spawn((pf.centerx, 40), MP.Sine(enemy, -90, 0, pf.width / 2 - 15, 0.5))

        if self.cycle == 660 and self.gatling is None:
            pf = self.playfield.rect
            self.gatling = self.queues[GatlingDrone].get()
            self.gatling.spawn((-10, pf.centery), MP.Linear(self.gatling, 0, 2, -0.032))
            self.gatling.rotate([-130])

        if self.gatling is not None:
            if self.gatling.is_cooling_down:
                self.gatling.rotate([-2])
            else:
                self.gatling.rotate([2])



            
