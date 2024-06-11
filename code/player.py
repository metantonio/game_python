from typing import Any
import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26) #check collision on hitbox to hide a part of the character

        # Graphic Setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        #movement
        self.direction = pygame.math.Vector2() #[x:0, y:0]
        self.speed = 5
        self.attacking = False #to avoid you can attack physical and magic at the same time
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack

        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.weapon_index = 0 
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        #print(self.weapon)
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy':60, 'attack':10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']



    def import_player_assets(self):
        character_path = '../graphics/player/' 
        self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)		    
        #print(self.animations)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            #movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #it's a mark time, will run only one time
                print('attack') #will trigger several times if is not regulate
                self.create_attack()

            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #it's a mark time, will run only one time
                print('attack makgic')

            if keys[pygame.K_q] and self.can_switch_weapon: #needs a timer different from attacks timer
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < list(weapon_data.keys()) - 1:
                    self.weapon_index +=1
                else:
                    self.weapon_index =0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        #idle status
        if self.direction.x ==0 and self.direction.y==0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')


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


    def cooldowns(self):
        #cooldowns of attacking
        current_time = pygame.time.get_ticks() #it's a mark time, will run continuesly

        if self.attacking: #creating a timer
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack() #destroy the weapon visually

        if not self.can_switch_weapon: #creating a timer
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
                #self.destroy_attack() #destroy the weapon visually


    def animate(self):
        animation = self.animations[self.status]
        
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) #update the rectangle of image with the center


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
