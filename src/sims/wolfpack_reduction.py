import os
import time
import random
import copy
import multiprocessing as mp

import numpy as np

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

param_values = np.linspace(0, 1, 11)


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
    reward_per_cat = 50
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
            reward += 50
        if self.world.can_cat_capture[1]:
            reward += 50
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


def worker(params):
    alpha, gamma, training_trials, test_trials, depth_a, depth_b, reward_per_cat = params

    def prepare(world):
        world.can_cat_capture = []
        for cat in world.cats:
            world.can_cat_capture.append(1 if cat.can_capture_mouse() else 0)

    env = Environment(World(os.path.join(os.path.dirname(os.path.dirname( __file__ )),
                                         'worlds/waco2.txt'),
                            CasualCell))

    '''   Training Phase'''
    cat_a = Cat()
    cat_a.ai.alpha = alpha
    cat_a.ai.gamma = gamma
    cat_a.ai.temp = 0.4
    cat_a.capture_radius = depth_a
    cat_a.reward_per_cat = reward_per_cat
    cat_a.idx = 0;

    cat_b = Cat()
    cat_b.ai.alpha = alpha
    cat_b.ai.gamma = gamma
    cat_b.ai.temp = 0.4
    cat_b.capture_radius = depth_b
    cat_b.reward_per_cat = reward_per_cat
    cat_b.idx = 1;

    env.add_agent(cat_a)
    env.add_agent(cat_b)
    env.world.cats = [cat_a, cat_b]

    mouse = Mouse()
    mouse.move = True
    mouse.id = 2;

    env.add_agent(mouse)
    env.world.mouse = mouse

    # env.show()

    env.world.fed = 0
    while env.world.fed < training_trials:
        prepare(env.world)
        env.update()

    training_results = [env.world.cats[0].total_rewards, env.world.cats[1].total_rewards]


    '''   Testing Phase   '''
    env = Environment(World(os.path.join(os.path.dirname(os.path.dirname( __file__ )),
                                         'worlds/waco2.txt'),
                            CasualCell))

    cat_a.total_rewards = 0
    cat_a.learning = False

    env.add_agent(cat_a)
    env.add_agent(cat_b)
    env.world.cats = [cat_a, cat_b]

    cat_b.total_rewards = 0
    cat_b.learning = False

    env.add_agent(mouse)
    env.world.mouse = mouse

    env.world.fed = 0
    while env.world.fed < test_trials:
        prepare(env.world)
        env.update()

    test_results = [env.world.cats[0].total_rewards, env.world.cats[1].total_rewards]

    return test_results
    #return training_results, test_results


def run(params, grid_params=False, test=False, to_save=True):
    runs, training_trials, test_trials = process(params)

    if test:
        preworker((0.5, 0.5, training_trials, test_trials, 2, 2, 50))
        return

    depths = [2, 4]
    rewards_per_cat = [20, 40, 60, 80, 100]

    params = []
    for reward in rewards_per_cat:
        for run in range(runs):
            params.append((0.5, 0.5, training_trials, test_trials, 2, 2, reward))
            params.append((0.5, 0.5, training_trials, test_trials, 2, 4, reward))
            params.append((0.5, 0.5, training_trials, test_trials, 4, 4, reward))

    with mp.Pool(mp.cpu_count()-1) as pool:
        results = pool.map(worker, params)

    results = np.array(results).reshape(len(rewards_per_cat), runs, 3, 2)
    np.save(output_dir + 'run_test', results)

    print(results.shape)
    print(results)
