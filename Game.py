import random
import pygame
import pygame_menu
from Cube import Cube
from Snake import Snake


class Game(object):
    width = 1700
    height = 1000
    rows = 20
    clocktick = 10
    snake = Snake((255, 0, 0), (10, 10))
    score = 0
    speed = 1

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake game !")
        self.is_running = True
        self.clock = pygame.time.Clock()

    def random_food(self, item):
        positions = item.body

        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # checks if x and y are in the list
                continue
            else:
                break

        return x, y

    def draw_window(self, surface, snake, food):
        surface.fill((0, 0, 0))
        snake.draw(surface)
        food.draw(surface)
        self.draw_grid(surface)

    def draw_grid(self, surface):
        size_btwn_w = (self.width - 200) // self.rows
        size_btwn_h = self.height // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x = x + size_btwn_w
            y = y + size_btwn_h

            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, self.width))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (self.width - 200, y))

    def start_menu(self):
        menu = pygame_menu.Menu(self.height, self.width, 'SNAKE',
                                theme=pygame_menu.themes.THEME_DARK)
        menu.add_label("Welcome to David's amazing Snake game !", max_char=-1, font_size=70)
        menu.add_label(' ', max_char=-1, font_size=70)
        menu.add_button('Play', self.game_loop, font_size=100)
        menu.add_label(' ', max_char=-1, font_size=70)
        menu.add_button('Quit', pygame_menu.events.EXIT, font_size=70)
        menu.mainloop(self.win)

    def end_menu(self, score):
        menu = pygame_menu.Menu(self.height, self.width, 'END',
                                theme=pygame_menu.themes.THEME_DARK)

        menu.add_label('YOUR SCORE: ' + str(score), max_char=-1, font_size=100)
        menu.add_label(' ', max_char=-1, font_size=100)
        menu.add_button('Play again', self.game_loop, font_size=75)
        menu.add_label(' ', max_char=-1, font_size=50)
        menu.add_button('Quit', pygame_menu.events.EXIT, font_size=75)
        menu.add_label(' ', max_char=-1, font_size=200)
        creator = "Made by David Audran"
        menu.add_label(creator, max_char=-1, font_size=20)
        menu.mainloop(self.win)

    def display_score(self, font):
        score_txt = font.render('Score :' + str(self.score), True, (255, 255, 255))
        score_rect = score_txt.get_rect()
        score_rect.center = (self.width - 100, 100)
        self.win.blit(score_txt, score_rect)

    def display_speed(self, font):
        speed_txt = font.render('Speed :' + str(self.speed), True, (255, 255, 255))
        speed_rect = speed_txt.get_rect()
        speed_rect.center = (self.width - 100, 200)
        self.win.blit(speed_txt, speed_rect)

    def check_collision(self):
        for x in range(len(self.snake.body)):
            if self.snake.body[x].pos in list(map(lambda z: z.pos, self.snake.body[x + 1:])):
                self.clocktick = 10
                self.snake.reset((10, 10))
                return True
        return False

    def check_food(self, food):
        if self.snake.body[0].pos == food.pos:
            self.snake.addCube()
            self.update_score_and_speed()
            return True

    def update_score_and_speed(self):
        self.score = len(self.snake.body) - 1
        if self.score % 5 == 0:
            self.speed += 1
            self.clocktick += 2

    def game_loop(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font('freesansbold.ttf', 32)
        food = Cube(self.random_food(self.snake), color=(0, 255, 0))
        while self.is_running:
            pygame.time.delay(50)
            clock.tick(self.clocktick)
            self.snake.move()
            if self.check_food(food):
                food = Cube(self.random_food(self.snake), color=(0, 255, 0))
            if self.check_collision():
                self.end_menu(self.score)
                break
            self.draw_window(self.win, self.snake, food)
            self.display_score(font)
            self.display_speed(font)
            pygame.display.update()