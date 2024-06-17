import pygame
from math import sin

#here we gonna use the colission system for players and enemies
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #normalize the direction to 1
    	
        # THIS HAS TO CHANGE TO HAVE SAME SPEED ON PLAYERS AND ENEMIES
        #self.rect.center += self.direction*speed ## We need to normalize direction to reduce speed on diagonal directions (trigonometry)
        #self.rect.x += self.direction.x * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        #self.rect.y += self.direction.y * speed
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #moving Left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        # sin() wave to flicker the monsters
        value = sin(pygame.time.get_ticks())
        if value >= 0 : return 255
        else: return 0