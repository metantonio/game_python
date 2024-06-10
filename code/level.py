import pygame

class Level:
    def __init__(self):

        # get the thisplay surface
        self.display_surface = pygame.display.get_surface()

        #sprites group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

    def run(self):
        #Comment for now
        pass
