from snake_game import SnakeGame
import pygame
import random

rand = random.Random()


class Color:
    GREEN_BODY = (113, 207, 90)
    GREEN_HEAD = (0, 255, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


class SnakeGameGUI(SnakeGame):
    
    def __init__(self):
        super().__init__()
        self.BODY_ELEM_SIZE = 25
        self.WIDTH = self.BODY_ELEM_SIZE * self.width
        self.HEIGHT = self.BODY_ELEM_SIZE * self.height
        self.TABLE_SIZE = (self.WIDTH + 400, self.HEIGHT)
        self.SCREEN = pygame.display.set_mode(self.TABLE_SIZE, )
        pygame.init()

    def draw_board(self):
        font = pygame.font.SysFont("monospace", 30)
        self.SCREEN.fill(Color.WHITE)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == 1:
                    loc_size = (j * self.BODY_ELEM_SIZE, i * self.BODY_ELEM_SIZE, self.BODY_ELEM_SIZE, self.BODY_ELEM_SIZE)
                    pygame.draw.rect(self.SCREEN, Color.GREEN_BODY, loc_size)
                elif self.board[i, j] == 2:
                    loc_size = (j * self.BODY_ELEM_SIZE, i * self.BODY_ELEM_SIZE, self.BODY_ELEM_SIZE, self.BODY_ELEM_SIZE)
                    pygame.draw.rect(self.SCREEN, Color.GREEN_HEAD, loc_size)
                elif self.board[i, j] == -1:
                    loc = (int((j+0.5) * self.BODY_ELEM_SIZE), int((i + 0.5) * self.BODY_ELEM_SIZE))
                    pygame.draw.circle(self.SCREEN, Color.RED, loc, self.BODY_ELEM_SIZE // 2)
        
        label = font.render(f"Score: {self.score}", True, Color.GREEN_HEAD)
        self.SCREEN.blit(label, (self.WIDTH + 10, 10))
        loc_size = (self.WIDTH, 0, 3, self.HEIGHT)
        pygame.draw.rect(self.SCREEN, (0, 0, 0), loc_size)
        pygame.display.update()
