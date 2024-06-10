import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):

        # get the thisplay surface
        self.display_surface = pygame.display.get_surface()

        #sprites group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group() #will help for collisions

        # sprite setup
        self.create_map()

         
    def create_map(self): 
        for row_index, row in enumerate(WORLD_MAP):
            #print(row_index, row)
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'X':
                    Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites])
                


    def run(self):
        # Update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        #debug(self.player.direction) # See direction on coordinates