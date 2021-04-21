import math
from .grid import *
import os
import time 

cwd = os.getcwd()
man = pygame.image.load(os.path.join(cwd, MAN_IMG))
fire = pygame.image.load(os.path.join(cwd, FIRE_IMG))
door = pygame.image.load(os.path.join(cwd, DOOR_IMG))
tile = pygame.image.load(os.path.join(cwd, TILE_IMG))
path = pygame.image.load(os.path.join(cwd, PATH_IMG))
dragon = pygame.image.load(os.path.join(cwd, DRAGON_IMG))
wall = pygame.image.load(os.path.join(cwd, WALL_IMG))
intr_section = pygame.image.load(os.path.join(cwd, INTER_IMG))

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return came_from
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if not current.is_end:
            current.make_path()
        draw()

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            if spot.is_start:
                win.blit(man, (spot.x, spot.y))
            elif spot.is_path:
                win.blit(path, (spot.x, spot.y))
            elif spot.is_barrier:
                win.blit(fire, (spot.x, spot.y))
            elif spot.is_end:
                win.blit(door, (spot.x, spot.y))
            elif spot.is_dragon:
                win.blit(dragon, (spot.x, spot.y))
            elif spot.is_wall:
                win.blit(wall, (spot.x, spot.y))
            elif spot.is_intersection:
                win.blit(intr_section, (spot.x, spot.y))
            else:
                win.blit(tile, (spot.x, spot.y))
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def get_barrier_count(grid):
    barrier_count = 0
    for row in grid:
        temp_count = len([spot for spot in row if spot.is_barrier])
        barrier_count += temp_count
    return barrier_count
