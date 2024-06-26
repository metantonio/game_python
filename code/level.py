import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):

        # get the thisplay surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprites group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()  # will help for collisions

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() #group for weapons sprite attack
        self.attackable_sprites = pygame.sprite.Group() #group for enemies tha can be attacked to check collision

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        # creation of map using default map on settings
        """for row_index, row in enumerate(WORLD_MAP):
        #print(row_index, row)
        for col_index, col in enumerate(row):
            x = col_index * TILESIZE
            y = row_index * TILESIZE
            if col == 'X':
                Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
            if col == 'p':
                self.player = Player((x,y),[self.visible_sprites], self.obstacles_sprites)
        """

        layouts = {
            "boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("../map/map_Grass.csv"),
            "object": import_csv_layout("../map/map_Objects.csv"),
            "entities": import_csv_layout("../map/map_Entities.csv"),
        }
        graphics = {
            "grass": import_folder("../graphics/Grass"),
            "objects": import_folder("../graphics/objects"),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(
                layout
            ):  # load the layout and not WORLD_MAP
                # print(row_index, row)
                for col_index, col in enumerate(row):
                    if col != "-1":  # on .csv file -1 should not be walkable
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == "boundary":
                            # Tile((x,y),[self.visible_sprites, self.obstacles_sprites], 'invisible') #this makes visible boundaries
                            Tile((x, y), [self.obstacles_sprites], "invisible")
                        if style == "grass":
                            # create grass randomly from the files, should be visible and collisionable
                            random_grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                "grass",
                                random_grass_image,
                            )

                        if style == "object":
                            # create object, cannot be random
                            surf = graphics["objects"][
                                int(col)
                            ]  # images has id, i want use the id but is a string
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites],
                                "object",
                                surf,
                            )

                        if style == "entities":
                            if col == "394":  # player is defined with id 394 from Tiles
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )

                            else:
                                monster_name = ''
                                if col == "390":
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                else:
                                    monster_name = "squid"
                                Enemy(
                                    monster_name, 
                                    (x, y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacles_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        print(style, strength, cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        #attack sprites and collision depending of weapon
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                #Check collision between sprites
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False) #sprite, group, DOKILL -> return a list
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            # logic for particles
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target_sprite.kill() #destroy every sprite just to test
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type) #want to know how the player attacked                    

    def damage_player(self, amount, attack_type):
        # function that will hurt the player
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            # spawn some particles, need attack_type, position and groups
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        # Block of thing that always gonna be displayed
        # Update and draw the game
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(
            self.player
        )
        self.ui.display(self.player)  # get information of the player in the UI

        #Display only is game is paused or not paused
        if self.game_paused:
            self.upgrade.display()
            #display menu

        else:
            # now the draw and camera are separated
            self.visible_sprites.update()
            #run the game
            # debug(self.player.direction) # See direction on coordinates
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
        
        
        
        


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # offset vector where camera gonna be, i'll give the center
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor (image below the sprites)
        self.floor_surface = pygame.image.load(
            "../graphics/tilemap/ground.png"
        ).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset to move the camera with the player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor (should be before drawing the sprites)
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        # now we sort wich sprite is drawn first, like the map, and player after
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)