from abc import abstractclassmethod
import os, sys
import pygame
from pygame.sprite import DirtySprite

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME
import MovementPatterns as MP


class EnemySprite(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = None
        self.rect = None

        self.dirty = 2

    # Nastaví východzie hodnoty vlastností, keď je
    # objekt prvý krát inicializovaný, alebo odstránený z groups
    def super_defaults(self):
        self.alpha = 255
        self.rotation = 90
        self.hit_timer = 0
        self.is_moving = True
        self.spawned = False

        self.event_timer = 0
        self.event_list = {}

        self.rect = self.image.get_rect(center = (1000, 1000))
        self.set_turret_positions()

    # Odstránenie objektov za hranicou playfieldu,
    # úprava priehľadnosti, zmena polohy podľa spôsobu pohybu
    def super_update(self):
        borders = GAME.level.playfield.rect
        self.dirty = 1

        if (self.rect.bottom + self.rect.height + 10 < borders.top
                or self.rect.top - self.rect.height - 10 > borders.bottom
                or self.rect.right + self.rect.width + 10 < borders.left
                or self.rect.left - self.rect.width - 10 > borders.right):
            self.despawn()

        if self.alpha < 255:
            self.alpha += 10

        if self.event_list != {}: self.execute_events()
        if self.is_moving: self.rect.center = self.movement_pattern.update()

        self.image.set_alpha(self.alpha)
        self.event_timer += 1

    # Zníženie zdravia po zásahu projektilom
    def take_damage(self, amount):
        self.hp -= amount

        if self.hp <= 0:
            self.die()

        if GAME.level.cycle - self.hit_timer > 5:
            self.alpha = 100
            self.hit_timer = GAME.level.cycle

        GAME.level.UI.score_counter.update_score(10)

    # Pridanie objektu do groups
    # Umiestnenie na dané súradnice hracieho pola
    def super_spawn(self, position):
        GAME.level.enemies_group.add(self)
        GAME.level.all_sprites.add(self)
        
        self.rect.center = position
        self.dirty = 1

        self.spawned = True

    # Odstránenie objektu z groups
    def despawn(self):
        GAME.level.queues[type(self)].put(self)
        GAME.level.enemies_group.remove(self)
        GAME.level.all_sprites.remove(self)

        self.set_defaults()



    # ----- Events -------------------------------------------------------- #
    def execute_events(self):
        for event in self.event_list:
            if not eval(event[0]): continue

            event[1](event[2])
            
    
    def stop_moving(self, args):
        self.is_moving = False


    def start_moving(self, args):
        self.is_moving = True

    
    def rotate(self, args):
        angle = args[0]
        self.rotation += angle

        self.image = pygame.transform.rotate(self.image_clean, -self.rotation + 90)
        self.rect = self.image.get_rect(center = self.rect.center)

        self.set_turret_positions()


    def change_mp(self, args):
        self.movement_pattern = args[0]


    # ----- Abstract Methods -------------------------------------------------------- #
    @abstractclassmethod
    def set_defaults(self):
        pass
    
    @abstractclassmethod
    def shoot(self):
        pass
    
    @abstractclassmethod
    def set_turret_positions(self):
        pass

    @abstractclassmethod
    def spawn(self, position, mp):
        pass

    @abstractclassmethod
    def die(self):
        pass