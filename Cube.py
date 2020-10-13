import pygame


class Cube(object):
    rows = 20
    w = 1700
    h = 1000

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface):
        dis_i = (self.w - 200)// self.rows
        dis_j = self.h // self.rows
        i = self.pos[0]
        j = self.pos[1]

        if i <= 19:
            pygame.draw.rect(surface, self.color, (i * dis_i + 1, j * dis_j + 1, dis_i - 2, dis_j - 2))
