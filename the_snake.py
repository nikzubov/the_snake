from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (177, 179, 177)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для всех объектов игры."""

    def __init__(self):
        """Инициализация родительского класса"""
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.body_color = None

    def draw(self, position, surface):
        """Метод отрисовки объектов."""
        rect = pygame.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def randomizer(self):
        """Метод обновления позиции объекта."""
        return (
            randint(0, SCREEN_WIDTH) // GRID_SIZE * GRID_SIZE,
            randint(0, SCREEN_HEIGHT) // GRID_SIZE * GRID_SIZE
        )


class Apple(GameObject):
    """Класс для игрового объекта, яблоко."""

    body_color = APPLE_COLOR

    def __init__(self):
        """Инициализация яблока."""
        self.position = super().randomizer()

    def randomize_position(self):
        """Метод обновления позиции яблока."""
        self.position = super().randomizer()

    def draw(self, surface):
        """Метод отрисовки яблока."""
        super().draw(self.position, surface)


class Stone(GameObject):
    """Класс для игрового объекта, камень"""

    body_color = STONE_COLOR

    def __init__(self):
        """Инициализация камня."""
        self.position = super().randomizer()

    def randomize_position(self):
        """Метод обновления позиции яблока."""
        dead_stone = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, dead_stone)
        self.position = super().randomizer()

    def draw(self, surface):
        """Метод отрисовки камня."""
        super().draw(self.position, surface)


class Snake(GameObject):
    """Класс для игрового объекта, змейка."""

    position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    def __init__(self):
        """Инициализация змейки."""
        self.length = 1
        self.positions = self.position
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = self.positions[-1]
        self.upp = 0

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        direction = (
            self.direction[0] * GRID_SIZE + self.positions[0][0],
            self.direction[1] * GRID_SIZE + self.positions[0][1]
        )
        self.positions.insert(0, direction)
        self.last = self.positions[-1]
        if self.get_head_position()[0] >= SCREEN_WIDTH:
            self.positions.insert(0, (0, self.positions[0][1]))
            del self.positions[1]
        elif self.get_head_position()[0] < 0:
            self.positions.insert(0, (SCREEN_WIDTH, self.positions[0][1]))
            del self.positions[1]
        elif self.get_head_position()[1] >= SCREEN_HEIGHT:
            self.positions.insert(0, (self.positions[0][0], 0))
            del self.positions[1]
        elif self.get_head_position()[1] < 0:
            self.positions.insert(0, (self.positions[0][0], SCREEN_HEIGHT))
            del self.positions[1]
        del self.positions[-1]
        self.draw(screen)

    def draw(self, surface):
        """Метод отрисовки змейки."""
        for position in self.positions[:-1]:
            GameObject.draw(self, position, surface)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения координат головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывания змейки в начально положение."""
        for pos in self.positions:
            dead_snake = pygame.Rect(
                (pos[0], pos[1]),
                (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, dead_snake)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]


def keys_down(game_object, event):
    """Функция обработки нажатых клавиш."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and game_object.direction != DOWN:
            game_object.next_direction = UP
        elif event.key == pygame.K_DOWN and game_object.direction != UP:
            game_object.next_direction = DOWN
        elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
            game_object.next_direction = LEFT
        elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
            game_object.next_direction = RIGHT
        elif event.key == pygame.K_LSHIFT:
            game_object.upp = 20


def keys_up(game_object, event):
    """Функция обработки отпущенных клавиш."""
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LSHIFT:
            game_object.upp = 0


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        keys_down(game_object, event)
        keys_up(game_object, event)


def main():
    """Непосредственно игра."""
    snake = Snake()
    apple = Apple()
    stone = Stone()

    while True:
        clock.tick(SPEED + snake.upp)
        handle_keys(snake)
        while apple.position in snake.positions:
            apple.randomize_position()
        while (
            stone.position in snake.position
                or stone.position in apple.position
        ):
            stone.randomize_position()
        snake.draw(screen)
        apple.draw(screen)
        stone.draw(screen)
        snake.move()
        if snake.next_direction:
            snake.update_direction()
            snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            snake.positions.insert(0, snake.get_head_position())

            stone.randomize_position()
        if stone.position == snake.get_head_position():
            snake.length = 1
            snake.reset()
        if snake.get_head_position() in snake.positions[2:]:
            snake.length = 1
            snake.reset()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
