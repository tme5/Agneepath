import time
import os
import sys
from lib.grid import Spot
from lib.operations import *
from lib.constants import *

class Agneepath:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Agneepath Incremental Pathfinding Algorithm")
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        
    def main(self):
        click = False
        mainClock = pygame.time.Clock()
        title = pygame.font.Font(TITLE, 80)
        font1 = pygame.font.Font(FONT1, 30)
        font2 = pygame.font.Font(FONT2, 40)

        bg = pygame.image.load(BG_IMAGE)
        while True:
            self.win.fill((0,0,0))
            self.win.blit(bg, (0,0))
            self.draw_text('AGNEEPATH', title, BUTTON, self.win, 10, 10)
            self.draw_text('MAIN MENU', font1, (255, 255, 255), self.win, 20, 90)

            mx, my = pygame.mouse.get_pos()
    
            button_1 = pygame.Rect(200, 200, 220, 50)
            button_2 = pygame.Rect(200, 260, 220, 50)
            button_3 = pygame.Rect(200, 320, 220, 50)
            button_4 = pygame.Rect(200, 380, 220, 50)
            button_5 = pygame.Rect(235, 440, 150, 50)

            if button_1.collidepoint((mx, my)):
                if click:
                    self.static_maze()
                    click = False
            
            if button_2.collidepoint((mx, my)):
                if click:
                    self.dynamic_maze()
                    click = False
            
            if button_3.collidepoint((mx, my)):
                if click:
                    self.moving_maze()
                    click = False
            
            if button_4.collidepoint((mx, my)):
                if click:
                    self.custom_maze()
                    click = False
            
            if button_5.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.win, BUTTON, button_1, 0, 30)
            pygame.draw.rect(self.win, BUTTON_BORDER, button_1, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_2, 0, 30)
            pygame.draw.rect(self.win, BUTTON_BORDER, button_2, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_3, 0, 30)
            pygame.draw.rect(self.win, BUTTON_BORDER, button_3, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_4, 0, 30)
            pygame.draw.rect(self.win, BUTTON_BORDER, button_4, 5, 30)

            pygame.draw.rect(self.win, BUTTON, button_5, 0, 30)
            pygame.draw.rect(self.win, BUTTON_BORDER, button_5, 5, 30)

            self.draw_text('STATIC MAZE', font2, (255, 255, 255), self.win, 235, 207)
            self.draw_text('DYNAMIC MAZE', font2, (255, 255, 255), self.win, 230, 267)
            self.draw_text('MOVING MAZE', font2, (255, 255, 255), self.win, 230, 327)
            self.draw_text('CUSTOM MAZE', font2, (255, 255, 255), self.win, 230, 387)
            self.draw_text('QUIT', font2, (255, 255, 255), self.win, 285, 447)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
            pygame.display.update()
            mainClock.tick(10)

    def static_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        with open(MAZE_CONF, 'r') as f:
            f_rd = f.readlines()
        i = 0
        for ln in f_rd:
            j = 0
            for conf in ln.split(','):
                if int(conf):
                    grid[j][i].make_barrier()
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
                            count = 0
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

    def custom_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        start = None
        end = None
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

                        elif spot != end and spot != start:
                            spot.make_barrier()

                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                        if event.key == pygame.K_SPACE and start and end:
                            find_path = True
                            count = 0
                            
                        if event.key == pygame.K_c:
                            start = None
                            end = None
                            grid = make_grid(TOTAL_ROWS, WIDTH)
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
                    
if __name__ == '__main__':
    test_obj = Agneepath()
    test_obj.main()