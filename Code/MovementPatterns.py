import pygame
import math
from Vectors import VectorPlus
import os


class Linear():
    def __init__(self, parent, angle, speed, acceleration=0):
        self.vector = VectorPlus.from_angle(angle)
        self.parent = parent
        self.speed = speed
        self.acceleration = acceleration

        self.buffer = [0, 0]



    def update(self):
        self.speed += self.acceleration

        vec_x = self.speed * self.vector.x
        vec_y = self.speed * self.vector.y

        x = self.parent.rect.centerx + vec_x
        y = self.parent.rect.centery + vec_y

        self.buffer[0] += vec_x
        self.buffer[1] += vec_y

        x += self.buffer[0]
        y += self.buffer[1]

        self.buffer[0] %= 1
        self.buffer[1] %= 1

        if self.speed <= 0: self.acceleration = 0

        return (x, y)


    def change_angle(self, angle):
        self.vector = VectorPlus.from_angle(angle)


    def init_vector(self):
        pass


class Sine():
    def __init__(self, parent, angle, speed, amplitude, freq, acceleration=0):
        # Jednotkový vektor predstavujúci smer osi sínusového pohybu
        self.axis_vector = VectorPlus.from_angle(angle)     

        self.parent = parent                   # Objekt, na ktorý je pohyb aplikovaný
        self.amplitude = amplitude             # Amplitúda sínusovky
        self.speed = speed                     # Rýchlosť pohybu po osi sínusovky
        self.freq = freq                       # Frekvencia oscilácie sínusovky
        self.acceleration = acceleration       # Zmena rýchlosti pohybu po osi sínusovky

        self.timer = 0                         # Časovač, predstavuje fázu sínusovky

        # Momentálna pozícia na osi sínusového pohybu
        self.axis_pos = [parent.rect.centerx, parent.rect.centery]


    # Vypočíta nasledovnú pozíciu na sínusovej krivke
    # Vizualizácia dôležitých premenných: https://cdn.discordapp.com/attachments/481431046089605120/949293452041023488/Picture1.png
    def update(self):
        self.speed += self.acceleration                         # Zmena rýchlosti

        perp = VectorPlus.get_perpendicular(self.axis_vector)   # Získa normálový vektor osi pohybu
        t = math.radians(self.timer * self.freq)                # Zmení hodnotu časovača na radiány
        perp *= math.sin(t) * self.amplitude                    # Vynásobí normálový vektor okamžitou
                                                                #   hodnotou sínusovej funkcie

        # Vypočíta nasledovnú pozíciu na osi sínusovky
        self.axis_pos[0] += self.axis_vector.x * self.speed
        self.axis_pos[1] += self.axis_vector.y * self.speed

        self.timer += 1

        # Vráti výslednú pozíciu kolmú na os sínusovky
        return (perp.x + self.axis_pos[0], perp.y + self.axis_pos[1])


    def change_angle(self, angle):
        self.axis_vector = VectorPlus.from_angle(angle)


    def init_vector(self):
        self.axis_pos = [self.parent.rect.centerx, self.parent.rect.centery]


class Homing():
    def __init__(self, parent, speed, target, acceleration=0):
        self.parent = parent
        self.speed = speed
        self.target = target
        self.acceleration = acceleration

        self.buffer = [0, 0]
        self.init_vector()


    def update(self):
        self.speed += self.acceleration

        vec_x = self.speed * self.vector.x
        vec_y = self.speed * self.vector.y

        x = self.parent.rect.centerx + vec_x
        y = self.parent.rect.centery + vec_y

        self.buffer[0] += vec_x
        self.buffer[1] += vec_y

        x += self.buffer[0]
        y += self.buffer[1]

        self.buffer[0] %= 1
        self.buffer[1] %= 1

        return (x, y)


    def init_vector(self):
        self.vector = pygame.Vector2(self.target.rect.centerx - self.parent.rect.centerx,
                                     self.target.rect.centery - self.parent.rect.centery)
        self.vector.normalize_ip()


class Chasing(Homing):
    def __init__(self, parent, speed, target, timer=-1, acceleration=0):
        Homing.__init__(self, parent, speed, target, acceleration)
        self.vector = pygame.math.Vector2()
        self.timer = timer
        self.buffer = [0, 0]


    def update(self):
        self.speed += self.acceleration

        if self.timer > 0: self.update_vector()
        self.timer -= 1

        vec_x = self.speed * self.vector.x
        vec_y = self.speed * self.vector.y

        x = self.parent.rect.centerx + vec_x
        y = self.parent.rect.centery + vec_y

        self.buffer[0] += vec_x
        self.buffer[1] += vec_y

        x += self.buffer[0]
        y += self.buffer[1]

        self.buffer[0] %= 1
        self.buffer[1] %= 1

        return (x, y)


    def update_vector(self):
        target_pos = self.target.rect.center
        parent_pos = self.parent.rect.center

        self.vector = pygame.Vector2(target_pos[0] - parent_pos[0], target_pos[1] - parent_pos[1])
        self.vector.normalize_ip()


    def init_vector(self):
        pass

