import time
import datetime
import os
import sys
import copy
import threading
from datetime import datetime

from lib.grid import Spot
from lib.operations import *
from lib.constants import *

THREAD_DRAW = False

class Agneepath:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Agneepath Incremental Pathfinding Algorithm")
        self.title = pygame.font.Font(TITLE, 80)
        self.font1 = pygame.font.Font(FONT1, 30)
        self.font2 = pygame.font.Font(FONT2, 40)
        self.font3 = pygame.font.Font(FONT2, 30)
        self.font4 = pygame.font.Font(FONT3, 30)
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        
    def main(self):
        i = 0
        click = False
        mainClock = pygame.time.Clock()
        
        bg = pygame.image.load(BG_IMAGE)
        logo = pygame.image.load(LOGO)
        textbox1_active = False
        textbox2_active = False
        user_input1 = '1'
        user_input2 = '1'
        self.start_count = 1
        self.end_count = 1

        while True:
            textbox1_border = BUTTON_BORDER
            textbox2_border = BUTTON_BORDER
            button1_border = BUTTON_BORDER
            button2_border = BUTTON_BORDER
            button3_border = BUTTON_BORDER
            button4_border = BUTTON_BORDER
            button5_border = BUTTON_BORDER
            self.win.fill((0,0,0))
            self.win.blit(bg, (0,0))
            self.draw_text('AGNEEPATH', self.title, BUTTON, self.win, 80, 10)
            self.draw_text('MAIN MENU', self.font1, YELLOW, self.win, 200, 150)
            self.draw_text('Enter start count', self.font4, YELLOW, self.win, 300, 90)
            self.draw_text('Enter end count', self.font4, YELLOW, self.win, 300, 130)

            self.win.blit(logo, (10, 10))
            mx, my = pygame.mouse.get_pos()

            textbox1 = pygame.Rect(500, 90, 50, 30)
            textbox2 = pygame.Rect(500, 130, 50, 30)
            button_1 = pygame.Rect(200, 200, 220, 50)
            button_2 = pygame.Rect(200, 260, 220, 50)
            button_3 = pygame.Rect(200, 320, 220, 50)
            button_4 = pygame.Rect(200, 380, 220, 50)
            button_5 = pygame.Rect(235, 440, 150, 50)

            if textbox1.collidepoint((mx, my)):
                textbox1_border = WHITE
                if click:
                    textbox1_active = not textbox1_active
                    click = False

            if textbox2.collidepoint((mx, my)):
                textbox2_border = WHITE
                if click:
                    textbox2_active = not textbox2_active
                    click = False

            if button_1.collidepoint((mx, my)):
                button1_border = WHITE
                if click:
                    self.play_game()
                    click = False
            
            if button_2.collidepoint((mx, my)):
                button2_border = WHITE
                if click:
                    self.static_maze()
                    click = False
            
            if button_3.collidepoint((mx, my)):
                button3_border = WHITE
                if click:
                    self.dynamic_maze()
                    click = False
            
            if button_4.collidepoint((mx, my)):
                button4_border = WHITE
                if click:
                    self.custom_maze()
                    click = False
            
            if button_5.collidepoint((mx, my)):
                button5_border = WHITE
                if click:
                    pygame.quit()
                    sys.exit()

            if textbox1_active:
                pygame.draw.rect(self.win, textbox1_border, textbox1, 5)
                pygame.draw.rect(self.win, BUTTON, textbox1)
            else:
                pygame.draw.rect(self.win, textbox1_border, textbox1, 5)
                pygame.draw.rect(self.win, BUTTON_BORDER, textbox1)
            
            if textbox2_active:
                pygame.draw.rect(self.win, textbox2_border, textbox2, 5)
                pygame.draw.rect(self.win, BUTTON, textbox2)
            else:
                pygame.draw.rect(self.win, textbox2_border, textbox2, 5)
                pygame.draw.rect(self.win, BUTTON_BORDER, textbox2)
            
            pygame.draw.rect(self.win, BUTTON, button_1, 0, 30)
            pygame.draw.rect(self.win, button1_border, button_1, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_2, 0, 30)
            pygame.draw.rect(self.win, button2_border, button_2, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_3, 0, 30)
            pygame.draw.rect(self.win, button3_border, button_3, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_4, 0, 30)
            pygame.draw.rect(self.win, button4_border, button_4, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_5, 0, 30)
            pygame.draw.rect(self.win, button5_border, button_5, 5, 30)

            self.draw_text('PLAY GAME', self.font2, YELLOW, self.win, 245, 207)
            self.draw_text('STATIC MAZE', self.font2, YELLOW, self.win, 235, 267)
            self.draw_text('DYNAMIC MAZE', self.font2, YELLOW, self.win, 230, 327)
            self.draw_text('CUSTOM MAZE', self.font2, YELLOW, self.win, 230, 387)
            self.draw_text('QUIT', self.font2, YELLOW, self.win, 285, 447)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if textbox1_active:
                        if event.key == pygame.K_RETURN:
                            self.start_count = int(user_input1)
                            textbox1_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_input1 = user_input1[:-1]
                        else:
                            user_input1 += event.unicode
                    if textbox2_active:
                        if event.key == pygame.K_RETURN:
                            self.end_count = int(user_input2)
                            textbox2_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_input2 = user_input2[:-1]
                        else:
                            user_input2 += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.draw_text(user_input1, self.font3, YELLOW, self.win, 510, 90)
            self.draw_text(user_input2, self.font3, YELLOW, self.win, 510, 130)
            pygame.display.update()
            mainClock.tick(10)

    def play_game(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        with open(MAZE_CONF, 'r') as f:
            f_rd = f.readlines()
        i = 0
        for ln in f_rd:
            j = 0
            for conf in ln.split(','):
                if int(conf):
                    grid[j][i].make_wall()
                j += 1
            i += 1
        
        start = grid[1][0]
        start.make_start()
        end = grid[19][18]
        end.make_end()
        dragon = grid[10][9]
        dragon.make_dragon()
        astar_path = False
        find_path = False
        run = True
        count = COUNT
        delay = False
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_LEFT:
                            if not grid[dragon.row - 1][dragon.col].is_wall and not grid[dragon.row - 1][dragon.col].is_end:
                                dragon.reset()
                                if dragon == start:
                                    start = None
                                dragon = grid[dragon.row -1][dragon.col]
                                dragon.make_dragon()
                        elif event.key==pygame.K_UP:
                            if not grid[dragon.row][dragon.col - 1].is_wall and not grid[dragon.row][dragon.col - 1].is_end:
                                dragon.reset()
                                if dragon == start:
                                    start = None
                                dragon = grid[dragon.row][dragon.col - 1]
                                dragon.make_dragon()
                        elif event.key==pygame.K_RIGHT:
                            if not grid[dragon.row + 1][dragon.col].is_wall and not grid[dragon.row + 1][dragon.col].is_end:
                                dragon.reset()
                                if dragon == start:
                                    start = None
                                dragon = grid[dragon.row + 1][dragon.col]
                                dragon.make_dragon()
                        elif event.key==pygame.K_DOWN:
                            if not grid[dragon.row][dragon.col + 1].is_wall and not grid[dragon.row][dragon.col + 1].is_end:
                                dragon.reset()
                                if dragon == start:
                                    start = None
                                dragon = grid[dragon.row][dragon.col + 1]
                                dragon.make_dragon()
                        elif event.key == pygame.K_ESCAPE:
                            run = False
                            return
                        elif event.key == pygame.K_SPACE and start and end:
                            find_path = True
                            count = 0
                if delay:
                    count -=1
            elif start == dragon:
                delay = False
                for spot in astar_path:
                    if not spot.is_dragon:
                        spot.reset()
                find_path = False
                count = COUNT
                pygame.draw.rect(self.win, BUTTON, pygame.Rect(170, 215, 230, 80), 0, 30)
                pygame.draw.rect(self.win, BUTTON_BORDER, pygame.Rect(170, 215, 230, 80), 5, 30)
                self.draw_text('YOU ARE CAUGHT!!!', self.font3, BLACK, self.win, 205, 225)
                self.draw_text('GOING TO MAIN MENU.', self.font3, BLACK, self.win, 200, 255)
                pygame.display.update()
                time.sleep(5)
                run = False
                return
            else:
                if find_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    astar_path = algorithm(lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH), grid, end, start)
                    find_path = False
                if astar_path:
                    if len([spot for spot in astar_path if spot.is_dragon]) > 0:
                        for spot in astar_path:
                            if not spot.is_dragon:
                                spot.reset()
                        find_path = True
                    if not find_path:
                        if start in astar_path:
                            start.reset()
                            start = astar_path.pop(start)
                            start.make_start()
                            delay = True
                            count = COUNT
                        if start is end:
                            end.make_end()
                            delay = False
                            count = COUNT

    def static_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        with open(MAZE_CONF, 'r') as f:
            f_rd = f.readlines()
        i = 0
        for ln in f_rd:
            j = 0
            for conf in ln.split(','):
                if int(conf):
                    grid[j][i].make_wall()
                j += 1
            i += 1
        
        grid[1][0].make_start()
        grid[19][18].make_end()

        start = grid[1][0]
        end = grid[19][18]
        astar_path = False
        find_path = False
        run = True
        count = COUNT
        delay = False
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return

                    if pygame.mouse.get_pressed()[0]: # LEFT
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if not start and spot != end:
                            start = spot
                            start.make_start()
                            
                        elif not end and spot != start:
                            end = spot
                            end.make_end()

                        elif spot != end and spot != start and not spot.is_wall:
                            barrier_count += 1
                            prev_barrier_count += 1
                            spot.make_barrier()

                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if spot.is_barrier:
                            barrier_count -= 1
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return
                        if event.key == pygame.K_SPACE and start and end:
                            find_path = True
                            count = 0
                if delay:
                    count -=1
            elif not find_path and not astar_path:
                pygame.draw.rect(self.win, BUTTON, pygame.Rect(170, 215, 230, 80), 0, 30)
                pygame.draw.rect(self.win, BUTTON_BORDER, pygame.Rect(170, 215, 230, 80), 5, 30)
                self.draw_text('CANNOT FIND PATH', self.font3, BLACK, self.win, 205, 225)
                self.draw_text('GOING TO MAIN MENU.', self.font3, BLACK, self.win, 200, 255)
                pygame.display.update()
                time.sleep(5)
                run = False
                return
            else:
                if find_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    astar_path = algorithm(lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH), grid, end, start)
                    find_path = False
                if astar_path:
                    if len([spot for spot in astar_path if spot.is_barrier]) > 0:
                        for spot in astar_path:
                            if not spot.is_barrier:
                                spot.reset()
                        find_path = True
                    if barrier_count < prev_barrier_count:
                        prev_barrier_count = barrier_count
                        for spot in astar_path:
                            if not spot.is_barrier:
                                spot.reset()
                        find_path = True
                    if not find_path:
                        if start in astar_path:
                            start.reset()
                            start = astar_path.pop(start)
                            start.make_start()
                            delay = True
                            count = COUNT
                        if start is end:
                            end.make_end()
                            delay = False
                            count = COUNT

    def dynamic_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        with open(MAZE_CONF, 'r') as f:
            f_rd = f.readlines()
        i = 0
        for ln in f_rd:
            j = 0
            for conf in ln.split(','):
                if int(conf):
                    grid[j][i].make_wall()
                j += 1
            i += 1
        
        grid[1][0].make_start()
        grid[19][18].make_end()

        start = grid[1][0]
        end = grid[19][18]
        astar_path = False
        find_path = False
        run = True
        count = COUNT
        delay = False
        delta = 1
        auto_add = False
        dyn_bar_pos = copy.deepcopy(DYN_BAR_POS)
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return
                        if event.key == pygame.K_SPACE and start and end:
                            find_path = True
                            dyn_time = datetime.datetime.now() + datetime.timedelta(seconds = delta)
                            auto_add = True
                            count = 0
                if delay:
                    count -=1
            else:
                if len(dyn_bar_pos) > 0 and auto_add:
                    if dyn_time <= datetime.datetime.now():
                        dyn_time = datetime.datetime.now() + datetime.timedelta(seconds = delta)
                        pos = dyn_bar_pos.pop(0)
                        grid[pos[0]][pos[1]].make_barrier()
                if find_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    astar_path = algorithm(lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH), grid, end, start)
                    find_path = False
                if astar_path:
                    if len([spot for spot in astar_path if spot.is_barrier]) > 0:
                        for spot in astar_path:
                            if not spot.is_barrier:
                                spot.reset()
                        find_path = True
                    if not find_path:
                        if start in astar_path:
                            start.reset()
                            start = astar_path.pop(start)
                            start.make_start()
                            delay = True
                            count = COUNT
                        if start is end:
                            end.make_end()
                            delay = False
                            count = COUNT

    def solve(self, name, grid, start, end):
        global THREAD_DRAW
        astar_path = False
        find_path = True
        count = 0
        delay = False
        run = True
        print("%s starts:" %name, datetime.now())
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if pygame.mouse.get_pressed()[0]: # LEFT
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if not spot.is_end and not spot.is_start:
                            spot.make_barrier()
                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        spot.reset()
                        if not spot.is_end and not spot.is_start:
                            spot.reset()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                if delay:
                    count -=1
            else:
                if find_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    astar_path = algorithm(lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH), grid, end, start)
                    find_path = False
                if astar_path:
                    _barriers = len([spot for spot in astar_path if spot.is_barrier])
                    _walls = len([spot for spot in astar_path if spot.is_wall])
                    _dragons = len([spot for spot in astar_path if spot.is_dragon])
                    if _barriers > 0 or _walls > 0 or _dragons > 0:
                        for spot in astar_path:
                            if not spot.is_barrier and not spot.is_wall and not spot.is_dragon:
                                spot.reset()
                            if spot.is_intersection:
                                spot.make_path()
                        find_paths = True
                    if not find_path:
                        if start in astar_path:
                            if not astar_path[start].is_start:
                                if start.is_intersection:
                                    start.reset()
                                    start.make_path()
                                else:
                                    start.reset()
                                start = astar_path.pop(start)
                                start.make_start()
                            delay = True
                            count = COUNT
                        if start is end:
                            end.is_start = False
                            end.make_end()
                            print("%s ends:" %name, datetime.now())
                            run = False
                if not astar_path and not find_path:
                    raise Exception("Cannot find astar_path.")

    def custom_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        start_list = []
        end = None
        run = True
        solve_flag = True
        self.astar_paths = {}
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]: # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                    spot = grid[row][col]
                    if len(start_list) != int(self.start_count) and spot != end:
                        spot.make_start()
                        start_list.append(spot)
                        
                    elif not end and not spot.is_start:
                        end = spot
                        end.make_end()

                    elif not spot.is_end and not spot.is_start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                    spot = grid[row][col]
                    spot.reset()
                    if spot in start_list:
                        start_list = [start for start in start_list if spot != start]
                    if spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        solve_flag = False
                    if event.key == pygame.K_SPACE and len(start_list) == self.start_count and end:
                        run = False
                    if event.key == pygame.K_c:
                        start_list = []
                        end = None
                        grid = make_grid(TOTAL_ROWS, WIDTH)
        
        if solve_flag:
            threads = []
            for i, start in enumerate(start_list):
                t = threading.Thread(target=self.solve, args=('man_%s' %i, grid, start, end))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                            
if __name__ == '__main__':
    test_obj = Agneepath()
    test_obj.main()