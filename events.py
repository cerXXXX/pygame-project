import pygame
import time
import math
from animation import *
import random


class SuperEvent:
    def __init__(self, frequency, board, text, duration=5):
        self.frequency = frequency
        self.board = board
        self.start_time = time.time()
        self.text = text
        self.duration = duration

    def update(self, screen):
        if time.time() - self.start_time > self.duration:
            self.board.curr_super_event = None
            return


class ArtilleryStrike(SuperEvent):
    def __init__(self, frequency, board, text, duration=5):
        super().__init__(frequency, board, text, duration)
        self.damage = 100
        self.radius = 50
        self.count = 5
        self.points = [ArtilleryCircle((random.randint(0, self.board.width * self.board.cell_size),
                                        random.randint(0, self.board.height * self.board.cell_size)), self.radius) for _
                       in range(self.count)]

    def update(self, screen):
        super().update(screen)
        if not self.board.curr_super_event:
            for i in self.points:
                for j in self.board.towers:
                    if math.sqrt((i.rect.centerx - j.rect.centerx) ** 2 + (
                            i.rect.centery - j.rect.centery) ** 2) <= self.radius + j.rect.centerx - j.rect.x:
                        for k in self.board.building_places:
                            if k[2] == j:
                                k[2] = None
                        self.board.towers.remove(j)
                        j.kill()

        if time.time() - self.start_time > 4.9375:
            for i in self.points:
                i.kill()
                self.board.animation_list.append(Animation(self.board, i.rect.center, 'assets/explosion', 4, 0.25 / 4,
                                                           resize_to=(2 * self.radius, 2 * self.radius)))
        for i in self.points:
            i.update(screen)
            screen.blit(i.image, i.rect)


class ArtilleryCircle(pygame.sprite.Sprite):
    def __init__(self, pos, radius):
        super().__init__()
        self.radius = radius
        self.pos = pos
        self.image = pygame.image.load('assets/artillerystrike1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, screen):
        screen.blit(self.image, self.rect)
