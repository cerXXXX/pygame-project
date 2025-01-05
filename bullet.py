import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target, damage=10, speed=5):
        super().__init__()
        self.image = pygame.Surface((5, 5))  # Маленький красный прямоугольник
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.target = target
        self.damage = damage
        self.speed = speed
        self.start_pos = start_pos

    def update(self):
        if not self.target or not self.target.alive():
            self.kill()  # Уничтожить пулю, если цель мертва или недоступна
            return

        # Вычисляем направление к цели
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Движение пули к цели
        if distance > self.speed:
            self.rect.x += self.speed * dx / distance
            self.rect.y += self.speed * dy / distance
        else:
            self.rect.center = self.target.rect.center  # Попадание в цель
            self.target.take_damage(self.damage)  # Наносим урон
            self.kill()  # Уничтожить пулю