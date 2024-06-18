import pygame
from settings import *

class MagicPlayer:
    def __init(self, animation_player):
        self.animation_player = animation_player

        def heal(self, player, strength, cost, groups):
            if player.energy >= cost:
                player.health += strength
                player.energy -= cost
                # dont heal more than max health bar:
                if player.health >= player.stats['health']:
                    player.health = player.stats['health']

        def flame(self):
            pass