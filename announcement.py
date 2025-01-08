import pygame


def draw_rounded_rect(surface, color, rect, border_radius, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius, width=width)


def render_multiline_text(surface, text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = f'{current_line} {word}'.strip()
        if font.size(test_line)[0] > rect.width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)

    total_height = len(lines) * font.size(lines[0])[1]
    y_offset = rect.top + (rect.height - total_height) // 2
    for line in lines:
        rendered_text = font.render(line, True, color)
        text_width = font.size(line)[0]
        x_offset = rect.left + (rect.width - text_width) // 2
        surface.blit(rendered_text, (x_offset, y_offset))
        y_offset += font.size(line)[1]


class Announcement:
    def __init__(self, content=None, size=(300, 300), font_size=20, position='center', background_image=None, master=None, render_func=None):
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
        self.render_func = render_func  # Новый параметр

    def render(self, screen):
        if not self.is_visible:
            return

        if self.render_func:
            # Используем пользовательскую функцию для рендера
            self.render_func(screen)
            return

        if self.background_image:
            background = self.background_image.copy()
        else:
            background = pygame.Surface(self.size, pygame.SRCALPHA)
            background.fill((0, 0, 0, 0))
            rect_color = (50, 205, 50)
            draw_rounded_rect(background, rect_color, pygame.Rect(0, 0, *self.size), border_radius=20)

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

        # Рендер текста с переносом строк
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        text_rect = pygame.Rect(10, 10, self.size[0] - 20, self.size[1] - 60)  # Оставляем место для кнопки
        render_multiline_text(background, self.content, font, (255, 255, 255), text_rect)

        # Рендер кнопки "ОК"
        button_font = pygame.font.Font('freesansbold.ttf', 16)
        button_text = button_font.render('OK', True, (255, 255, 255))
        button_rect = button_text.get_rect()
        button_rect.bottomright = (self.size[0] - 10, self.size[1] - 10)

        # Рисуем кнопку с закругленными углами
        button_border_rect = button_rect.inflate(10, 10)
        draw_rounded_rect(background, border_color, button_border_rect, border_radius=10, width=2)
        background.blit(button_text, button_rect)

        # Рисуем уведомление на основном экране
        screen.blit(background, screen_rect)

        # Рисуем рамку уведомления с закругленными углами
        draw_rounded_rect(screen, border_color, screen_rect, border_radius=20, width=5)

        # Сохраняем положение кнопки в координатах экрана
        self.button_rect = pygame.Rect(
            screen_rect.left + button_rect.left,
            screen_rect.top + button_rect.top,
            button_rect.width,
            button_rect.height
        )

    def handle_event(self, event):
        if not self.is_visible or not self.button_rect:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            if self.button_rect.collidepoint(event.pos):
                if self.master and self.master.announcements:
                    self.master.announcements.remove(self)

    def mouse_click(self, mouse_pos):
        if self.button_rect and self.button_rect.collidepoint(mouse_pos):
            if self.master and self.master.announcements:
                self.master.announcements.remove(self)


