import pygame, sys
from settings import *
from debug import debug

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock() #Delta time to gran same spee on any machine

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            debug('Hello') #comment this line on production
            pygame.display.update()
            self.clock.tick(FPS) #controlling the FPS with the delta time

if __name__ == '__main__':
    game = Game()
    game.run()