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
        self.visible_sprites = YSortCameraGroup()
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
                    self.player = Player((x,y),[self.visible_sprites], self.obstacles_sprites)
                


    def run(self):
        # Update and draw the game
        #self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw() #now the draw and camera are separated
        self.visible_sprites.update()
        #debug(self.player.direction) # See direction on coordinates

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
            
