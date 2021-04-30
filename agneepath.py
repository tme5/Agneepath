import time
import datetime
import os
import sys
import copy
import threading
import random
import datetime

from lib.grid import Spot
from lib.operations import *
from lib.constants import *

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
        self.sound_flag = True
        self.music_flag = True
        self.play = True
        self.play_sound = True
        sound_hover = False
        music_hover = False
        sound_icon = pygame.image.load(SOUND_ICON).convert()
        music_icon = pygame.image.load(MUSIC_ICON).convert()
        no_sound_icon = pygame.image.load(NO_SOUND_ICON).convert()
        no_music_icon = pygame.image.load(NO_MUSIC_ICON).convert()
        textbox1_active = False
        textbox2_active = False
        user_input1 = '2'
        user_input2 = '3'
        self.start_count = int(user_input1)
        self.end_count = int(user_input2)
        self.music = pygame.mixer.music.load(BG_MUSIC)
        self.click_sound = pygame.mixer.Sound(CLICK_SOUND)
        self.footstep_sound = pygame.mixer.Sound(FOOTSTEP_SOUND)
        pygame.mixer.Sound.set_volume(self.footstep_sound, 0.2)
        self.eat_sound = pygame.mixer.Sound(EAT_SOUND)

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
            self.draw_text('MAIN MENU', self.font1, YELLOW, self.win, 200, 170)
            self.draw_text('Enter start count', self.font4, YELLOW, self.win, 300, 90)
            self.draw_text('Enter end count', self.font4, YELLOW, self.win, 300, 130)

            self.win.blit(logo, (10, 10))
            music_box = pygame.Rect(549, 499, 42, 42)
            sound_box = pygame.Rect(549, 549, 42, 42)
            if self.sound_flag:
                sound_icon.set_colorkey(WHITE)
                self.win.blit(sound_icon, (550, 550))
                self.play_sound = True
            else:
                no_sound_icon.set_colorkey(WHITE)
                self.win.blit(no_sound_icon, (550, 550))
                self.play_sound = False
            
            if self.music_flag:
                music_icon.set_colorkey(WHITE)
                self.win.blit(music_icon, (550, 500))
                if self.play:
                    pygame.mixer.music.play()
                    self.play = False
            else:
                no_music_icon.set_colorkey(WHITE)
                self.win.blit(no_music_icon, (550, 500))
                pygame.mixer.music.stop()
                self.play = True
            if sound_hover:
                pygame.draw.rect(self.win, WHITE, sound_box, 3, 21)
                sound_hover = False
            else:
                pygame.draw.rect(self.win, BUTTON_BORDER, sound_box, 3, 21)
            if music_hover:
                pygame.draw.rect(self.win, WHITE, music_box, 3, 21)
                music_hover = False
            else:
                pygame.draw.rect(self.win, BUTTON_BORDER, music_box, 3, 21)
            
            mx, my = pygame.mouse.get_pos()

            textbox1 = pygame.Rect(500, 90, 50, 30)
            textbox2 = pygame.Rect(500, 130, 50, 30)
            button_1 = pygame.Rect(200, 220, 220, 50)
            button_2 = pygame.Rect(200, 280, 220, 50)
            button_3 = pygame.Rect(200, 340, 220, 50)
            button_4 = pygame.Rect(200, 400, 220, 50)
            button_5 = pygame.Rect(235, 460, 150, 50)

            if music_box.collidepoint((mx, my)):
                music_hover = True
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.music_flag = not self.music_flag
                    click = False
            if sound_box.collidepoint((mx, my)):
                sound_hover = True
                audio_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.sound_flag = not self.sound_flag
                    click = False

            if textbox1.collidepoint((mx, my)):
                textbox1_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    textbox1_active = not textbox1_active
                    click = False

            if textbox2.collidepoint((mx, my)):
                textbox2_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    textbox2_active = not textbox2_active
                    click = False

            if button_1.collidepoint((mx, my)):
                button1_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.play_game()
                    click = False
            
            if button_2.collidepoint((mx, my)):
                button2_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.static_maze()
                    click = False
            
            if button_3.collidepoint((mx, my)):
                button3_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.dynamic_maze()
                    click = False
            
            if button_4.collidepoint((mx, my)):
                button4_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
                    self.custom_maze()
                    click = False
            
            if button_5.collidepoint((mx, my)):
                button5_border = WHITE
                if click:
                    if self.play_sound:
                        self.click_sound.play()
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

            self.draw_text('PLAY GAME', self.font2, YELLOW, self.win, 245, 227)
            self.draw_text('STATIC MAZE', self.font2, YELLOW, self.win, 235, 287)
            self.draw_text('DYNAMIC MAZE', self.font2, YELLOW, self.win, 230, 347)
            self.draw_text('CUSTOM MAZE', self.font2, YELLOW, self.win, 230, 407)
            self.draw_text('QUIT', self.font2, YELLOW, self.win, 285, 467)

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
        
        self.start_list = []
        self.end_list = []
        while len(self.start_list) < self.start_count:
            row = random.randint(0,10)
            col = random.randint(0,10)
            spot = grid[row][col]
            if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_intersection and not spot.is_dragon and not spot.is_wall:
                spot.make_start()
                self.start_list.append(spot)

        while len(self.end_list) < self.end_count:
            row = random.randint(10,19)
            col = random.randint(10,19)
            spot = grid[row][col]
            if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_intersection and not spot.is_dragon and not spot.is_wall:
                spot.make_end()
                self.end_list.append(spot)
        dragon = False
        while not dragon:
            row = random.randint(0,19)
            col = random.randint(0,19)
            spot = grid[row][col]
            if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_intersection and not spot.is_dragon and not spot.is_wall:
                dragon = spot
                dragon.make_dragon()

        self.path_obj_dict = {}
        run = True
        update_path = False
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        count = COUNT
        delay = False
        caught = 0
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    if event.type == pygame.KEYDOWN:
                        if self.play_sound:
                            self.click_sound.play()
                        if event.key==pygame.K_LEFT:
                            if not grid[dragon.row - 1][dragon.col].is_wall and not grid[dragon.row - 1][dragon.col].is_end:
                                dragon.reset()
                                dragon = grid[dragon.row -1][dragon.col]
                                dragon.make_dragon()
                        elif event.key==pygame.K_UP:
                            if not grid[dragon.row][dragon.col - 1].is_wall and not grid[dragon.row][dragon.col - 1].is_end:
                                dragon.reset()
                                dragon = grid[dragon.row][dragon.col - 1]
                                dragon.make_dragon()
                        elif event.key==pygame.K_RIGHT:
                            if not grid[dragon.row + 1][dragon.col].is_wall and not grid[dragon.row + 1][dragon.col].is_end:
                                dragon.reset()
                                dragon = grid[dragon.row + 1][dragon.col]
                                dragon.make_dragon()
                        elif event.key==pygame.K_DOWN:
                            if not grid[dragon.row][dragon.col + 1].is_wall and not grid[dragon.row][dragon.col + 1].is_end:
                                dragon.reset()
                                dragon = grid[dragon.row][dragon.col + 1]
                                dragon.make_dragon()
                        elif event.key == pygame.K_ESCAPE:
                            run = False
                        elif event.key == pygame.K_SPACE and len(self.start_list) == self.start_count and len(self.end_list) == self.end_count and dragon:
                            update_path = True
                            count = 0
                if delay:
                    count -=1
            elif not self.start_list:
                delay = False
                count = COUNT
                pygame.draw.rect(self.win, BUTTON, pygame.Rect(175, 215, 240, 80), 0, 30)
                pygame.draw.rect(self.win, BUTTON_BORDER, pygame.Rect(175, 215, 240, 80), 5, 30)
                if caught:
                    self.draw_text('YOU CAUGHT %s PREY!!!' %caught, self.font3, BLACK, self.win, 205, 225)
                else:
                    self.draw_text('ALL PREY WENT HOME', self.font3, BLACK, self.win, 205, 225)
                self.draw_text('GOING TO MAIN MENU.', self.font3, BLACK, self.win, 200, 255)
                pygame.display.update()
                time.sleep(5)
                run = False
                return
            else:
                if dragon in self.start_list:
                    caught += 1
                    if self.play_sound:
                        self.eat_sound.play()
                    for i, start in enumerate(self.start_list):
                        if dragon == start and self.path_obj_dict and 'man_%s' %i in self.path_obj_dict:
                            for spot in self.path_obj_dict['man_%s' %i][2]:
                                if not spot.is_barrier and not spot.is_dragon:
                                    spot.reset()
                    self.start_list = [start for start in self.start_list if start != dragon]
                    dragon.is_start = False
                if update_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    threads = []
                    for i, start in enumerate(self.start_list):
                        if self.path_obj_dict and 'man_%s' %i in self.path_obj_dict:
                            for spot in self.path_obj_dict['man_%s' %i][2]:
                                if not spot.is_barrier and not spot.is_dragon:
                                    spot.reset()
                        self.path_obj_dict['man_%s' %i] = [start, self.end_list, False]
                        t = threading.Thread(target=self.solve, args=('man_%s' %i, grid))
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                    update_path = False
                if self.start_list and self.path_obj_dict:
                    for i, start in enumerate(self.start_list):
                        _path_obj = self.path_obj_dict['man_%s' %i]
                        if not len(_path_obj[2]):
                            start.reset()
                            print('Man %s has reached' %i)
                            self.start_list.pop(i)
                        if len([spot for spot in _path_obj[2] if spot.is_barrier]) > 0 or len([spot for spot in _path_obj[2] if spot.is_dragon]) > 0:
                            update_path = True
                        if barrier_count < prev_barrier_count:
                            prev_barrier_count = barrier_count
                            update_path = True
                        if not update_path and len(_path_obj[2]) > 0:
                            if not _path_obj[2][0].is_start:
                                if start.is_intersection:
                                    start.reset()
                                    start.make_path()
                                else:
                                    start.reset()
                                start = _path_obj[2].pop(0)
                                start.make_start()
                                if self.play_sound:
                                    self.footstep_sound.play()
                                self.start_list[i] = start
                            delay = True
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
        
        self.start_list = []
        self.end_list = []
        while len(self.start_list) < self.start_count:
            row = random.randint(0,19)
            col = random.randint(0,19)
            spot = grid[row][col]
            if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_intersection and not spot.is_dragon and not spot.is_wall:
                spot.make_start()
                self.start_list.append(spot)

        while len(self.end_list) < self.end_count:
            row = random.randint(0,19)
            col = random.randint(0,19)
            spot = grid[row][col]
            if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_intersection and not spot.is_dragon and not spot.is_wall:
                spot.make_end()
                self.end_list.append(spot)

        self.path_obj_dict = {}
        run = True
        update_path = False
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        count = COUNT
        delay = False
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if pygame.mouse.get_pressed()[0]: # LEFT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if not spot.is_end and not spot.is_start and not spot.is_wall:
                            barrier_count += 1
                            prev_barrier_count += 1
                            spot.make_barrier()
                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if spot.is_barrier and not spot.is_end and not spot.is_start and not spot.is_wall:
                            barrier_count -= 1
                            spot.reset()
                    if event.type == pygame.KEYDOWN:
                        if self.play_sound:
                            self.click_sound.play()
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            update_path = False
                        if event.key == pygame.K_SPACE and len(self.start_list) == self.start_count and len(self.end_list) == self.end_count:
                            update_path = True
                            delay = True
                if delay:
                    count -=1
            else:
                if update_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    threads = []
                    for i, start in enumerate(self.start_list):
                        if self.path_obj_dict and 'man_%s' %i in self.path_obj_dict:
                            for spot in self.path_obj_dict['man_%s' %i][2]:
                                if not spot.is_barrier:
                                    spot.reset()
                        self.path_obj_dict['man_%s' %i] = [start, self.end_list, False]
                        t = threading.Thread(target=self.solve, args=('man_%s' %i, grid))
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                    update_path = False
                if not self.start_list:
                    run = False
                if self.start_list and self.path_obj_dict:
                    for i, start in enumerate(self.start_list):
                        _path_obj = self.path_obj_dict['man_%s' %i]
                        if not _path_obj[2]:
                            print('Cannot find path')
                            self.start_list.pop(i)
                        else:
                            if not len(_path_obj[2]):
                                start.reset()
                                print('Man %s has reached' %i)
                                self.start_list.pop(i)
                            if len([spot for spot in _path_obj[2] if spot.is_barrier]) > 0 or len([spot for spot in _path_obj[2] if spot.is_dragon]) > 0:
                                update_path = True
                            if barrier_count < prev_barrier_count:
                                prev_barrier_count = barrier_count
                                update_path = True
                            if not update_path and len(_path_obj[2]) > 0:
                                if not _path_obj[2][0].is_start:
                                    if start.is_intersection:
                                        start.reset()
                                        start.make_path()
                                    else:
                                        start.reset()
                                    start = _path_obj[2].pop(0)
                                    start.make_start()
                                    if self.play_sound:
                                        self.footstep_sound.play()
                                    self.start_list[i] = start
                                delay = True
                                count = COUNT

    def dynamic_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        self.obst_1 = []
        self.obst_2 = []
        self.obst_3 = []
        self.obst_4 = []
        for i in range(4):
            self.obst_1.append(grid[4][i])
            grid[4][i].make_wall()
            self.obst_2.append(grid[19-i][4])
            grid[19-i][4].make_wall()
            self.obst_3.append(grid[14][19-i])
            grid[14][19-i].make_wall()
            self.obst_4.append(grid[i][15])
            grid[i][15].make_wall()
            
        self.start_list = []
        self.end_list = []
        reverse_1 = reverse_2 = reverse_3 = reverse_4 = True
        self.path_obj_dict = {}
        run = True
        update_path = False
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        count = COUNT
        delay = False
        delta = 0.5
        add_barrier = False
        dyn_time = datetime.datetime.now() + datetime.timedelta(seconds = delta)
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
                        if event.key == pygame.K_SPACE and len(self.start_list) == self.start_count and len(self.end_list) == self.end_count:
                            dyn_time = datetime.datetime.now() + datetime.timedelta(seconds = delta)
                            add_barrier = True
                            update_path = True
                            delay = True
                    if pygame.mouse.get_pressed()[0]: # LEFT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if not update_path and len(self.start_list) != int(self.start_count) and not spot.is_end and not spot.is_start:
                            spot.make_start()
                            self.start_list.append(spot)
                        elif not update_path and len(self.end_list) != int(self.end_count) and not spot.is_start and not spot.is_end:
                            spot.make_end()
                            self.end_list.append(spot)
                        elif not spot.is_end and not spot.is_start and not spot.is_wall:
                            barrier_count += 1
                            prev_barrier_count += 1
                            spot.make_barrier()
                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if spot.is_barrier:
                            barrier_count -= 1
                        if not update_path: 
                            spot.reset()
                            if spot in self.start_list:
                                self.start_list = [start for start in self.start_list if start != spot]
                            if spot in self.end_list:
                                self.end_list = [end for end in self.end_list if end != spot]
                        else:
                            if spot not in self.start_list and spot not in self.end_list:
                                spot.reset()
                if dyn_time <= datetime.datetime.now():
                    dyn_time = datetime.datetime.now() + datetime.timedelta(seconds = delta)
                    row = random.randint(0,19)
                    col = random.randint(0,19)
                    if not row in [4,15] and not col in [4,15]:
                        spot = grid[row][col]
                        if not spot.is_start and not spot.is_end and not spot.is_barrier and not spot.is_wall:
                            spot.make_barrier()
                    if reverse_1:
                        if self.obst_1[-1].col < 19:
                            nxt = grid[self.obst_1[-1].row][self.obst_1[-1].col+1]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_1 = False
                            else:
                                for i, obs in reversed(list(enumerate(self.obst_1))):
                                    obs.reset()
                                    grid[obs.row][obs.col + 1].make_wall()
                                    self.obst_1[i] = grid[obs.row][obs.col + 1]
                        else:
                            reverse_1 = False
                    else:
                        if self.obst_1[0].col > 0:
                            nxt = grid[self.obst_1[0].row][self.obst_1[0].col-1]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_1= True
                            else:
                                for i, obs in enumerate(self.obst_1):
                                    obs.reset()
                                    grid[obs.row][obs.col - 1].make_wall()
                                    self.obst_1[i] = grid[obs.row][obs.col - 1]
                        else:
                            reverse_1 = True
                    
                    if reverse_3:
                        if self.obst_3[-1].col > 0:
                            nxt = grid[self.obst_3[-1].row][self.obst_3[-1].col-1]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_3 = False
                            else:
                                for i, obs in reversed(list(enumerate(self.obst_3))):
                                    obs.reset()
                                    grid[obs.row][obs.col - 1].make_wall()
                                    self.obst_3[i] = grid[obs.row][obs.col - 1]
                        else:
                            reverse_3 = False
                    else:
                        if self.obst_3[0].col < 19:
                            nxt = grid[self.obst_3[0].row][self.obst_3[0].col+1]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_3 = True
                            else:
                                for i, obs in enumerate(self.obst_3):
                                    obs.reset()
                                    grid[obs.row][obs.col + 1].make_wall()
                                    self.obst_3[i] = grid[obs.row][obs.col + 1]
                        else:
                            reverse_3 = True

                    if reverse_2:
                        if self.obst_2[-1].row > 0:
                            nxt = grid[self.obst_2[-1].row-1][self.obst_2[-1].col]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_2 = False
                            else:
                                for i, obs in reversed(list(enumerate(self.obst_2))):
                                    obs.reset()
                                    grid[obs.row-1][obs.col].make_wall()
                                    self.obst_2[i] = grid[obs.row-1][obs.col]
                        else:
                            reverse_2 = False
                    else:
                        if self.obst_2[0].row < 19:
                            nxt = grid[self.obst_2[-1].row-1][self.obst_2[-1].col]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_2 = True
                            else:
                                for i, obs in enumerate(self.obst_2):
                                    obs.reset()
                                    grid[obs.row+1][obs.col].make_wall()
                                    self.obst_2[i] = grid[obs.row+1][obs.col]
                        else:
                            reverse_2 = True
                    
                    if reverse_4:
                        if self.obst_4[-1].row < 19:
                            nxt = grid[self.obst_4[-1].row+1][self.obst_4[-1].col]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_4 = False
                            else:
                                for i, obs in reversed(list(enumerate(self.obst_4))):
                                    obs.reset()
                                    grid[obs.row+1][obs.col].make_wall()
                                    self.obst_4[i] = grid[obs.row+1][obs.col]
                        else:
                            reverse_4 = False
                    else:
                        if self.obst_4[0].row > 0:
                            nxt = grid[self.obst_4[0].row-1][self.obst_4[0].col]
                            if nxt.is_end or nxt.is_wall or nxt.is_barrier:
                                reverse_4 = True
                            else:
                                for i, obs in enumerate(self.obst_4):
                                    obs.reset()
                                    grid[obs.row-1][obs.col].make_wall()
                                    self.obst_4[i] = grid[obs.row-1][obs.col]
                        else:
                            reverse_4 = True
                if delay:
                    count -=1
            else:
                if update_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    threads = []
                    for i, start in enumerate(self.start_list):
                        if self.path_obj_dict and 'man_%s' %i in self.path_obj_dict:
                            for spot in self.path_obj_dict['man_%s' %i][2]:
                                if not spot.is_barrier:
                                    spot.reset()
                        self.path_obj_dict['man_%s' %i] = [start, self.end_list, False]
                        t = threading.Thread(target=self.solve, args=('man_%s' %i, grid))
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                    update_path = False
                if not self.start_list:
                    run = False
                if self.start_list and self.path_obj_dict:
                    for i, start in enumerate(self.start_list):
                        _path_obj = self.path_obj_dict['man_%s' %i]
                        if not len(_path_obj[2]):
                            start.reset()
                            print('Man %s has reached' %i)
                            self.start_list.pop(i)
                        if len([spot for spot in _path_obj[2] if spot.is_wall]) > 0 or len([spot for spot in _path_obj[2] if spot.is_barrier]) > 0 or len([spot for spot in _path_obj[2] if spot.is_dragon]) > 0:
                            update_path = True
                        if barrier_count < prev_barrier_count:
                            prev_barrier_count = barrier_count
                            update_path = True
                        if not update_path and len(_path_obj[2]) > 0:
                            if not _path_obj[2][0].is_start and not _path_obj[2][0].is_wall:
                                if start.is_intersection:
                                    start.reset()
                                    start.make_path()
                                else:
                                    start.reset()
                                start = _path_obj[2].pop(0)
                                start.make_start()
                                if self.play_sound:
                                    self.footstep_sound.play()
                                self.start_list[i] = start
                            delay = True
                            count = COUNT

    def solve(self, name, grid):
        start = self.path_obj_dict[name][0]
        end_list = self.path_obj_dict[name][1]
        astar_path = self.path_obj_dict[name][2]
        astar_paths = []
        for end in end_list:
            _path = algorithm(grid, end, start)
            astar_paths.append(_path)
        try:
            astar_path = sorted(astar_paths, key=len)[0]
        except Exception as exp:
            astar_path = False
        color_path(astar_path, lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH))
        self.path_obj_dict[name] = [start, end_list, astar_path]

    def custom_maze(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)
        self.start_list = []
        self.end_list = []
        self.path_obj_dict = {}
        run = True
        update_path = False
        barrier_count = prev_barrier_count = get_barrier_count(grid)
        count = COUNT
        delay = False
        while run:
            draw(self.win, grid, TOTAL_ROWS, WIDTH)
            if count > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if pygame.mouse.get_pressed()[0]: # LEFT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if not update_path and len(self.start_list) != int(self.start_count) and not spot.is_end and not spot.is_start:
                            spot.make_start()
                            self.start_list.append(spot)
                        elif not update_path and len(self.end_list) != int(self.end_count) and not spot.is_start and not spot.is_end:
                            spot.make_end()
                            self.end_list.append(spot)
                        elif not spot.is_end and not spot.is_start and not spot.is_wall:
                            barrier_count += 1
                            prev_barrier_count += 1
                            spot.make_barrier()
                    elif pygame.mouse.get_pressed()[2]: # RIGHT
                        if self.play_sound:
                            self.click_sound.play()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, TOTAL_ROWS, WIDTH)
                        spot = grid[row][col]
                        if spot.is_barrier:
                            barrier_count -= 1
                        if not update_path: 
                            spot.reset()
                            if spot in self.start_list:
                                self.start_list = [start for start in self.start_list if start != spot]
                            if spot in self.end_list:
                                self.end_list = [end for end in self.end_list if end != spot]
                        else:
                            if spot not in self.start_list and spot not in self.end_list:
                                spot.reset()
                    if event.type == pygame.KEYDOWN:
                        if self.play_sound:
                            self.click_sound.play()
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            update_path = False
                        if event.key == pygame.K_SPACE and len(self.start_list) == self.start_count and len(self.end_list) == self.end_count:
                            update_path = True
                            delay = True
                        if event.key == pygame.K_c:
                            self.start_list = []
                            end = None
                            grid = make_grid(TOTAL_ROWS, WIDTH)
                if delay:
                    count -=1
            else:
                if update_path:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    threads = []
                    for i, start in enumerate(self.start_list):
                        if self.path_obj_dict and 'man_%s' %i in self.path_obj_dict:
                            for spot in self.path_obj_dict['man_%s' %i][2]:
                                if not spot.is_barrier:
                                    spot.reset()
                        self.path_obj_dict['man_%s' %i] = [start, self.end_list, False]
                        t = threading.Thread(target=self.solve, args=('man_%s' %i, grid))
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                    update_path = False
                if not self.start_list:
                    run = False
                if self.start_list and self.path_obj_dict:
                    for i, start in enumerate(self.start_list):
                        _path_obj = self.path_obj_dict['man_%s' %i]
                        if not _path_obj[2]:
                            print('Cannot find path')
                            self.start_list.pop(i)
                        else:
                            if not len(_path_obj[2]):
                                start.reset()
                                print('Man %s has reached' %i)
                                self.start_list.pop(i)
                            if len([spot for spot in _path_obj[2] if spot.is_barrier]) > 0 or len([spot for spot in _path_obj[2] if spot.is_dragon]) > 0:
                                update_path = True
                            if barrier_count < prev_barrier_count:
                                prev_barrier_count = barrier_count
                                update_path = True
                            if not update_path and len(_path_obj[2]) > 0:
                                if not _path_obj[2][0].is_start:
                                    if start.is_intersection:
                                        start.reset()
                                        start.make_path()
                                    else:
                                        start.reset()
                                    start = _path_obj[2].pop(0)
                                    start.make_start()
                                    if self.play_sound:
                                        self.footstep_sound.play()
                                    self.start_list[i] = start
                                delay = True
                                count = COUNT

if __name__ == '__main__':
    test_obj = Agneepath()
    test_obj.main()