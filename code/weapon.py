import pygame

""" One problem is that Weapon should be on Level, but the attack is on Player class. Pass Weapon to Level, and from Level to Player """

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)

        self.sprite_type = 'weapon'
        #weapon should face the same direction that the player
        direction = player.status.split('_')[0]

        #graphic
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
        #self.image = pygame.Surface((40,40))
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement of the weapon
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16)) #The center right border of the player will be the center left border of the weapon when facing to the right direction, with a little offset of 16px to visual
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(center= player.rect.center)

