import pygame
import math
import time
import random


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30, towers_data=None):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.way = []
        self.building_places = []
        self.towers = []
        self.towers_Group = pygame.sprite.Group()
        self.towers_data = towers_data if towers_data else []
        self.menu_open = False
        self.menu_position = None
        self.menu_buttons = []
        self.selected_building_place = None
        self.selected_tower = None  # Currently selected tower

        self.currency = 1000  # Начальное количество монет
        self.coin_icon = pygame.image.load('coin.png')  # Иконка монеты
        self.coin_icon = pygame.transform.scale(self.coin_icon, (30, 30))

    def set_way(self, way: list[tuple[int, int]]):
        self.way = way

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, enemies):
        # Отрисовка сетки игрового поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white',
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

        # Отрисовка пути и зон строительства
        for cell in self.way:
            pygame.draw.rect(screen, 'antiquewhite3',
                             (cell[0] * self.cell_size + self.left,
                              cell[1] * self.cell_size + self.top, self.cell_size, self.cell_size))

        for cell in self.building_places:
            if not cell[2]:
                pygame.draw.rect(screen, 'aquamarine4',
                                 (cell[0] * self.cell_size + self.left,
                                  cell[1] * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, 'aquamarine4',
                                 ((cell[0] + 1) * self.cell_size + self.left,
                                  cell[1] * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, 'aquamarine4',
                                 (cell[0] * self.cell_size + self.left,
                                  (cell[1] + 1) * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, 'aquamarine4',
                                 ((cell[0] + 1) * self.cell_size + self.left,
                                  (cell[1] + 1) * self.cell_size + self.top, self.cell_size, self.cell_size))

        # Отрисовка выделенного круга видимости башни
        if self.selected_tower:
            pygame.draw.circle(screen, 'blue', self.selected_tower.rect.center, self.selected_tower.visibility_zone, 1)

        # Отрисовка башен и их пуль
        self.towers_Group.update(screen, enemies)

        # Отрисовка меню (всегда последним для повышения приоритета)
        if self.menu_open and self.menu_position:
            self.render_menu(screen)

    def render_interface(self, screen):
        """Отрисовка монет и меню поверх всех элементов."""
        # Отображение валюты
        font = pygame.font.Font(None, 36)
        currency_text = font.render(f"{self.currency}", True, 'black')
        screen.blit(self.coin_icon, (10, 10))
        screen.blit(currency_text, (50, 15))

        # Отрисовка меню, если оно открыто
        if self.menu_open and self.menu_position:
            self.render_menu(screen)

    def get_cell(self, pos):
        cell_x = (pos[0] - self.left) // self.cell_size
        cell_y = (pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        for i in self.building_places:
            if cell == (i[0], i[1]) or cell == (i[0] + 1, i[1]) or cell == (i[0], i[1] + 1) or cell == (
                    i[0] + 1, i[1] + 1):
                if i[2] is None:  # Empty building place
                    self.menu_open = True
                    self.menu_position = ((i[0] + 1) * self.cell_size + self.left, i[1] * self.cell_size + self.top)
                    self.selected_building_place = i
                    self.create_menu_buttons()
                else:  # A tower already exists here
                    if self.selected_tower == i[2]:  # Deselect if already selected
                        self.selected_tower = None
                    else:  # Select the tower
                        self.selected_tower = i[2]
                return
        else:
            self.selected_tower = None

    def get_click(self, mouse_pos):
        """Обрабатывает клик мыши."""
        if self.menu_open:  # Если меню открыто, проверить клик для меню
            self.handle_menu_click(mouse_pos)
        else:
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)

    def set_background(self, background):
        pass

    def set_building_places(self, building_places):
        self.building_places = [[i[0], i[1], None] for i in building_places]

    def spawn_enemies(self, enemies):
        pass

    def create_menu_buttons(self):
        self.menu_buttons = []
        font = pygame.font.Font(None, 24)
        for index, tower_data in enumerate(self.towers_data):
            # Формируем текст с названием и стоимостью башни
            text = font.render(f"{tower_data['name']} (${tower_data['cost']})", True, 'black')
            text_width = text.get_width()
            button_width = max(150, text_width + 50)  # Задаем ширину кнопки
            button_height = max(40, text.get_height() + 10)

            # Определяем положение кнопки
            button_rect = pygame.Rect(self.menu_position[0],
                                      self.menu_position[1] + index * (button_height + 5),
                                      button_width, button_height)
            self.menu_buttons.append((button_rect, tower_data))

            # Добавляем текст к кнопке
            tower_data['menu_text'] = text  # Сохраняем текст для последующего рендера

    def render_menu(self, screen):
        font = pygame.font.Font(None, 24)
        for button_rect, tower_data in self.menu_buttons:
            # Рисуем кнопку
            pygame.draw.rect(screen, 'grey', button_rect)
            pygame.draw.rect(screen, 'black', button_rect, 2)

            # Загружаем и отображаем иконку башни
            icon = pygame.image.load(tower_data['icon']).convert_alpha()
            icon = pygame.transform.scale(icon, (30, 30))
            screen.blit(icon, (button_rect.x + 5, button_rect.y + 5))

            # Отображаем текст с названием и стоимостью
            text = tower_data['menu_text']
            screen.blit(text, (button_rect.x + 40, button_rect.y + 10))

    def handle_menu_click(self, mouse_pos):
        """Обрабатывает клик внутри меню или закрывает меню при клике вне его."""
        menu_closed = True
        for button_rect, tower_data in self.menu_buttons:
            if button_rect.collidepoint(mouse_pos):
                self.build_tower(tower_data)
                menu_closed = True
                break

        if menu_closed:  # Если клик был вне кнопок, закрыть меню
            self.menu_open = False
            self.menu_position = None
            self.selected_building_place = None

    def build_tower(self, tower_data):
        if self.selected_building_place is None:
            return
        if self.currency < tower_data['cost']:  # Проверка наличия монет
            print("Not enough currency!")
            return
        self.currency -= tower_data['cost']  # Списываем стоимость башни
        tower = Tower(self.selected_building_place[:2], tower_data['icon'], tower_data['rate_of_fire'],
                      tower_data['damage'], tower_data['visibility_zone'], tower_data['cost'])
        self.selected_building_place[2] = tower  # Mark as occupied
        self.towers.append(tower)
        self.towers_Group.add(tower)


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


class Level:
    def __init__(self, way, waves, background, building_places: list[tuple[int, int]]):
        self.way = way
        self.waves = waves
        self.background = background
        self.building_places = building_places


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, image, rate_of_fire=2, damage=5, visibility_zone=200, cost=100):
        super().__init__()
        self.visibility_zone = visibility_zone
        self.damage = damage
        self.image_path = image
        self.original_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (60, 60))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0] * 30 + 30, pos[1] * 30 + 30)
        self.angle = 0
        self.target = None
        self.rate_of_fire = rate_of_fire
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.cost = cost

    def update(self, screen, enemies):
        # Target logic
        if self.target and self.target.alive():
            distance = math.sqrt((self.rect.centerx - self.target.rect.centerx) ** 2 +
                                 (self.rect.centery - self.target.rect.centery) ** 2)
            if distance > self.visibility_zone:
                self.target = None
        else:
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

        # Shooting logic
        current_time = time.time()
        if self.target and current_time - self.last_shot_time >= 1 / self.rate_of_fire:
            self.shoot()
            self.last_shot_time = current_time  # Update last shot time

        # Update bullets
        self.bullets.update()
        self.bullets.draw(screen)

        # Rotate tower
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            self.angle = -math.degrees(math.atan2(dy, dx)) - 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Draw tower
        screen.blit(self.image, self.rect)

    def shoot(self):
        bullet = Bullet(self.rect.center, self.target, self.damage)
        self.bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, way, speed, turn_speed, max_health=100, reward=50, board=None):
        super().__init__()
        self.image_path = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.reward = reward
        self.board = board  # Сохраняем ссылку на объект Board

        delta = 10
        delta_x, delta_y = 0, 0
        if random.randint(0, 1):
            delta_x = random.randint(-delta, delta)
        else:
            delta_y = random.randint(-delta, delta)
        self.way = way
        self.pixels_way = [(i[0] * 30 + 15 + delta_x, i[1] * 30 + delta_y) for i in self.way]
        self.rect.centerx = self.pixels_way[0][0]
        self.rect.centery = self.pixels_way[0][1]
        self.speed = speed
        self.turn_speed = turn_speed
        self.original_image = pygame.image.load(image).convert_alpha()
        self.health = max_health
        self.max_health = max_health
        self.angle = 0
        self.turning = False
        self.target_angle = 0
        self.current_index = 0
        self.rotation_threshold = 5

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
            self.rect.x += self.speed * delta_x / distance
            self.rect.y += self.speed * delta_y / distance
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

    def take_damage(self, damage):
        """Наносит урон врагу"""
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Удаляет врага, если здоровье <= 0
            self.board.currency += self.reward

    def get_cell(self):
        """Возвращает координаты текущей клетки"""
        return self.rect.centerx // 30, self.rect.centery // 30


class Tank(Enemy):
    def __init__(self, pos, image, way):
        super().__init__(pos, image, way, speed=1, turn_speed=2)  # Медленный поворот


class Car(Enemy):
    def __init__(self, pos, image, way):
        super().__init__(pos, image, way, speed=3, turn_speed=5)  # Быстрый поворот


class GameState:
    MAIN_MENU = 'main_menu'
    GAME = 'game'
    LEVEL_SELECT = 'level_select'
    PAUSE = 'pause'


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.completed_levels = set()  # Хранит номера пройденных уровней

    def generate_level(self, difficulty):
        levels = [None, Level([(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                               (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11),
                               (12, 12),
                               (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14),
                               (5, 15),
                               (5, 16),
                               (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                               (14, 17),
                               (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)], [], None,
                              [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)])]
        # Генерация уровня по сложности
        return levels[difficulty]


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.buttons = []

    def add_button(self, text, position, action):
        self.buttons.append({"text": text, "position": position, "action": action})

    def render(self):
        for button in self.buttons:
            text = self.font.render(button["text"], True, 'white')
            rect = text.get_rect(center=button["position"])
            pygame.draw.rect(self.screen, 'black', rect.inflate(20, 10))
            self.screen.blit(text, rect)

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            text = self.font.render(button["text"], True, 'white')
            rect = text.get_rect(center=button["position"])
            if rect.collidepoint(mouse_pos):
                button["action"]()


towers_data = [
    {
        'name': 'Cannon Tower',
        'icon': 'tower1.png',
        'rate_of_fire': 2,
        'damage': 10,
        'visibility_zone': 200,
        'cost': 200  # Стоимость
    },
    {
        'name': 'Archer Tower',
        'icon': 'tower2.png',
        'rate_of_fire': 5,
        'damage': 2,
        'visibility_zone': 300,
        'cost': 150
    },
    {
        'name': 'Wtf is this tower',
        'icon': 'tower1.png',
        'rate_of_fire': 25,
        'damage': 0.2,
        'visibility_zone': 500,
        'cost': 300
    }
]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MAIN_MENU
        self.level_manager = LevelManager()
        self.board = None
        self.enemy_group = pygame.sprite.Group()
        self.main_menu = Menu(self.screen)
        self.pause_menu = Menu(self.screen)
        self.level_select_menu = Menu(self.screen)
        self.enemies = []

        # Настройка меню
        self.setup_menus()

    def setup_menus(self):
        # Главное меню
        self.main_menu.add_button("Продолжить игру", (300, 200), self.start_game)
        self.main_menu.add_button("Все уровни", (300, 300), self.show_level_select)
        self.main_menu.add_button("Выйти", (300, 400), self.exit_game)

        # Меню паузы
        self.pause_menu.add_button("Продолжить игру", (300, 200), self.resume_game)
        self.pause_menu.add_button("Выйти в меню", (300, 300), self.return_to_main_menu)

        # Меню выбора уровня
        for i in range(1, 11):
            x = 100 + ((i - 1) % 5) * 100
            y = 200 + ((i - 1) // 5) * 100
            self.level_select_menu.add_button(f"Уровень {i}", (x, y), lambda i: self.start_level(i))

    def start_game(self):
        self.state = GameState.GAME
        self.start_level(self.level_manager.current_level)

    def start_level(self, level_number):
        if level_number > 1 and (level_number - 1 not in self.level_manager.completed_levels):
            print(f"Уровень {level_number} недоступен.")
            return
        self.level_manager.current_level = level_number
        level = self.level_manager.generate_level(level_number)
        self.board = Board(20, 20, 0, 0, towers_data=towers_data)
        self.board.set_way(level.way)
        self.board.set_building_places(level.building_places)
        self.enemy_group = pygame.sprite.Group()
        self.state = GameState.GAME

    def show_level_select(self):
        self.state = GameState.LEVEL_SELECT

    def return_to_main_menu(self):
        self.state = GameState.MAIN_MENU

    def resume_game(self):
        self.state = GameState.GAME

    def toggle_pause(self):
        self.state = GameState.PAUSE if self.state == GameState.GAME else GameState.GAME

    def exit_game(self):
        self.running = False

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == GameState.MAIN_MENU:
                        self.main_menu.handle_click(event.pos)
                    elif self.state == GameState.PAUSE:
                        self.pause_menu.handle_click(event.pos)
                    elif self.state == GameState.LEVEL_SELECT:
                        self.level_select_menu.handle_click(event.pos)
                    elif self.state == GameState.GAME:
                        self.board.get_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and self.state == GameState.GAME:
                        self.toggle_pause()
                    if event.key == pygame.K_SPACE and self.state == GameState.GAME:
                        level = self.level_manager.generate_level(1)
                        self.enemies.append(Tank(level.way[0], 'tank1.png', level.way))

            self.screen.fill('lightgreen')
            if self.state == GameState.MAIN_MENU:
                self.main_menu.render()
            elif self.state == GameState.PAUSE:
                self.pause_menu.render()
            elif self.state == GameState.LEVEL_SELECT:
                self.level_select_menu.render()
            elif self.state == GameState.GAME:
                self.board.render(self.screen, self.enemy_group.sprites())
                self.enemy_group.update(self.screen)
                self.enemy_group.draw(self.screen)
                self.board.render_interface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.game_loop()
    pygame.quit()
