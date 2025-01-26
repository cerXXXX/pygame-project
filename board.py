from copy import deepcopy
import pygame
from events import *
import time
import random
from tower import *
from enemy import *
from announcement import *


class Board:
    def __init__(self, width: int, height: int, left: int = 10, top: int = 10, cell_size: int = 30,
                 towers_data: list = None, level: int = 1, waves=None, level_manager=None, super_events=None):
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
        self.coin_icon = pygame.image.load('assets/coin.png')  # Иконка монеты
        self.coin_icon = pygame.transform.scale(self.coin_icon, (30, 30))

        self.super_events = []
        self.set_super_events(super_events if super_events else [])

        self.curr_super_event = None
        self.time_between_events = 5
        self.last_super_event_time = time.time()  # TODO: + 15 (время с начала игры без событий)
        self.max_num_super_events = 3

        self.level = level
        self.enemy_group = pygame.sprite.Group()

        self.level_manager = level_manager

        self.animation_list = []

        self.waves = deepcopy(waves)
        self.cur_wave = []
        self.time_between_enemies_in_wave = 0.5
        self.last_enemy_spawn_time = 0
        self.time_between_waves = 5
        self.last_wave_time = time.time()

        self.game_state = True
        self.win = False
        self.health = 3

        self.score = 0
        self.level_start_time = time.time()
        self.level_time = 0

        self.filter = None

        self.announcements = []

        # Загрузка изображений сердец
        self.heart_image = pygame.image.load('assets/heart.png')
        self.grey_heart_image = pygame.image.load('assets/grey_heart.png')
        self.road_img = pygame.image.load('assets/road1.png')
        self.ground_img = pygame.image.load('assets/ground.png')
        self.add_tower_img = pygame.image.load('assets/add_tower2.png')

    def set_super_events(self, events: list[SuperEvent]):
        self.super_events = events
        self.super_events.append(SuperEvent(100, self, 'pass', 10))

    def set_way(self, way: list[tuple[int, int]]):
        self.way = way

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        if not self.game_state:
            return

        if self.announcements:
            for announcement in self.announcements:
                announcement.render(screen)
            return

        if self.cur_wave:
            if time.time() - self.last_enemy_spawn_time > self.time_between_enemies_in_wave:
                enemy = self.cur_wave.pop(0)
                entity = enemy(pos=self.way[0], way=self.way, board=self)
                self.enemy_group.add(entity)

                self.last_enemy_spawn_time = time.time()
        elif not self.enemy_group.sprites():
            if self.waves:
                if (time.time() - self.last_enemy_spawn_time > self.time_between_enemies_in_wave and
                        time.time() - self.last_wave_time > self.time_between_waves):
                    self.last_wave_time = time.time()
                    self.cur_wave = self.waves.pop(0)
                    enemy = self.cur_wave.pop(0)
                    entity = enemy(pos=self.way[0], way=self.way, board=self)
                    self.enemy_group.add(entity)

                    self.last_enemy_spawn_time = time.time()
            else:
                self.game_state = False
                self.win = True
                self.level_time = time.time() - self.level_start_time
                return
        # Отрисовка сетки игрового поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white',
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)
                screen.blit(self.ground_img, (x * self.cell_size + self.left, y * self.cell_size + self.top))

        # Отрисовка пути и зон строительства
        for cell in self.way:
            """pygame.draw.rect(screen, 'antiquewhite3',
                             (cell[0] * self.cell_size + self.left,
                              cell[1] * self.cell_size + self.top, self.cell_size, self.cell_size))"""
            screen.blit(self.road_img, (cell[0] * self.cell_size + self.left, cell[1] * self.cell_size + self.top))

        for cell in self.building_places:
            if not cell[2]:
                screen.blit(self.add_tower_img, (cell[0] * self.cell_size + self.left, cell[1] * self.cell_size + self.top))
                """pygame.draw.rect(screen, 'aquamarine4',
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
                                  (cell[1] + 1) * self.cell_size + self.top, self.cell_size, self.cell_size))"""

        # Отрисовка выделенного круга видимости башни
        if self.selected_tower:
            pygame.draw.circle(screen, 'blue', self.selected_tower.rect.center, self.selected_tower.visibility_zone, 1)

        # Отрисовка башен и их пуль
        self.towers_Group.update(screen, self.enemy_group)

        # Отрисовка меню (всегда последним для повышения приоритета)
        if self.menu_open and self.menu_position:
            self.render_menu(screen)

        if self.max_num_super_events > 0:
            super_event = \
                random.choices(self.super_events, weights=[i.frequency for i in self.super_events], k=1)[0]
            if super_event.text != 'pass' and time.time() - self.last_super_event_time > self.time_between_events:
                self.last_super_event_time = time.time() + super_event.duration
                self.max_num_super_events -= 1

                # TODO: добавить новые события
                if super_event.text == 'ArtilleryStrike':
                    self.announcements.append(Announcement('Артиллерийский удар!', master=self))
                    self.curr_super_event = ArtilleryStrike(frequency=super_event.frequency, board=self)
                    self.curr_super_event.start_time = time.time()
                elif super_event.text == 'Freeze':
                    # print('start_freeze_event')
                    self.announcements.append(Announcement('Заморозка!', master=self))
                    self.curr_super_event = FreezeEvent(frequency=super_event.frequency, board=self)
                    self.curr_super_event.start_time = time.time()

        if self.curr_super_event:
            self.curr_super_event.update(screen)

        self.enemy_group.update(screen)
        self.enemy_group.draw(screen)
        self.enemy_group.update(screen)

        for i in self.animation_list:
            i.update(screen)

        # Отображение оставшихся сердечек в правом верхнем углу
        self.render_health(screen)

        if self.filter:
            s = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height))  # the size of your rect
            s.set_alpha(self.filter[-1])  # alpha level
            s.fill(self.filter[:-1])  # this fills the entire surface
            screen.blit(s, (0, 0))

    def render_health(self, screen):
        """Отображает количество оставшихся сердечек."""
        for i in range(3):
            x_offset = screen.get_width() - 40 * (3 - i)
            y_offset = 10
            if i < self.health:
                screen.blit(self.heart_image, (x_offset, y_offset))
            else:
                screen.blit(self.grey_heart_image, (x_offset, y_offset))

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
            self.menu_buttons.append((button_rect, tower_data, tower_data['cost']))

            # Добавляем текст к кнопке
            tower_data['menu_text'] = text  # Сохраняем текст для последующего рендера

    def render_menu(self, screen):
        font = pygame.font.Font(None, 24)
        for button_rect, tower_data, tower_price in self.menu_buttons:
            # Рисуем кнопку
            pygame.draw.rect(screen, 'grey' if tower_price <= self.currency else 'gray34', button_rect)
            pygame.draw.rect(screen, 'black', button_rect, 2)

            # Загружаем и отображаем иконку башни
            icon = pygame.image.load(tower_data['icon']).convert_alpha()
            icon = pygame.transform.scale(icon, (30, 30))
            screen.blit(icon, (button_rect.x + 5, button_rect.y + 5))

            # Отображаем текст с названием и стоимостью
            text = tower_data['menu_text']
            screen.blit(text, (button_rect.x + 40, button_rect.y + 10))

    def handle_menu_click(self, mouse_pos):
        if self.announcements:
            return
        """Обрабатывает клик внутри меню или закрывает меню при клике вне его."""
        menu_closed = True
        for button_rect, tower_data, tower_price in self.menu_buttons:
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
            return
        self.currency -= tower_data['cost']  # Списываем стоимость башни
        tower = Tower(self.selected_building_place[:2], tower_data['icon'], tower_data['rate_of_fire'],
                      tower_data['damage'], tower_data['visibility_zone'], tower_data['cost'],
                      tower_data['armor_piercing'], kill_zone=tower_data['kill_zone'], board=self)
        self.selected_building_place[2] = tower  # Mark as occupied
        self.towers.append(tower)
        self.towers_Group.add(tower)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level_data = self.level_manager.generate_level(self.level)
                enemy = Car(level_data.way[0], level_data.way, 'assets/car1.png', speed=20, board=self)
                self.enemy_group.add(enemy)
                # print(self.enemy_group)

        if self.announcements:
            for announcement in self.announcements:
                announcement.handle_event(event)

    def add_animation(self, animation):
        self.animation_list.append(animation)

    def enemy_on_end_of_way(self):
        self.health -= 1

        if self.health <= 0:
            self.game_state = False
            self.win = False
            self.level_time = time.time() - self.level_start_time
