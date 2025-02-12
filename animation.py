import pygame
import time


class Animation(pygame.sprite.Sprite):
    """Рисует анимацию в выбранном месте. Составляет анимацию из img_count картинок. Картинки должны быть названы
    image + num, где num - номер картинки от 1 до img_count. Каждая картинка показывается speed секунд."""

    def __init__(self, board, pos, image, img_count, speed, img_type='png', resize_to=(32, 32)):
        super().__init__()
        self.img_type = img_type
        self.board = board
        self.image_str = image
        self.resize_to = resize_to

        # первая картинка с номером 1
        self.image = pygame.image.load(image + '1' + '.' + self.img_type).convert_alpha()
        self.image = pygame.transform.scale(self.image, resize_to)
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.pos = pos
        self.speed = speed
        self.prev_time = time.time()
        self.count = 0
        self.img_count = img_count

    def update(self, screen):
        """Обновляет анимацию"""

        # если с прошлого отображения картинки прошло больше speed секунд, то переход на следующую картинку
        if time.time() - self.prev_time > self.speed:
            self.prev_time = time.time()
            self.count += 1
            self.image = pygame.image.load(self.image_str + str(self.count) + '.' + self.img_type).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.resize_to)
            self.rect = self.image.get_rect(center=self.rect.center)

        # рисуем картинку
        screen.blit(self.image, self.rect)

        # если анимация закончилась, то удаляем ее3
        if self.count >= self.img_count:
            self.kill()
            self.board.animation_list.remove(self)
