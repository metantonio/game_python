import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self):

        # get the thisplay surface
        self.display_surface = pygame.display.get_surface()

        #sprites group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group() #will help for collisions

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()    

        # user interface
        self.ui = UI()

         
    def create_map(self):
        #creation of map using default map on settings
        """ for row_index, row in enumerate(WORLD_MAP):
            #print(row_index, row)
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'X':
                    Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites], self.obstacles_sprites) """
        
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
        }
        graphics = {
            'grass':import_folder('../graphics/Grass'),
            'objects':import_folder('../graphics/objects')
        }

        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout): #load the layout and not WORLD_MAP
            #print(row_index, row)
                for col_index, col in enumerate(row):
                    if col != '-1': #on .csv file -1 should not be walkable
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            #Tile((x,y),[self.visible_sprites, self.obstacles_sprites], 'invisible') #this makes visible boundaries
                            Tile((x,y),[self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            #create grass randomly from the files, should be visible and collisionable
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                            
                        if style == 'object':
                            # create object, cannot be random
                            surf = graphics['objects'][int(col)] #images has id, i want use the id but is a string
                            Tile((x,y),[self.visible_sprites, self.obstacles_sprites], 'object', surf)

                
        self.player = Player((2000,1430),[self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    
    def run(self):
        # Update and draw the game
        #self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player) #now the draw and camera are separated
        self.visible_sprites.update()
        #debug(self.player.direction) # See direction on coordinates
        self.ui.display(self.player) #get information of the player in the UI

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
            
