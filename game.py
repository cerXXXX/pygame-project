import pygame
from data import *
from board import *
from level import *
from announcement import *


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
            x = 300  # + ((i - 1) % 5) * 100
            y = 50 + (i - 1) * 50
            self.level_select_menu.add_button(f"Уровень {i}", (x, y), lambda x: self.start_level(x))

    def start_game(self):
        self.state = GameState.GAME
        self.start_level(self.level_manager.current_level)

    def start_level(self, level_number):
        if level_number > 1 and (level_number - 1 not in self.level_manager.completed_levels):
            self.level_select_menu.announcements.append(Announcement(f"Уровень {level_number} не доступен", (300, 100), master=self.level_select_menu))
            return
        self.level_manager.current_level = level_number
        level = self.level_manager.generate_level(level_number)
        self.board = Board(20, 20, 0, 0, waves=level.waves, towers_data=towers_data, level=level_number,
                           level_manager=self.level_manager, super_events=level.super_events)
        self.board.set_way(level.way)
        self.board.set_building_places(level.building_places)
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
            if self.board:
                self.board.handle_event(event)
                if not self.board.game_state:
                    self.state = GameState.LEVEL_END
            if not self.board or not self.board.announcements:
                self.screen.fill('lightgreen')
            if self.state == GameState.MAIN_MENU:
                self.main_menu.render()
            elif self.state == GameState.PAUSE:
                self.pause_menu.render()
            elif self.state == GameState.LEVEL_SELECT:
                self.level_select_menu.render()
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
        self.completed_levels = set()  # Хранит номера пройденных уровней

    def generate_level(self, difficulty):
        # TODO: переделать
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
        # Генерация уровня по сложности
        return levels[difficulty]


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.buttons = []

        self.announcements = []

    def add_button(self, text, position, action):
        self.buttons.append({"text": text, "position": position, "action": action})

    def render(self):
        if self.announcements:
            for announcement in self.announcements:
                announcement.render(self.screen)
            return

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
                if button["text"].split()[0] == 'Уровень' and len(button["text"].split()) == 2:
                    button["action"](int(button["text"].split()[1]))
                    return
                button["action"]()

        if self.announcements:
            for announcement in self.announcements:
                announcement.mouse_click(mouse_pos)
