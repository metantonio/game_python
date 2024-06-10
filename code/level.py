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
        self.visible_sprites.custom_draw(self.player) #now the draw and camera are separated
        self.visible_sprites.update()
        #debug(self.player.direction) # See direction on coordinates

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #offset vector where camera gonna be, i'll give the center
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor (image below the sprites)
        self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))


    def custom_draw(self, player):
        # getting the offset to move the camera with the player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor (should be before drawing the sprites)
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #for sprite in self.sprites():
        #now we sort wich sprite is drawn first, like the map, and player after
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
