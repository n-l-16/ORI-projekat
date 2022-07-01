from snake_game import SnakeGame
import pygame
import time
import random

rand = random.Random()
class Color:
    GREEN_BODY = (113, 207, 90)
    GREEN_HEAD = (0, 255, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

class SnakeGameGUI(SnakeGame):
    
    def __init__(self, headless_mode = False):
        super().__init__()
        self.visualization_active = True
        self.GREEN_BODY = (113, 207, 90)
        self.GREEN_HEAD = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.SQUARESIZE = 25
        self.WIDTH = self.SQUARESIZE*self.width
        self.HEIGHT = self.SQUARESIZE*self.height
        self.SIZE = (self.WIDTH + 400, self.HEIGHT)

        if headless_mode == False:
            self.SCREEN = pygame.display.set_mode(self.SIZE)
            pygame.init()

    def draw_board(self):
        myfont = pygame.font.SysFont("monospace", 30)
        self.SCREEN.fill(self.WHITE)
        for i in range(self.height):
            for j in range(self.width):
                # check for head, body, food
                if self.board[i, j] == 1:
                    loc_size = (j*self.SQUARESIZE, i*self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                    pygame.draw.rect(self.SCREEN, self.GREEN_BODY, loc_size)
                elif self.board[i, j] == 2:
                    loc_size = (j*self.SQUARESIZE, i*self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                    pygame.draw.rect(self.SCREEN, self.GREEN_HEAD, loc_size)
                elif self.board[i, j] == -1:
                    loc = (int((j+0.5)*self.SQUARESIZE), int((i+0.5)*self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.RED, loc, self.SQUARESIZE//2)
        
        label = myfont.render(f"Score: {self.score}", 1, self.GREEN_HEAD)
        self.SCREEN.blit(label, (self.WIDTH + 10,10))
        loc_size = (self.WIDTH, 0, 3, self.HEIGHT)
        pygame.draw.rect(self.SCREEN, (0, 0, 0), loc_size)
        pygame.display.update()

