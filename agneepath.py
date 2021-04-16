import time
from lib.grid import Spot
from lib.operations import *
from lib.constants import *

class Agneepath:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Agneepath Incremental Pathfinding Algorithm")
        
    def main(self):
        grid = make_grid(TOTAL_ROWS, WIDTH)

        start = None
        end = None

        run = True
        while run:    
            draw(self.win, grid, TOTAL_ROWS, WIDTH)

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
                    if event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        astar_path = algorithm(lambda: draw(self.win, grid, TOTAL_ROWS, WIDTH), grid, end, start)
                        while start in astar_path:
                            start.reset()
                            time.sleep(0.5)
                            start = astar_path[start]
                            start.make_start()
                            draw(self.win, grid, TOTAL_ROWS, WIDTH)
                            
                        if start is end:
                            start.make_end()
                            print("Reached destination")
                        
                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(TOTAL_ROWS, WIDTH)
        pygame.quit()

if __name__ == '__main__':
    test_obj = Agneepath()
    test_obj.main()