import pygame
from data import *
from board import *
from level import *
from announcement import *
from database import save_completed_level, get_completed_levels, save_level_result, get_best_result


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
        self.main_menu = Menu(self.screen)
        self.pause_menu = Menu(self.screen)
        self.level_select_menu = Menu(self.screen)
        self.level_end_menu = Menu(self.screen)

        # Загрузка изображений сердец
        self.heart_image = pygame.image.load('assets/heart.png')
        self.grey_heart_image = pygame.image.load('assets/grey_heart.png')

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

        # Первоначальное создание меню выбора уровня
        self.update_level_select_menu()

        # Меню завершения уровня
        self.level_end_menu.add_button("Выйти в меню", (300, 400), self.return_to_main_menu)

    def update_level_select_menu(self):
        """Перестраивает меню выбора уровня с учетом пройденных уровней и добавляет значки информации."""
        self.level_select_menu.buttons = []  # Очистка старых кнопок
        font = pygame.font.Font(None, 36)  # Меньший шрифт
        vertical_spacing = 55  # Интервал между кнопками
        initial_offset = 50  # Начальное смещение сверху
        for i in range(1, 11):
            x = 300
            y = initial_offset + (i - 1) * vertical_spacing
            # Цвет кнопки: серый для пройденного, иначе — черный
            color = 'gray' if i in self.level_manager.completed_levels else 'black'
            button = {
                "text": f"Уровень {i}",
                "position": (x, y),
                "action": lambda x=i: self.start_level(x),
                "color": color,
                "level": i
            }
            if i in self.level_manager.completed_levels:
                text_surface = font.render(button["text"], True, 'white')
                text_rect = text_surface.get_rect(center=(x - 15, y))  # смещение текста влево
                # Сделаем кнопку компактной: inflate(40, 15)
                rect = text_rect.inflate(40, 15)
                # Определяем прямоугольник для значка информации – в правом верхнем углу кнопки
                info_rect = pygame.Rect(rect.right - 25, rect.top + 5, 20, 20)
                button["info_rect"] = info_rect
                button["action_info"] = lambda lvl=i: self.show_best_result(lvl)
            self.level_select_menu.buttons.append(button)

    def show_best_result(self, level):
        """Отображает уведомление с лучшим результатом для данного уровня."""
        best = get_best_result(level)
        if best:
            score, time_val = best
            message = f"Лучший результат для уровня {level}:\nСчёт: {score}\nВремя: {time_val:.2f} сек."
        else:
            message = f"Для уровня {level} пока нет результатов."
        # Добавляем уведомление в меню выбора уровней
        self.level_select_menu.announcements.append(
            Announcement(message, (350, 100), master=self.level_select_menu)
        )

    def start_game(self):
        self.state = GameState.GAME
        self.start_level(self.level_manager.current_level)

    def start_level(self, level_number):
        if level_number > 1 and (level_number - 1 not in self.level_manager.completed_levels):
            self.level_select_menu.announcements.append(
                Announcement(f"Уровень {level_number} не доступен", (300, 100), master=self.level_select_menu))
            return
        self.level_manager.current_level = level_number
        level = self.level_manager.generate_level(level_number)
        self.board = Board(20, 20, 0, 0, waves=level.waves, towers_data=towers_data, level=level_number,
                           level_manager=self.level_manager, super_events=level.super_events)
        self.board.set_way(level.way)
        self.board.set_building_places(level.building_places)
        self.state = GameState.GAME

    def show_level_select(self):
        self.update_level_select_menu()  # Обновляем меню перед показом
        self.state = GameState.LEVEL_SELECT

    def return_to_main_menu(self):
        self.state = GameState.MAIN_MENU

    def resume_game(self):
        self.state = GameState.GAME

    def toggle_pause(self):
        self.state = GameState.PAUSE if self.state == GameState.GAME else GameState.GAME

    def exit_game(self):
        self.running = False

    def end_level(self):
        # Переход в меню завершения уровня
        self.state = GameState.LEVEL_END
        self.level_end_menu.announcements.clear()

        if self.board.win:
            self.level_manager.completed_levels.add(self.level_manager.current_level)
            save_completed_level(self.level_manager.current_level)  # Сохранение уровня
            save_level_result(self.level_manager.current_level, self.board.score, self.board.level_time, True)
            result_text = "Победа!"
        else:
            save_level_result(self.level_manager.current_level, self.board.score, self.board.level_time, False)
            result_text = "Поражение!"

        def render_results(surface):
            font = pygame.font.Font(None, 48)
            y_offset = 100

            result_surface = font.render(f"Результат: {result_text}", True, 'white')
            surface.blit(result_surface, result_surface.get_rect(center=(300, y_offset)))
            y_offset += 50
            score_surface = font.render(f"Счет: {self.board.score}", True, 'white')
            surface.blit(score_surface, score_surface.get_rect(center=(300, y_offset)))
            y_offset += 50
            time_surface = font.render(f"Время: {self.board.level_time:.2f} сек.", True, 'white')
            surface.blit(time_surface, time_surface.get_rect(center=(300, y_offset)))
            y_offset += 50
            for i in range(3):
                x_offset = 240 + i * 40
                if i < self.board.health:
                    surface.blit(self.heart_image, (x_offset, y_offset))
                else:
                    surface.blit(self.grey_heart_image, (x_offset, y_offset))

            button_font = pygame.font.Font(None, 36)
            button_text = button_font.render("Выйти в меню", True, 'white')
            button_rect = button_text.get_rect(center=(300, y_offset + 100))
            pygame.draw.rect(surface, 'black', button_rect.inflate(20, 10))
            surface.blit(button_text, button_rect)
            self.level_end_menu.add_button("Выйти в меню", (300, y_offset + 100), self.return_to_main_menu)

        self.level_end_menu.announcements.append(
            Announcement(render_func=render_results, position=(0, 0), master=self.level_end_menu)
        )

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
                    elif self.state == GameState.LEVEL_END:
                        self.level_end_menu.handle_click(event.pos)
                    elif self.state == GameState.GAME:
                        self.board.get_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and self.state == GameState.GAME:
                        self.toggle_pause()

            if self.board and self.state == GameState.GAME:
                self.board.handle_event(event)
                if not self.board.game_state:
                    self.end_level()

            if not self.board or not self.board.announcements:
                self.screen.fill('lightgreen')

            if self.state == GameState.MAIN_MENU:
                self.main_menu.render()
            elif self.state == GameState.PAUSE:
                self.pause_menu.render()
            elif self.state == GameState.LEVEL_SELECT:
                self.level_select_menu.render()
            elif self.state == GameState.LEVEL_END:
                self.level_end_menu.render()
            elif self.state == GameState.GAME:
                self.board.render(self.screen)
                self.board.render_interface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


class GameState:
    MAIN_MENU = 'main_menu'
    GAME = 'game'
    LEVEL_SELECT = 'level_select'
    PAUSE = 'pause'
    LEVEL_END = 'level_end'


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.completed_levels = get_completed_levels()

    def generate_level(self, difficulty):
        levels = {1: DefaultLevel(1),
                  2: DefaultLevel(2),
                  3: DefaultLevel(3),
                  4: DefaultLevel(4),
                  5: DefaultLevel(5),
                  6: DefaultLevel(6),
                  7: DefaultLevel(7),
                  8: DefaultLevel(8),
                  9: DefaultLevel(9),
                  10: DefaultLevel(10)}
        return levels[difficulty]


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.buttons = []
        self.announcements = []

    def add_button(self, text, position, action, color='black', **kwargs):
        """Можно передать дополнительные параметры, например info_rect, action_info, level и т.п."""
        button = {"text": text, "position": position, "action": action, "color": color}
        button.update(kwargs)
        self.buttons.append(button)

    def render(self):
        if self.announcements:
            for announcement in self.announcements:
                if callable(announcement.render_func):
                    announcement.render_func(self.screen)
                else:
                    announcement.render(self.screen)
            return

        for button in self.buttons:
            text_surface = self.font.render(button["text"], True, 'white')
            text_center = (button["position"][0] - 15, button["position"][1])
            text_rect = text_surface.get_rect(center=text_center)
            rect = text_rect.inflate(55, 15)
            pygame.draw.rect(self.screen, button["color"], rect)
            self.screen.blit(text_surface, text_rect)

            if "info_rect" in button:
                info_rect = pygame.Rect(rect.right - 25, rect.top + 5, 20, 20)
                button["info_rect"] = info_rect
                pygame.draw.rect(self.screen, 'blue', info_rect)
                info_text = pygame.font.Font(None, 20).render("i", True, 'white')
                info_text_rect = info_text.get_rect(center=info_rect.center)
                self.screen.blit(info_text, info_text_rect)

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            text_surface = self.font.render(button["text"], True, 'white')
            rect = text_surface.get_rect(center=button["position"])
            # Если есть значок информации, проверяем его область в приоритете
            if "info_rect" in button and button["info_rect"].collidepoint(mouse_pos):
                if "action_info" in button:
                    button["action_info"]()
                continue  # не вызываем основное действие кнопки, если клик пришёл по инфо-иконке

            if rect.collidepoint(mouse_pos):
                button["action"]()

        if self.announcements:
            for announcement in self.announcements:
                announcement.mouse_click(mouse_pos)
