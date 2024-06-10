import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        #self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha() #testing porpouse
        self.image = surface

        #there are large object (bigger than 64x64) that are 64x128 or 128x128, we want use the left-center and not left-top as (0,0)
        if sprite_type == 'object':
            #do an offset
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
        else:
            self.sprite_type = sprite_type #to determine if is an enemy, grass, etc...
        self.rect = self.image.get_rect(topleft = pos) #rectangle full size of image
        self.hitbox = self.rect.inflate(0, -10) #change the sizer of the rectangle for the sprite, hit box is reduced or aumented, 0 on x, -5 on top and -5 on bottom
