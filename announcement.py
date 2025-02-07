import pygame


def render_multiline_text(surface, text, font, color, rect):
    """Отрисовка многострочного текста, который не вылезает за rect"""
    otstup = 5
    available_height = rect.height - otstup - otstup

    # разбиваем текст на абзацы по символу новой строки
    paragraphs = text.splitlines()
    lines = []
    for p in paragraphs:
        words = p.split(' ')
        current_line = ''
        for word in words:
            line = f'{current_line} {word}'.strip()
            if font.size(line)[0] > rect.width and current_line:
                # если вылезли за границу, начинаем новую строку
                lines.append(current_line)
                current_line = word
            else:
                current_line = line
        if current_line:
            lines.append(current_line)

    # высота одной строки
    line_height = font.get_linesize()
    # высота всех строк
    total_height = len(lines) * font.get_linesize()

    # если текст меньше доступной высоты, центрируем его, иначе начинаем с otstup
    if total_height < available_height:
        y_offset = rect.top + otstup + (available_height - total_height) // 2
    else:
        y_offset = rect.top + otstup

    # рисуем каждую строку
    for line in lines:
        rendered_text = font.render(line, True, color)
        text_width = font.size(line)[0]
        x_offset = rect.left + (rect.width - text_width) // 2
        surface.blit(rendered_text, (x_offset, y_offset))
        y_offset += line_height


class Announcement:
    """Класс для отображения уведомлений. Рисует в центре экрана окно размером size и текстом content, а также
    кнопку ОК, при нажатии на которую уведомление закрывается"""

    def __init__(self, content=None, size=(300, 300), font_size=20, position='center', background_image=None,
                 master=None, render_func=None):
        self.content = content
        self.size = size
        self.font_size = font_size
        self.position = position
        self.background_image = background_image
        if self.background_image:
            self.size = self.background_image.get_size()
        self.master = master
        self.is_visible = True
        self.button_rect = None

        # пользовательская функция для отображения уведомления
        self.render_func = render_func

    def render(self, screen):
        """Рендер уведомления"""

        # если невидима
        if not self.is_visible:
            return

        # если есть пользовательская функция для отображения
        if self.render_func:
            self.render_func(screen)
            return

        if self.background_image:
            background = self.background_image.copy()
        else:
            background = pygame.Surface(self.size, pygame.SRCALPHA)
            background.fill((0, 0, 0, 0))
            rect_color = (50, 205, 50)
            pygame.draw.rect(background, rect_color, pygame.Rect(0, 0, *self.size), border_radius=20, width=0)

        border_color = (255, 255, 255)

        # Позиционируем уведомление
        screen_rect = pygame.Rect(0, 0, *self.size)
        if self.position == 'center':
            screen_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        elif self.position == 'top-left':
            screen_rect.topleft = (10, 10)
        elif self.position == 'top-right':
            screen_rect.topright = (screen.get_width() - 10, 10)
        elif self.position == 'bottom-left':
            screen_rect.bottomleft = (10, screen.get_height() - 10)
        elif self.position == 'bottom-right':
            screen_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)

        # рендер текста с переносом строк
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        text_rect = pygame.Rect(10, 10, self.size[0] - 20, self.size[1] - 60)  # Оставляем место для кнопки
        render_multiline_text(background, self.content, font, (255, 255, 255), text_rect)

        # рендер кнопки "ОК"
        button_font = pygame.font.Font('freesansbold.ttf', 16)
        button_text = button_font.render('OK', True, (255, 255, 255))
        button_rect = button_text.get_rect()
        button_rect.bottomright = (self.size[0] - 10, self.size[1] - 10)

        # рисуем кнопку с закругленными углами
        button_border_rect = button_rect.inflate(10, 10)
        pygame.draw.rect(background, border_color, button_border_rect, border_radius=10, width=2)

        background.blit(button_text, button_rect)

        # рисуем задний фон уведомления
        screen.blit(background, screen_rect)

        # рисуем рамку уведомления с закругленными углами
        pygame.draw.rect(screen, border_color, screen_rect, border_radius=20, width=5)

        # сохраняем положение кнопки
        self.button_rect = pygame.Rect(
            screen_rect.left + button_rect.left,
            screen_rect.top + button_rect.top,
            button_rect.width,
            button_rect.height
        )

    def handle_event(self, event):
        """Обработчик событий"""

        # если невидима или нет кнопки
        if not self.is_visible or not self.button_rect:
            return

        # если нажата лкм
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            if self.button_rect.collidepoint(event.pos):
                if self.master and self.master.announcements:
                    # удалить событие
                    self.master.announcements.remove(self)

    def mouse_click(self, mouse_pos):
        """Обработчик нажатия кнопки"""

        if self.button_rect and self.button_rect.collidepoint(mouse_pos):
            if self.master and self.master.announcements:
                # удалить событие
                self.master.announcements.remove(self)
