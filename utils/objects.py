import pygame as py

from dataclasses import dataclass

class EntityManager:
    def __init__(self):
        self._next_id = 0

    def get_next_eid(self):
        eid = self._next_id
        self._next_id += 1
        return eid

# Statistics of entities
@dataclass
class Health:
    """ health is not a percentage and the max value scales with weight """
    health: float = 100
    max_health: float = 100

@dataclass
class Combat:
    attack: float = 10
    defence: float = 5

@dataclass
class Dimensions:
    weight: float = 1
    height: float = 1
    length: float = 1
    width: float = 1

    """ changes as weight changes """
    growth_rate: float = 1

@dataclass
class Needs:
    """ hunger and thirst are percentages """
    hunger: float = 0
    max_hunger: float = 100 
    thirst: float = 0
    max_thirst: float = 100

    """ the rates are modified as growth happens """
    hunger_rate: float = 1
    thirst_rate: float = 1

@dataclass
class Senses:
    sight_range: float = 10
    sight_angle: float = 90
    hearing_range: float = 10

@dataclass
class Movement:
    pos_x: float = 0
    pos_y: float = 0

    vel_x: float = 0
    vel_y: float = 0

    acceleration: float = 1

    angle: float = 0
    angle_acc: float = 1

    ms_land: float = 5
    ms_water: float = 2


class World:
    def __init__(self):
        self.entities = set()

        self.health = {}
        self.combat = {}
        self.dimensions = {}
        self.needs = {}
        self.senses = {}
        self.movement = {}

    def add_entity(self, eid):
        self.entities.add(eid)

    def remove_entity(self, eid):
        self.entities.discard(eid)

        for comp in [self.health, self.combat, self.dimensions, self.needs, self.senses, self.movement]:
            comp.pop(eid, None)

    def print_info(self):
        print("-- Entities --")
        print(self.health)
        print(self.combat)
        print(self.dimensions)
        print(self.needs)
        print(self.senses)
        print(self.movement)

def update_health(world: World):
    for eid, needs in world.needs.items():
        health = world.health.get(eid)

        if not health:
            continue

        # starvation damage
        if needs.hunger > 80:
            health.value -= 0.1

        if health.value <= 0:
            world.remove_entity(eid)

def update_needs(world: World):
    for eid, needs in world.needs.items():
        needs.hunger += needs.hunger_rate * 0.1
        needs.thirst += needs.thirst_rate * 0.1

def update_movement(world: World):
    for eid, mov in world.movement.items():
        mov.vx *= 0.95
        mov.vy *= 0.95

def update_display(world: World, screen, grid_cell_size):
    for eid, mov in world.movement.items():
        py.draw.circle(screen, (255, 255, 255), (mov.pos_x * grid_cell_size - int(grid_cell_size / 2), mov.pos_y * grid_cell_size - int(grid_cell_size / 2)), 20)

def create_prey(world: World, eid):
    world.add_entity(eid)

    world.health[eid] = Health(100, 100)
    world.combat[eid] = Combat(attack=2, defence=1)
    world.dimensions[eid] = Dimensions(weight=10)
    world.needs[eid] = Needs(hunger_rate=1.5, thirst_rate=1.0)
    world.senses[eid] = Senses(sight_range=15)
    world.movement[eid] = Movement(ms_land=6, ms_water=2)

def create_plant(world: World, eid, pos_x, pos_y):
    world.add_entity(eid)

    world.health[eid] = Health(100, 100)
    world.dimensions[eid] = Dimensions(weight=10)
    world.movement[eid] = Movement(pos_x=pos_x, pos_y=pos_y)