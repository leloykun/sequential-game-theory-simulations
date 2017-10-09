import sys
import time
import random
import multiprocessing

from ..utils import ord, process

from ...world import World
from ...qlearn import QLearn

sim_name = 'route_choice'
output_dir = 'sims/' + sim_name + '/data/'

test = False


class DriverWorld(World):
    agents = []

    def __init__(self, road_cap):
        self.road_cap = road_cap
        self.num_roads = len(road_cap)
        self.road_cnt = [0 for _ in range(self.num_roads)]

    def update(self):
        self.road_cnt = [0 for _ in range(self.num_roads)]

        for agent in self.agents:
            agent.do_action()
        # print()

        total_rewards = 0
        for agent in self.agents:
            total_rewards += agent.learn()

    def get_are(self):
        sum_stat_are = 0
        sum_dyna_are = 0

        for agent in self.agents:
            sum_stat_are += agent.ai.stat_are
            sum_dyna_are += agent.ai.dyna_are

        return (sum_stat_are / len(self.agents),
                sum_dyna_are / len(self.agents))


class Driver:
    cell = (0, 0)

    def __init__(self, _world):
        self.world = _world

        self.ai = QLearn(temp=0.01, actions=[0, 1, 2, 3])
        self.ai.agent = self

        self.last_action = None
        self.last_state = None

    def do_action(self):
        self.state = 0
        action = self.ai.choose_action(self.state)

        self.last_state = self.state
        self.last_action = action

        self.world.road_cnt[action] += 1
        # print(action, end=" ")

    def learn(self):
        reward = self.calc_reward()
        self.ai.learn(self.last_state, self.last_action,
                      reward, self.state)
        return reward

    def calc_reward(self):
        if self.world.road_cap[self.last_action] >= self.world.road_cnt[self.last_action]:
            return 1
        else:
            return -1


def worker(params):
    run, timesteps, num_drivers, road_cap = params
    global test

    world = DriverWorld(road_cap)
    for _ in range(num_drivers):
        agent = Driver(world)
        agent.ai.max_states = len(road_cap)
        world.agents.append(agent)

    choice_dist = []
    res_ent = []

    for _ in range(timesteps):
        world.update()
        choice_dist.append(' '.join(map(str, world.road_cnt)))
        res_ent.append(' '.join(map(str, world.get_are())))

    if not test:
        with open(output_dir + 'dis/' + str(run) + 'run.txt', 'w') as f:
            f.write('\n'.join(choice_dist))

        with open(output_dir + 'are/' + str(run) + 'run.txt', 'w') as f:
            f.write('\n'.join(res_ent))


def run(params, test_=False):
    runs, timesteps, num_drivers, *road_cap = process(params)
    global test
    test = test_

    params = []
    for run in range(1, runs + 1):
        params.append((run, timesteps, num_drivers, road_cap))

    with multiprocessing.Pool(4) as pool:
        pool.map(worker, params)
