import pygame
import random
import math
from animation import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, way, speed, turn_speed, max_health=150, reward=50, board=None, armor=0):
        super().__init__()
        self.image_path = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.reward = reward
        self.board = board  # Сохраняем ссылку на объект Board
        self.health = max_health
        self.max_health = max_health

        delta = 10
        # delta_x, delta_y = 0, 0
        delta_x = random.randint(0, delta)
        delta_y = random.randint(-delta, delta)
        self.way = way
        self.pixels_way = [(i[0] * 30 + 15 + delta_x, i[1] * 30 + 15 + delta_y) for i in self.way]
        self.rect.centerx = self.pixels_way[0][0]
        self.rect.centery = self.pixels_way[0][1]

        self.float_pos = [self.rect.centerx, self.rect.centery]

        self.speed_ = speed / 40
        self.speed = speed / 40
        self.turn_speed = turn_speed
        self.original_image = pygame.image.load(image).convert_alpha()

        self.angle = -90
        self.turning = False
        self.target_angle = -90
        self.current_index = 0
        self.rotation_threshold = 5

        self.armor = armor

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, screen):
        if self.turning:
            self.turn()
        else:
            self.move()
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)

        """for i in self.pixels_way:
            pygame.draw.circle(screen, 'red', i, 1)"""

        # pygame.draw.circle(screen, 'red', self.pixels_way[self.current_index], 2)
        # pygame.draw.circle(screen, 'blue', self.rect.center, 15)

    def move(self):
        """try:
            self.current_index = self.way.index(self.get_cell())
        except ValueError:
            pygame.draw.rect(screen, 'red',
                             (self.get_cell()[0] * 30,
                              self.get_cell()[1] * 30, 30, 30))"""
        # Если достигли конца пути, останавливаемся
        if self.current_index >= len(self.pixels_way) - 1:
            self.board.enemy_on_end_of_way()
            self.kill()
            return

        # Получить следующую точку пути
        next_point = self.pixels_way[self.current_index + 1]
        delta_x = next_point[0] - self.rect.centerx
        delta_y = next_point[1] - self.rect.centery
        target_angle = math.degrees(math.atan2(-delta_y, delta_x)) - 90
        # print(f'Moving to {next_point} from {self.rect}')

        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        # Проверка необходимости поворота
        if abs((target_angle - self.angle + 180) % 360 - 180) > self.rotation_threshold and distance > self.speed:
            self.turning = True
            self.target_angle = target_angle
            return

        # Движение к следующей точке
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if distance <= self.speed:  # Если точка близка, переходим к следующей
            self.rect.x, self.rect.y = next_point[0] - 15, next_point[1] - 15
            self.current_index += 1
        else:  # Иначе продолжаем движение
            self.float_pos[0] += self.speed * delta_x / distance
            self.float_pos[1] += self.speed * delta_y / distance
            self.rect.x, self.rect.y = self.float_pos[0] - 15, self.float_pos[1] - 15
        # print(self.rect.center, math.sqrt(delta_x ** 2 + delta_y ** 2))

    def turn(self):
        # Плавный поворот к целевому углу
        angle_diff = (self.target_angle - self.angle + 180) % 360 - 180
        if abs(angle_diff) <= self.turn_speed:  # Если угол достаточно близок, завершить поворот
            self.angle = self.target_angle
            self.turning = False
        else:
            self.angle += self.turn_speed if angle_diff > 0 else -self.turn_speed

        # Обновление изображения
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_health_bar(self, screen):
        """Рисует хитбар над врагом"""
        bar_width = 30
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - bar_height - 2
        fill_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Красный фон
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))  # Зеленый прогресс

    def take_damage(self, damage, armor_piercing):
        """Наносит урон врагу"""
        # print(self.armor, armor_piercing)
        damage_k = self.armor - armor_piercing
        if damage_k <= 0:
            # print('k <= 0')
            damage = damage
        else:
            damage = damage * (1 - damage_k / 100)
        self.health -= damage
        if self.health <= 0:
            self.board.score += self.reward
            self.kill()  # Удаляет врага, если здоровье <= 0
            self.board.currency += self.reward
            self.board.add_animation(Animation(self.board, self.rect.center, 'assets/explosion', 4, 0.25 / 4))

    def get_cell(self):
        """Возвращает координаты текущей клетки"""
        return self.rect.centerx // 30, self.rect.centery // 30

    def freeze(self, freeze: int):
        self.speed *= freeze / 100


class Tank(Enemy):
    def __init__(self, pos, way, image='assets/tank1.png', speed=15, turn_speed=2, board=None, armor=100, reward=250):
        super().__init__(pos, image, way, speed=speed, turn_speed=turn_speed, board=board, armor=armor, reward=reward)
        self.name = 'Tank'


class Car(Enemy):
    def __init__(self, pos, way, image='assets/car1.png', speed=30, turn_speed=3, board=None, armor=20, reward=100):
        super().__init__(pos, image, way, speed=speed, turn_speed=turn_speed, board=board, max_health=50, armor=armor,
                         reward=reward)
        self.name = 'Car'


class FastCar(Enemy):
    def __init__(self, pos, way, image='assets/car2.png', speed=45, turn_speed=4, board=None, armor=20, reward=120):
        super().__init__(pos, image, way, speed=speed, turn_speed=turn_speed, board=board, max_health=50, armor=armor,
                         reward=reward)
        self.name = 'FastCar'


class HeavyTank(Enemy):
    def __init__(self, pos, way, image='assets/tank2.png', speed=10, turn_speed=1, board=None, armor=150, reward=300):
        super().__init__(pos, image, way, speed=speed, turn_speed=turn_speed, board=board, max_health=130, armor=armor,
                         reward=reward)
        self.name = 'HeavyTank'
