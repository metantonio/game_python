import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        #self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha() #testing porpouse
        self.image = surface
        self.sprite_type = sprite_type #to determine if is an enemy, grass, etc...
        self.rect = self.image.get_rect(topleft = pos) #rectangle full size of image
        self.hitbox = self.rect.inflate(0, -10) #change the sizer of the rectangle for the sprite, hit box is reduced or aumented, 0 on x, -5 on top and -5 on bottom
