import pygame, sys
from settings import *
from level import Level
#from debug import debug

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('My Game') #Title of the game
        self.clock = pygame.time.Clock() #Delta time to gran same spee on any machine

        self.level = Level() #Load level class  to the game class

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # In case any button is pressed
                if event.type == pygame.KEYDOWN:
                    # if is the M button
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            
            self.screen.fill('black')
            #debug('Hello') #comment this line on production
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS) #controlling the FPS with the delta time

if __name__ == '__main__':
    game = Game()
    game.run()