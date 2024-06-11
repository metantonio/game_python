import pygame
from settings import *

class UI:
    def __init__(self):

        #general information
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT) #needs left, top, width, height
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        #drag the bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

    def display(self, player):
        #pygame.draw.rect(self.display_surface, 'black', self.health_bar_rect) #needs surface, color, rectangle
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
