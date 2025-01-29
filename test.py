import pygame
from collections import deque


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, 'white',
                                     (x * self.cell_size + self.left,
                                      y * self.cell_size + self.top, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, 'white',
                                     (x * self.cell_size + self.left,
                                      y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def get_cell(self, pos):
        cell_x = (pos[0] - self.left) // self.cell_size
        cell_y = (pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = not self.board[cell[1]][cell[0]]
        a = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    a.append((x, y))
        _, path = bfs(self.board, a[0], a[-1])
        print(path)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


data = [(0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (6, 8), (13, 8), (6, 9), (13, 9), (6, 10),
        (13, 10), (13, 11), (14, 11), (15, 11), (16, 11),
        (17, 11), (18, 11), (19, 11)]


def bfs(field, start, end):
    n = len(field)
    m = len(field[0])
    inf = 10 ** 9
    delta = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    d = [[inf] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()
    d[start[0]][start[1]] = 0
    used[start[0]][start[1]] = True
    queue.append(start)
    while len(queue) != 0:
        x, y = queue.popleft()
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            if not (not (0 <= nx < n) or not (0 <= ny < m) or used[nx][ny]) and field[nx][ny] == 1:
                d[nx][ny] = d[x][y] + 1
                p[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))
    way_len = d[end[1]][end[0]]

    curr = end[::-1]
    path = []
    while curr is not None:
        path.append(curr)
        curr = p[curr[0]][curr[1]]
    return way_len, path[:-1]


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('pygame')
    size = width, height = 20 * 30 + 10, 20 * 30 + 10
    screen = pygame.display.set_mode(size)

    fps = 60

    running = True
    clock = pygame.time.Clock()
    board = Board(20, 20)
    for (x, y) in data:
        board.board[y][x] = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
