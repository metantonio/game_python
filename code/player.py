from typing import Any
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() #[x:0, y:0]
        self.speed = 5


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #normalize the direction to 1
    	
        # THIS HAS TO CHANGE TO HAVE SAME SPEED ON PLAYERS AND ENEMIES
        self.rect.center += self.direction*speed ## We need to normalize direction to reduce speed on diagonal directions (trigonometry)

    def update(self):
        self.input()
        self.move(self.speed)
