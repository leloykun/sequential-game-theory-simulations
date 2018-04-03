import os
import time
import random
import copy
import multiprocessing as mp

import numpy as np

from .world import World
from .qlearn import QLearn
from .cell import CasualCell
from .environment import Environment


class Agent:
    def __setattr__(self, key, val):
        if key == 'cell':
            # transfer the agent:
            # old -> val
            old = self.__dict__.get(key, None)
            if old is not None:
                old.agents.remove(self)
            if val is not None:
                val.agents.append(self)
        self.__dict__[key] = val

    """ unnecessary codes
    def __getattr__(self, key):
        if key == 'leftCell':
            return self.get_cell_on_left()
        elif key == 'rightCell':
            return self.get_cell_on_right()
        elif key == 'aheadCell':
            return self.get_cell_ahead()
        raise AttributeError(key)

    def turn(self, amount):
        self.dir = (self.dir + amount) % self.world.num_dir

    def turn_left(self):
        self.turn(-1)

    def turn_right(self):
        self.turn(1)

    def turn_around(self):
        self.turn(self.world.num_dir / 2)

    def go_forward(self):
        self.go_in_direction(self.dir)

    def go_backward(self):
        self.turn_around()
        self.go_forward()
        self.turn_around()

    def get_cell_ahead(self):
        return self.cell.neighbour[self.dir]

    def get_cell_on_left(self):
        return self.cell.neighbour[(self.dir - 1) % self.world.num_dir]

    def get_cell_on_right(self):
        return self.cell.neighbour[(self.dir + 1) % self.world.num_dir]"""

    # return True if successfully moved in that direction
    def go_in_direction(self, dir):
        target = self.cell.neighbour[dir]
        if getattr(target, 'wall', False):
            # print "hit a wall"
            return False
        self.cell = target
        return True

    def go_towards(self, target):
        if self.cell == target:
            return
        best = None
        bestDist = None
        for n in self.cell.neighbours:
            if n == target:
                best = target
                break
            dist = (n.x - target.x)**2 + (n.y - target.y)**2
            if best is None or bestDist > dist:
                best = n
                bestDist = dist
        if best is not None:
            if getattr(best, 'wall', False):
                return
            self.cell = best


class DumbPrey(Agent):
    colour = 'yellow'

    def update(self):
        if self.move:
            cell = self.cell
            while cell == self.cell:
                self.go_in_direction(random.randrange(self.world.num_dir))


class WolfpackMouse(Agent):
    colour = (41, 113, 177)
    mark = False

    def update(self):
        if self.move:
            cell = self.cell
            while cell == self.cell:
                self.go_in_direction(random.randrange(self.world.num_dir))

        if self.mark:
            self.mark = False
            self.cell = self.env.get_random_avail_cell()


class WolfpackCat(Agent):
    colour = (185, 39, 50)
    visual_depth = 6
    capture_radius = 4
    reward_per_cat = 100
    lookcells = []
    idx = -1;

    def __init__(self):
        self.ai = QLearn(actions=list(range(8)))
        self.learning = True
        self.ai.agent = self

        self.eaten = 0
        self.fed = 0

        self.total_rewards = 0

        self.last_action = None
        self.last_state = None

        self.calc_lookcells()

    def calc_lookcells(self):
        self.lookcells = []
        for i in range(-self.visual_depth, self.visual_depth + 1):
            for j in range(-self.visual_depth, self.visual_depth + 1):
                self.lookcells.append((i, j))

    def calc_reward(self):
        reward = 0
        if self.world.can_cat_capture[0]:
            reward += self.reward_per_cat
        if self.world.can_cat_capture[1]:
            reward += self.reward_per_cat
        return reward

    def update(self):
        state = self.calc_state()
        reward = -1

        if self.world.can_cat_capture[self.idx]:
            self.world.fed += 1
            reward = self.calc_reward()
            self.world.mouse.mark = True
            # self.world.mouse.cell = self.env.get_random_avail_cell()

        self.total_rewards += reward

        if self.last_state is not None and self.learning:
            self.ai.learn(self.last_state,
                          self.last_action,
                          reward,
                          state)

        state = self.calc_state()

        action = self.ai.choose_action(state)
        self.last_state = state
        self.last_action = action

        self.go_in_direction(action)

    def can_capture_mouse(self):
        return self.dist_to_mouse() <= self.capture_radius

    def dist_to_mouse(self):
        mouse = self.world.mouse
        return abs(self.cell.x - mouse.cell.x) + abs(self.cell.y - mouse.cell.y)

    # TODO: consider wrapping here
    def calc_state(self):
        cats = self.world.cats
        mouse = self.world.mouse

        def cell_value(cell):
            if cats[0].cell is not None and (cell.x == cats[0].cell.x and
                                             cell.y == cats[0].cell.y):
                return 4
            elif cats[1].cell is not None and (cell.x == cats[1].cell.x and
                                               cell.y == cats[1].cell.y):
                return 3
            elif mouse.cell is not None and (cell.x == mouse.cell.x and
                                             cell.y == mouse.cell.y):
                return 2
            elif cell.wall:
                return 1
            else:
                return 0

        return tuple([
            cell_value(self.world.get_wrapped_cell(self.cell.x + j,
                                                   self.cell.y + i))
            for i, j in self.lookcells
        ])

    def going_to_obstacle(self, action):
        cell = self.world.get_point_in_direction(self.cell.x,
                                                 self.cell.y,
                                                 action)
        return self.world.get_cell(cell[0], cell[1]).wall

    def get_data(self):
        pass
