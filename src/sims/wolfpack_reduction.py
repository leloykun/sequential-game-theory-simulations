import os
import time
import random
import multiprocessing as mp

from .utils import to_ordinal, process

from ..agent import Agent
from ..world import World
from ..qlearn import QLearn
from ..cell import CasualCell
#from ..agent import DumbPrey as Mouse
from ..environment import Environment

sim_name = 'wolfpack_reduction'
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))),
                          'data/raw/{}/'.format(sim_name))

max_visual_depth = 4
param_values = [p/10 for p in range(11)]
#print(param_values)


class Mouse(Agent):
    colour = 'yellow'
    mark = False

    def update(self):
        if self.move:
            cell = self.cell
            while cell == self.cell:
                self.go_in_direction(random.randrange(self.world.num_dir))

        if self.mark:
            self.mark = False
            self.cell = self.env.get_random_avail_cell()

class Cat(Agent):
    colour = 'red'
    visual_depth = 6
    capture_radius = 2
    lookcells = []

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
        if self.world.cats[0].can_capture_mouse():
            reward += 100
        if self.world.cats[1].can_capture_mouse():
            reward += 100
        return reward

    def update(self):
        state = self.calc_state()
        reward = -1

        if self.can_capture_mouse():
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


def preworker(params):
    alpha, gamma, trials, depth = params

    env = Environment(World(os.path.join(os.path.dirname(os.path.dirname( __file__ )),
                                         'worlds/waco2.txt'),
                            CasualCell))

    cat1 = Cat()
    cat1.ai.alpha = alpha
    cat1.ai.gamma = gamma
    cat1.ai.temp = 0.4
    cat1.capture_radius = depth
    env.add_agent(cat1)

    cat2 = Cat()
    cat2.ai.alpha = alpha
    cat2.ai.gamma = gamma
    cat2.ai.temp = 0.4
    cat2.capture_radius = depth
    env.add_agent(cat2)

    env.world.cats = [cat1, cat2]

    mouse = Mouse()
    mouse.move = True
    env.add_agent(mouse)
    env.world.mouse = mouse

    # env.show()

    env.world.fed = 0
    while env.world.fed < trials:
        env.update()

    return env.world.cats


def postworker(params):
    trials, cat1, cat2 = params

    env = Environment(World(os.path.join(os.path.dirname(os.path.dirname( __file__ )),
                                         'worlds/waco2.txt'),
                            CasualCell))

    cat1.total_rewards = 0
    cat1.learning = False
    env.add_agent(cat1)

    cat2.total_rewards = 0
    cat2.learning = False
    env.add_agent(cat2)

    env.world.cats = [cat1, cat2]

    mouse = Mouse()
    mouse.move = True
    env.add_agent(mouse)
    env.world.mouse = mouse

    # env.show()

    env.world.fed = 0
    while env.world.fed < trials:
        env.update()

    return env.world.cats[0].total_rewards, env.world.cats[1].total_rewards


def run(params, grid_params=False, test=False, to_save=True):
    runs, trials = process(params)

    if test:
        preworker((0.5, 0.5, trials, steps, 2))
        return

    print("pre experiment")
    cats = []
    for depth in range(1, max_visual_depth + 1):
        cats.append(preworker((0.5, 0.5, trials, depth)))

    for pair in cats:
        print(pair[0].total_rewards, pair[1].total_rewards)

    print("main experiment:")
    idx = [1, 3]
    for run in range(1, runs + 1):
        print("run {}: ".format(run))
        for i in idx:
            for j in idx: 
                res = postworker((trials, cats[i][0], cats[j][0]))
                print("D" if i == 1 else "C",
                      "D" if j == 1 else "C",
                      res[0],
                      res[1])
