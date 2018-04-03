import os
import time
import random
import copy
# import multiprocessing as mp

import pathos.multiprocessing as mp
import numpy as np

from .utils import to_ordinal, process

from ..agent import Agent
from ..agent import WolfpackMouse as Mouse
from ..agent import WolfpackCat as Cat
from ..world import World
from ..qlearn import QLearn
from ..cell import CasualCell
from ..environment import Environment

sim_name = 'wolfpack_reduction'
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))),
                          'data/raw/{}/'.format(sim_name))

param_values = np.linspace(0, 1, 11)
depths = [2, 4]
rewards_per_cat = [20, 40, 60, 80, 100]


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

    print([training_results, test_results])
    return [training_results, test_results]


def run(params, grid_params=False, test=False, to_save=True):
    runs, training_trials, test_trials, base_reward = process(params)

    if test:
        worker((0.5, 0.5, training_trials, test_trials, 2, 2, 50))
        return

    params = []
    for run in range(runs):
        params.append((0.5, 0.5, training_trials, test_trials, 2, 2, base_reward))
        params.append((0.5, 0.5, training_trials, test_trials, 2, 4, base_reward))
        params.append((0.5, 0.5, training_trials, test_trials, 4, 4, base_reward))

    with mp.Pool(mp.cpu_count()-1) as pool:
        results = pool.map(worker, params)

    results = np.array(results).reshape(runs, 3, 2, 2)
    np.save(output_dir + 'run_test', results)

    print(results.shape)
    print(results)
