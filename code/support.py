#File to define support functions to work with other files, or actions that do not belong to the game
from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as content_bin:
        #print(level_map)
        layout = reader(content_bin, delimiter=',')
        #print(layout)
        
        for row in layout:
        #    print(row)
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    """return all relatives path of all files from a folder, then loads the images.
    Note: Need pygame.display initiated to work, so it wont work directly with this file, 
    but will work from another already initiated    
    """
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            #print(image)
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
