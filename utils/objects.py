import pygame as py
import numpy as np

from dataclasses import dataclass
from utils.functions import calc_grid_pos

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

    ms_land: float = 1
    ms_water: float = 0.2

@dataclass
class Appearance:
    colour: tuple = (255, 255, 255)
    shape: str = "circle"


class World:
    def __init__(self):
        self.entities = set()

        self.health = {}
        self.combat = {}
        self.dimensions = {}
        self.needs = {}
        self.senses = {}
        self.movement = {}
        self.appearance = {}

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

        # calculate how to scale the velocity to be at the land movespeed
        rms = np.sqrt(mov.vel_x**2 + mov.vel_y**2)
        if rms != 0:
            scale_fac = mov.ms_land / rms
        else:
            scale_fac = 1

        mov.pos_x += mov.vel_x * 0.1 * scale_fac
        mov.pos_y += mov.vel_y * 0.1 * scale_fac

def update_display(world: World, screen, grid_cell_size):
    for eid, app in world.appearance.items():
        mov = world.movement[eid]

        x = calc_grid_pos(mov.pos_x, grid_cell_size)
        y = calc_grid_pos(mov.pos_y, grid_cell_size)

        if app.shape == "circle":
            r = int(grid_cell_size / 2) - 1
            py.draw.circle(screen, app.colour, (x - int(grid_cell_size / 2), y - int(grid_cell_size / 2)), r)

        if app.shape == "square":
            rect = py.Rect(
                x + 1,
                y + 1,
                grid_cell_size - 2,
                grid_cell_size - 2
            )
            py.draw.rect(screen, app.colour, rect, 0)

def create_prey(world: World, eid, pos_x, pos_y):
    world.add_entity(eid)

    world.health[eid] = Health(100, 100)
    world.combat[eid] = Combat(attack=2, defence=1)
    world.dimensions[eid] = Dimensions(weight=10)
    world.needs[eid] = Needs(hunger_rate=1.5, thirst_rate=1.0)
    world.senses[eid] = Senses(sight_range=15)
    world.movement[eid] = Movement(pos_x=pos_x, pos_y=pos_y, vel_x=1, vel_y=1)
    world.appearance[eid] = Appearance(colour=(143, 104, 43), shape="square")

def create_plant(world: World, eid, pos_x, pos_y):
    world.add_entity(eid)

    world.health[eid] = Health(100, 100)
    world.dimensions[eid] = Dimensions(weight=10)
    world.movement[eid] = Movement(pos_x=pos_x, pos_y=pos_y)
    world.appearance[eid] = Appearance((5, 130, 20))