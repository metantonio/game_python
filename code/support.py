#File to define support functions to work with other files, or actions that do not belong to the game
from csv import reader

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