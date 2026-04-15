import json

scale = 2

width = 16 * scale
height = 9 * scale

map_data = [(width, height)]

for i in range(height):
    for j in range(width):

        if j == 25 or j == 26 or j == 27 or j == 28:
            map_data.append({"type": "water", "colour": (25, 25, 128)})

        elif j == 24 and (i == 0 or i == 1 or i == 2 or i == 3):
            map_data.append({"type": "water", "colour": (25, 25, 128)})
        
        elif j == 29 and (i == 12 or i == 13 or i == 14 or i == 15 or i == 16 or i == 17):
            map_data.append({"type": "water", "colour": (25, 25, 128)})

        else:
            map_data.append({"type": "soil", "colour": (150, 75, 0)})

with open("map.json", "w") as file:
    json.dump(map_data, file)