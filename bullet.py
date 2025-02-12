import pygame
import math
from data import resource_path


class Bullet(pygame.sprite.Sprite):
    """Класс пули"""

    def __init__(self, start_pos, target, damage=10, speed=5, armor_piercing=0, quantity=1):
        super().__init__()
        self.target = target
        self.damage = damage
        self.speed = speed
        self.armor_piercing = armor_piercing

        color = (0, 0, 0)
        # пуль может быть от 1 до 3 (они рисуются рядом)
        if quantity == 1:
            self.original_image = pygame.Surface((6, 4), pygame.SRCALPHA)  # Прозрачный фон
            pygame.draw.rect(self.original_image, color, (0, 0, 6, 4))  # Одна пуля
        elif quantity == 2:
            self.original_image = pygame.Surface((6, 12), pygame.SRCALPHA)  # Прозрачный фон
            pygame.draw.rect(self.original_image, (1, 0, 4, 4), color)  # Верхняя пуля
            pygame.draw.rect(self.original_image, (1, 8, 4, 4), color)  # Нижняя пуля
        elif quantity == 3:
            self.original_image = pygame.Surface((4, 15), pygame.SRCALPHA)  # Прозрачный фон
            pygame.draw.rect(self.original_image, color, (1, 0, 4, 4))  # Верхняя пуля
            pygame.draw.rect(self.original_image, color, (1, 6, 4, 4))  # Средняя пуля (сдвиг на 3 пикселя)
            pygame.draw.rect(self.original_image, color, (1, 12, 4, 4))  # Нижняя пуля

        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # уничтожить пулю, если цель мертва или недоступна
        if not self.target or not self.target.alive():
            self.kill()
            return

        # вычисляем направление к цели
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # поворачиваем пулю к цели
        angle = math.degrees(math.atan2(-dy, dx))  # Угол поворота (в Pygame ось Y перевернута)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # движение пули к цели
        if distance > self.speed and not pygame.sprite.collide_mask(self, self.target):
            self.rect.x += self.speed * dx / distance
            self.rect.y += self.speed * dy / distance
        else:
            # попадание в цель
            self.rect.center = self.target.rect.center
            # наносим урон
            self.target.take_damage(self.damage, self.armor_piercing)
            # уничтожить пулю
            self.kill()


class BigBullet(Bullet):
    """Класс ракеты"""

    def __init__(self, start_pos, target, damage=10, speed=2, armor_piercing=0, board=None, kill_radius=20):
        super().__init__(start_pos, target, damage, speed, armor_piercing)

        self.image = pygame.image.load(resource_path('assets/rocket.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.original_image = self.image.copy()
        self.original_image = pygame.transform.rotate(self.original_image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.mask = pygame.mask.from_surface(self.image)

        self.board = board
        self.kill_radius = kill_radius

        self.speed = 0
        self.acceleration = 0.05

        self.angle = 0

    def update(self):
        if not self.target or not self.target.alive():
            self.kill()  # уничтожить пулю, если цель мертва или недоступна
            return

        self.speed += self.acceleration
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        self.angle = -math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # вычисляем направление к цели
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # движение пули к цели
        if distance > self.speed and not pygame.sprite.collide_mask(self, self.target):
            self.rect.x += self.speed * dx / distance
            self.rect.y += self.speed * dy / distance
        else:
            for enemy in self.board.enemy_group:
                if enemy.alive():
                    # создаем маску для зоны поражения (kill_radius)
                    kill_zone_surface = pygame.Surface((self.kill_radius * 2, self.kill_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(kill_zone_surface, (255, 255, 255), (self.kill_radius, self.kill_radius),
                                       self.kill_radius)
                    kill_zone_mask = pygame.mask.from_surface(kill_zone_surface)

                    # центрируем зону поражения относительно пули
                    kill_zone_offset = (
                        self.rect.centerx - (enemy.rect.left + self.kill_radius),
                        self.rect.centery - (enemy.rect.top + self.kill_radius),
                    )

                    # проверяем пересечение маски врага с зоной поражения
                    if kill_zone_mask.overlap(enemy.mask, kill_zone_offset):
                        enemy.take_damage(self.damage, self.armor_piercing)
            self.kill()
