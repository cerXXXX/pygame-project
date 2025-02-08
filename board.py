from copy import deepcopy
import pygame

from data import resource_path
from events import *
import time
import random
from tower import *
from enemy import *
from announcement import *


class Board:
    """Основной класс игры"""

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
        self.selected_tower = None

        self.currency = 1000  # начальное количество монет
        self.coin_icon = pygame.image.load(resource_path('assets/coin.png'))  # иконка монеты
        self.coin_icon = pygame.transform.scale(self.coin_icon, (30, 30))

        self.super_events = []
        self.set_super_events(super_events if super_events else [])
        self.curr_super_event = None
        self.time_between_events = 7
        self.last_super_event_time = time.time()
        self.max_num_super_events = 8

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
        self.heart_image = pygame.image.load(resource_path('assets/heart.png'))
        self.grey_heart_image = pygame.image.load(resource_path('assets/grey_heart.png'))
        self.road_img = pygame.image.load(resource_path('assets/road1.png'))
        self.ground_img = pygame.image.load(resource_path('assets/ground.png'))
        self.add_tower_img = pygame.image.load(resource_path('assets/add_tower2.png'))

    def set_super_events(self, events: list[SuperEvent]):
        """Установить список событий"""

        self.super_events = events
        self.super_events.append(SuperEvent(100, self, 'pass', 10))

    def set_way(self, way: list[tuple[int, int]]):
        """Установить путь"""

        self.way = way

    def set_view(self, left, top, cell_size):
        """Установить параметры отображения"""

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        """Отрисовка игрового поля"""

        # если игра не идет
        if not self.game_state:
            return

        # если есть оповещения
        if self.announcements:
            for announcement in self.announcements:
                announcement.render(screen)
            return

        # если есть волны
        if self.cur_wave:
            # спавним противников раз в time_between_enemies_in_wave
            if time.time() - self.last_enemy_spawn_time > self.time_between_enemies_in_wave:
                # вытаскиваем противника, создаем его и добавляем в группу противников
                enemy = self.cur_wave.pop(0)
                entity = enemy(pos=self.way[0], way=self.way, board=self)
                self.enemy_group.add(entity)
                self.last_enemy_spawn_time = time.time()
        # если все противники уничтожены
        elif not self.enemy_group.sprites():
            # и остались еще волны
            if self.waves:
                if (time.time() - self.last_enemy_spawn_time > self.time_between_enemies_in_wave and
                        time.time() - self.last_wave_time > self.time_between_waves):
                    self.last_wave_time = time.time()
                    self.cur_wave = self.waves.pop(0)
                    enemy = self.cur_wave.pop(0)
                    entity = enemy(pos=self.way[0], way=self.way, board=self)
                    self.enemy_group.add(entity)

                    self.last_enemy_spawn_time = time.time()
            # если волн больше нет, то победа
            else:
                self.game_state = False
                self.win = True
                self.level_time = time.time() - self.level_start_time
                return
        # отрисовка поля
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(self.ground_img, (x * self.cell_size + self.left, y * self.cell_size + self.top))

        # отрисовка дороги
        for cell in self.way:
            """pygame.draw.rect(screen, 'antiquewhite3',
                             (cell[0] * self.cell_size + self.left,
                              cell[1] * self.cell_size + self.top, self.cell_size, self.cell_size))"""
            screen.blit(self.road_img, (cell[0] * self.cell_size + self.left, cell[1] * self.cell_size + self.top))

        # отрисовка мест для строительства и башен
        for cell in self.building_places:
            if not cell[2]:
                screen.blit(self.add_tower_img,
                            (cell[0] * self.cell_size + self.left, cell[1] * self.cell_size + self.top))

        # отрисовка выделенного круга видимости башни
        if self.selected_tower:
            pygame.draw.circle(screen, 'blue', self.selected_tower.rect.center, self.selected_tower.visibility_zone, 1)

        # отрисовка башен и их пуль
        self.towers_Group.update(screen, self.enemy_group)

        # отрисовка меню
        if self.menu_open and self.menu_position:
            self.render_menu(screen)

        # если количество суперивентов больше нуля
        if self.max_num_super_events > 0:
            super_event = random.choices(self.super_events, weights=[i.frequency for i in self.super_events], k=1)[0]
            # если ивент не pass, то отрисовываем его
            if super_event.text != 'pass' and time.time() - self.last_super_event_time > self.time_between_events:
                self.last_super_event_time = time.time() + super_event.duration
                self.max_num_super_events -= 1

                if super_event.text == 'ArtilleryStrike':
                    self.announcements.append(Announcement('Артиллерийский удар!', master=self))
                    self.curr_super_event = ArtilleryStrike(frequency=super_event.frequency, board=self)
                    self.curr_super_event.start_time = time.time()
                elif super_event.text == 'Freeze':
                    self.announcements.append(Announcement('Заморозка!', master=self))
                    self.curr_super_event = FreezeEvent(frequency=super_event.frequency, board=self)
                    self.curr_super_event.start_time = time.time()

        # если идет ивент, то отрисовываем его
        if self.curr_super_event:
            self.curr_super_event.update(screen)

        # обновляем врагов
        self.enemy_group.update(screen)
        self.enemy_group.draw(screen)

        # обновляем анимации
        for i in self.animation_list:
            i.update(screen)

        # отображение оставшихся сердечек в правом верхнем углу
        self.render_health(screen)

        # если применен фильтр на экран, то отрисовываем его (для FreezeEvent)
        if self.filter:
            s = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height))
            s.set_alpha(self.filter[-1])
            s.fill(self.filter[:-1])
            screen.blit(s, (0, 0))

    def render_health(self, screen):
        """Отображает количество оставшихся сердечек"""

        for i in range(3):
            x_offset = screen.get_width() - 40 * (3 - i)
            y_offset = 10
            if i < self.health:
                screen.blit(self.heart_image, (x_offset, y_offset))
            else:
                screen.blit(self.grey_heart_image, (x_offset, y_offset))

    def render_interface(self, screen):
        """Отрисовка монет и меню поверх всех элементов"""

        # отображение монет
        font = pygame.font.Font(None, 36)
        currency_text = font.render(f"{self.currency}", True, 'black')
        screen.blit(self.coin_icon, (10, 10))
        screen.blit(currency_text, (50, 15))

        # отрисовка меню, если оно открыто
        if self.menu_open and self.menu_position:
            self.render_menu(screen)

    def get_cell(self, pos):
        """Возвращает координаты клетки, на которую нажал пользователь"""

        cell_x = (pos[0] - self.left) // self.cell_size
        cell_y = (pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        """Обрабатывает клик на клетку"""

        # если пользователь нажал на одно из мест для строительства
        for i in self.building_places:
            # если координаты совпадают
            if cell == (i[0], i[1]) or cell == (i[0] + 1, i[1]) or cell == (i[0], i[1] + 1) or cell == (
                    i[0] + 1, i[1] + 1):
                # если башни нет, открываем меню
                if i[2] is None:
                    self.menu_open = True
                    self.menu_position = ((i[0] + 1) * self.cell_size + self.left, i[1] * self.cell_size + self.top)
                    self.selected_building_place = i
                    self.create_menu_buttons()
                else:  # если башня уже есть, то показываем радиус действия
                    # если башня уже была выбрана, то снимаем выбор
                    if self.selected_tower == i[2]:
                        self.selected_tower = None
                    else:  # выбираем башню
                        self.selected_tower = i[2]
                return
        else:
            self.selected_tower = None

    def get_click(self, mouse_pos):
        """Обрабатывает клик мыши"""

        if self.menu_open:  # Если меню открыто, проверить клик для меню
            self.handle_menu_click(mouse_pos)
        else:
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)

    def set_building_places(self, building_places):
        """Устанавливает места для строительства башен"""

        self.building_places = [[i[0], i[1], None] for i in building_places]

    def create_menu_buttons(self):
        """Создает кнопки для меню выбора башни"""

        # очищаем список кнопок
        self.menu_buttons = []
        font = pygame.font.Font(None, 24)

        # получаем размеры экрана
        screen_width, screen_height = pygame.display.get_surface().get_size()

        # высота одной кнопки (с запасом)
        button_height = 40
        # высота всего меню
        menu_height = len(self.towers_data) * (button_height + 5)

        # определяем начальные координаты
        button_x = self.menu_position[0]
        button_y = self.menu_position[1]

        # проверяем выход за правый край экрана
        max_button_width = max(150, max(font.size(f"{td['name']} (${td['cost']})")[0] for td in self.towers_data) + 50)
        if button_x + max_button_width > screen_width:
            # смещаем влево
            button_x = self.menu_position[0] - max_button_width - 10

        # проверяем выход за нижний край экрана
        if button_y + menu_height > screen_height:
            # смещаем вверх
            button_y = screen_height - menu_height - 10

        # проверяем выход за верхний край экрана
        if button_y < 0:
            # смещаем вниз
            button_y = 10

        # создаем кнопки для каждой башни
        for index, tower_data in enumerate(self.towers_data):
            text = font.render(f"{tower_data['name']} (${tower_data['cost']})", True, 'black')
            text_width = text.get_width()
            button_width = max(150, text_width + 50)

            button_rect = pygame.Rect(button_x, button_y + index * (button_height + 5), button_width, button_height)
            self.menu_buttons.append((button_rect, tower_data, tower_data['cost']))

            # cохраняем текст для последующего рендера
            tower_data['menu_text'] = text

    def render_menu(self, screen):
        """Отображает меню выбора башни"""

        for button_rect, tower_data, tower_price in self.menu_buttons:
            # рисуем кнопку
            pygame.draw.rect(screen, 'grey' if tower_price <= self.currency else 'gray34', button_rect)
            pygame.draw.rect(screen, 'black', button_rect, 2)

            # загружаем и отображаем иконку башни
            icon = pygame.image.load(tower_data['icon']).convert_alpha()
            icon = pygame.transform.scale(icon, (30, 30))
            screen.blit(icon, (button_rect.x + 5, button_rect.y + 5))

            # отображаем текст с названием и стоимостью
            text = tower_data['menu_text']
            screen.blit(text, (button_rect.x + 40, button_rect.y + 10))

    def handle_menu_click(self, mouse_pos):
        """Обрабатывает клик мыши для меню выбора башни"""

        # блокируем, если есть оповещение
        if self.announcements:
            return

        menu_closed = True
        for button_rect, tower_data, tower_price in self.menu_buttons:
            if button_rect.collidepoint(mouse_pos):
                self.build_tower(tower_data)
                menu_closed = True
                break

        if menu_closed:  # если клик был вне кнопок, закрыть меню
            self.menu_open = False
            self.menu_position = None
            self.selected_building_place = None

    def build_tower(self, tower_data):
        """Строит башню"""

        # если ничего не выбрано
        if self.selected_building_place is None:
            return

        # если нет денег
        if self.currency < tower_data['cost']:
            return

        # списываем стоимость башни
        self.currency -= tower_data['cost']
        tower = Tower(self.selected_building_place[:2], tower_data['icon'], tower_data['rate_of_fire'],
                      tower_data['damage'], tower_data['visibility_zone'], tower_data['cost'],
                      tower_data['armor_piercing'], kill_zone=tower_data['kill_zone'], board=self)
        # указываем, что место занято
        self.selected_building_place[2] = tower
        self.towers.append(tower)
        self.towers_Group.add(tower)

    def handle_event(self, event):
        """Обрабатывает события"""

        if self.announcements:
            for announcement in self.announcements:
                announcement.handle_event(event)

    def add_animation(self, animation):
        """Добавляет анимацию"""

        self.animation_list.append(animation)

    def enemy_on_end_of_way(self):
        """Обрабатывает событие, когда враг дошел до конца пути"""

        # убираем хп и счет
        self.health -= 1
        self.score -= 100

        # если хп меньше нуля, то игра проиграна
        if self.health <= 0:
            self.game_state = False
            self.win = False
            self.level_time = time.time() - self.level_start_time
