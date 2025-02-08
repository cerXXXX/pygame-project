import pygame
import time
import math
from animation import *
import random
from data import resource_path


class SuperEvent:
    """Класс события"""

    def __init__(self, frequency, board, text, duration=5):
        self.frequency = frequency
        self.board = board
        self.start_time = time.time()
        self.text = text
        self.duration = duration

    def update(self, screen):
        """Обновление события"""

        # если событие завершилось
        if time.time() - self.start_time > self.duration:
            self.board.curr_super_event = None
            return


class ArtilleryStrike(SuperEvent):
    """Класс ивента артиллерийского удара"""

    def __init__(self, board, text='ArtilleryStrike', frequency=0.1, duration=5):
        super().__init__(frequency, board, text, duration)
        self.damage = 100
        self.radius = 50
        self.count = 5

        # точки удара
        self.points = [ArtilleryCircle((random.randint(0, self.board.width * self.board.cell_size),
                                        random.randint(0, self.board.height * self.board.cell_size)), self.radius) for _
                       in range(self.count)]

    def update(self, screen):
        """Обновление артиллерийского удара"""

        super().update(screen)
        # если событие завершилось, то пробегаем по всем точкам и удаляем башни, которые попали под удар
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

                # наносим урон противникам
                for j in self.board.enemy_group.sprites():
                    if pygame.sprite.collide_mask(j, i):
                        j.take_damage(self.damage, 0)

        # если событие подходит к концу, то начинаем проигрывать анимацию взрыва
        if time.time() - self.start_time > 4.9375:
            for i in self.points:
                i.kill()
                self.board.animation_list.append(
                    Animation(self.board, i.rect.center, resource_path('assets/explosion'), 4, 0.25 / 4,
                              resize_to=(2 * self.radius, 2 * self.radius)))
        # обновляем анимации взрыва
        for i in self.points:
            i.update(screen)
            screen.blit(i.image, i.rect)


class ArtilleryCircle(pygame.sprite.Sprite):
    """Спрайт точки артиллерийского удара"""

    def __init__(self, pos, radius):
        super().__init__()
        self.radius = radius
        self.pos = pos
        self.image = pygame.image.load(resource_path('assets/artillerystrike1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.radius * 2), int(self.radius * 2)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        mask_surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(mask_surf, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.mask = pygame.mask.from_surface(mask_surf)

    def update(self, screen):
        screen.blit(self.image, self.rect)


class NothingEvent(SuperEvent):
    """Ивент в котором ничего не происходит"""

    def __init__(self, board, text='pass', frequency=10, duration=0):
        super().__init__(frequency, board, text, duration)

    def update(self, screen):
        pass


class FreezeEvent(SuperEvent):
    """Ивент заморозки"""

    def __init__(self, board, text='Freeze', frequency=0.1, duration=5):
        super().__init__(frequency, board, text, duration)

    def update(self, screen):
        super().update(screen)
        # убираем эффект
        if not self.board.curr_super_event:
            self.board.filter = None
            for i in self.board.enemy_group.sprites():
                # возвращаем скорость врагам
                i.speed = i.speed_
            return

        # добавляем эффект
        self.board.filter = (166, 220, 237, 80)
        for i in self.board.enemy_group.sprites():
            i.freeze(80)


class Reinforcements(SuperEvent):
    def __init__(self, board, text='Reinforcements', frequency=0.1, duration=5):
        super().__init__(frequency, board, text, duration)


class ChaosMode(SuperEvent):
    def __init__(self, board, text='Chaos Mode', frequency=0.1, duration=5):
        super().__init__(frequency, board, text, duration)
