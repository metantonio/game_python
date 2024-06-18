import pygame
from settings import *


class Upgrade:
    def __init__(self, player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(player.max_stats.values())

        # Item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // (self.attribute_nr + 1)
        self.create_items()

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for index, item in enumerate(range(self.attribute_nr)):
            # horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            # vertical position
            top = 0.10 * self.display_surface.get_size()[1]

            # create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        # self.display_surface.fill('black')
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # get attrib
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(
                self.display_surface, self.selection_index, name, value, max_value, cost
            )


class Item:
    def __init__(self, left, top, w, h, index, font):
        self.rect = pygame.Rect(left, top, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        #title
        title_surf = self.font.render(name, False, TEXT_COLOR) #creation
        title_rect = title_surf.get_rect(midtop = self.rect.midtop+pygame.math.Vector2(0,20)) #rectangle where text gonna be

        #cost

        #draw
        surface.blit(title_surf, title_rect)


    def display(self, surface, selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface, name, cost, False)