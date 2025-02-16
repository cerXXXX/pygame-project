import pygame
import math
import time
from bullet import *


class Tower(pygame.sprite.Sprite):
    """Класс башни"""

    def __init__(self, pos, image, rate_of_fire=2, damage=5, visibility_zone=200, cost=100, armor_piercing=0,
                 kill_zone=None, board=None):
        super().__init__()
        self.visibility_zone = visibility_zone
        self.damage = damage
        self.image_path = image
        self.original_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (60, 60))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos[0] * 30 + 30, pos[1] * 30 + 30)
        self.angle = 0
        self.target = None
        self.rate_of_fire = rate_of_fire
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.cost = cost
        self.armor_piercing = armor_piercing

        self.mask = pygame.mask.from_surface(self.image)
        self.board = board
        self.kill_zone = kill_zone

    def update(self, screen, enemies):
        """Обновление башни"""

        # если есть цель и она жива, то проверяем дистанцю до нее
        if self.target and self.target.alive():
            distance = math.sqrt((self.rect.centerx - self.target.rect.centerx) ** 2 +
                                 (self.rect.centery - self.target.rect.centery) ** 2)

            # если дистанция до цели больше чем зона видимости, то цель сбрасывается
            if distance > self.visibility_zone:
                self.target = None
        else:
            # определение ближайшей цели
            closest_enemy = None
            closest_distance = float('inf')
            for enemy in enemies:
                distance = math.sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 +
                                     (self.rect.centery - enemy.rect.centery) ** 2)
                if distance < self.visibility_zone and distance < closest_distance:
                    closest_enemy = enemy
                    closest_distance = distance
            if closest_enemy:
                self.target = closest_enemy

        # если время стрельбы
        current_time = time.time()
        if self.target and current_time - self.last_shot_time >= 1 / self.rate_of_fire:
            self.shoot()
            self.last_shot_time = current_time

        # обновление всех пуль
        self.bullets.update()
        self.bullets.draw(screen)

        # поворот башни
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            self.angle = -math.degrees(math.atan2(dy, dx)) - 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # отрисовка башни
        screen.blit(self.image, self.rect)

    def shoot(self):
        """Стрельба"""

        # количество пуль зависит от скорости стрельбы
        quantity = 1 if self.rate_of_fire <= 2 else 2 if self.rate_of_fire <= 4 else 3

        # если имеет радиус поражение (ракеты), то стреляем с радиусом поражения
        if self.kill_zone:
            bullet = BigBullet(self.rect.center, self.target, self.damage, armor_piercing=self.armor_piercing,
                               board=self.board, kill_radius=self.kill_zone)
        else:  # иначе без него
            bullet = Bullet(self.rect.center, self.target, self.damage, armor_piercing=self.armor_piercing,
                            quantity=quantity)
        self.bullets.add(bullet)
