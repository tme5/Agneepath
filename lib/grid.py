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
        self.is_path = False
        self.is_dragon = False
        self.is_wall = False
        self.is_intersection = False

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.is_dragon = False
        self.is_start = False
        self.is_end = False
        self.is_barrier = False
        self.is_intersection = False
        self.is_path = False
        self.is_wall = False
        self.color = TILE

    def make_start(self):
        self.is_dragon = False
        self.is_barrier = False
        self.is_end = False
        self.is_start = True

    def make_barrier(self):
        self.is_dragon = False
        self.is_path = False
        self.is_barrier = True

    def make_wall(self):
        self.is_wall = True
        
    def make_end(self):
        self.is_dragon = False
        self.is_path = False
        self.is_barrier = False
        self.is_start = False
        self.is_end = True

    def make_dragon(self):
        self.is_path = False
        self.is_barrier = False
        self.is_start = False
        self.is_dragon = True

    def make_path(self):
        if self.is_path:
            self.is_intersection = True
            self.is_path = False
        elif self.is_intersection:
            self.is_intersection = False
            self.is_path = True
        else:
            self.is_path = True

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier and not grid[self.row + 1][self.col].is_wall and not grid[self.row + 1][self.col].is_dragon: # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier and not grid[self.row - 1][self.col].is_wall and not grid[self.row - 1][self.col].is_dragon: # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier and not grid[self.row][self.col + 1].is_wall and not grid[self.row][self.col + 1].is_dragon: # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier and not grid[self.row][self.col - 1].is_wall and not grid[self.row][self.col - 1].is_dragon: # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
