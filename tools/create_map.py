import json

scale = 2

width = 16 * scale
height = 9 * scale

map_data = [(width, height)]

# Colours
BLUE = (6, 63, 120)
BROWN = (107, 63, 6)

for i in range(height):
    for j in range(width):

        if j == 25 or j == 26 or j == 27 or j == 28:
            map_data.append({"type": "water", "colour": BLUE})

        elif j == 24 and (i == 0 or i == 1 or i == 2 or i == 3):
            map_data.append({"type": "water", "colour": BLUE})
        
        elif j == 29 and (i == 12 or i == 13 or i == 14 or i == 15 or i == 16 or i == 17):
            map_data.append({"type": "water", "colour": BLUE})

        else:
            map_data.append({"type": "soil", "colour": BROWN})

with open("map.json", "w") as file:
    json.dump(map_data, file)