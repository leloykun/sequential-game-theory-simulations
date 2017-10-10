import sys
import time
import math
import random
import multiprocessing as mp

from ..utils import ord, process

from ...agent import Agent
from ...world import World
from ...qlearn import QLearn
from ...cell import CasualCell
from ...agent import Prey as Cheese
from ...environment import Environment

sim_name = 'migration'
output_dir = 'sims/' + sim_name + '/data/'

test = False
max_visual_depth = 4


class Mouse(Agent):
    colour = 'gray'
    visual_depth = 3
    lookcells = []

    def __init__(self):
        self.ai = QLearn(actions=list(range(8)))
        self.ai.agent = self

        self.eaten = 0
        self.fed = 0

        self.last_action = None
        self.last_state = None

        self.calc_lookcells()

    def calc_lookcells(self):
        self.lookcells = []
        for i in range(-self.visual_depth, self.visual_depth + 1):
            for j in range(-self.visual_depth, self.visual_depth + 1):
                self.lookcells.append((i, j))

    def update(self):
        state = self.calc_state()
        reward = -1

        if self.cell == self.world.cat.cell:
            self.eaten += 1
            reward = -100
            if self.last_state is not None:
                self.ai.learn(self.last_state,
                              self.last_action,
                              reward,
                              state)

            self.last_state = None
            self.cell = self.env.get_random_avail_cell()
            return

        if self.cell == self.world.cheese.cell:
            self.fed += 1
            reward = 50
            self.world.cheese.cell = self.env.get_random_avail_cell()

        if self.last_state is not None:
            self.ai.learn(self.last_state,
                          self.last_action,
                          reward,
                          state)

        state = self.calc_state()
        action = self.ai.choose_action(state)

        self.last_state = state
        self.last_action = action

        self.go_in_direction(action)

    def calc_state(self):
        def cell_value(cell):
            if cat.cell is not None and (cell.x == cat.cell.x and
                                         cell.y == cat.cell.y):
                return 3
            elif cheese.cell is not None and (cell.x == cheese.cell.x and
                                              cell.y == cheese.cell.y):
                return 2
            elif cell.wall:
                return 1
            else:
                return 0

        cat = self.world.cat
        cheese = self.world.cheese

        return tuple([
            cell_value(self.world.get_wrapped_cell(self.cell.x + j, 
                                                   self.cell.y +i))
            for i, j in self.lookcells
        ])

    def going_to_obstacle(self, action):
        cell = self.world.get_point_in_direction(self.cell.x,
                                                 self.cell.y,
                                                 action)
        cell = self.world.get_cell(cell[0], cell[1])
        return cell.wall or (cell.num_agents() > 0 and
                             self.world.cheese not in cell.agents)


class Cat(Agent):
    colour = 'red'

    def update(self):
        cell = self.cell
        mouse = self.get_nearest_mouse()
        if cell != mouse.cell:
            self.go_towards(mouse.cell)
            while cell == self.cell:
                self.go_in_direction(random.randrange(self.world.num_dir))

    def get_nearest_mouse(self):
        mouse_so_far = None
        for mouse in self.world.mice:
            if mouse_so_far is None or self.is_nearer(mouse, mouse_so_far):
                mouse_so_far = mouse
        return mouse_so_far

    def is_nearer(self, mouse1, mouse2):
        dx1 = self.cell.x - mouse1.cell.x
        dy1 = self.cell.y - mouse1.cell.y
        dist1 = dx1**2 + dy1**2
        # dist1 = math.sqrt(dist1)
        dx2 = self.cell.x - mouse2.cell.x
        dy2 = self.cell.y - mouse2.cell.y
        dist2 = dx2**2 + dy2**2
        # dist2 = math.sqrt(dist2)
        return dist1 < dist2


def worker(params):
    timesteps, num_mice = params

    env = Environment(world=World(map='worlds/box15x15.txt',
                                  Cell=CasualCell))

    env.world.mice = []
    for i in range(num_mice):
        mouse = Mouse()
        env.add_agent(mouse)
        env.world.mice.append(mouse)

    cat = Cat()
    env.add_agent(cat)
    env.world.cat = cat

    cheese = Cheese()
    env.add_agent(cheese)
    cheese.move = False
    env.world.cheese = cheese

    # env.show()

    losses = []
    wins = []
    for now in range(1, timesteps + 1):
        env.update(sum(mouse.eaten for mouse in env.world.mice), 
                   sum(mouse.fed for mouse in env.world.mice))

        losses.append(mouse.eaten)
        wins.append(mouse.fed)

    return ' '.join(map(str, losses + wins))


def run(params, test_=True):
    runs, timesteps, num_mice = process(params)
    global test
    test = test_

    for run in range(runs):
        print(worker((timesteps, num_mice)))
