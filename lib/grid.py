import pygame
import math
from queue import PriorityQueue
from .constants import *

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * self.width
        self.y = col * self.width
        self.color = TILE
        self.neighbors = []
        self.total_rows = total_rows
        self.is_start = False
        self.is_end = False
        self.is_barrier = False

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.is_start = False
        self.is_end = False
        self.is_barrier = False
        self.color = TILE

    def make_start(self):
        self.is_start = True

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.is_barrier = True

    def make_end(self):
        self.is_end = True

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier: # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier: # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier: # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier: # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
