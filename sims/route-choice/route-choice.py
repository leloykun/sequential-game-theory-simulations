import sys
import time
import random
import multiprocessing

from qlearn import QLearn
from world import World

sim_name = 'route-choice'


class DriverWorld(World):
    agents = []

    road_cap = [5, 15]
    road_cnt = [0, 0]

    def __init__(self):
        pass

    def update(self):
        self.road_cnt = [0, 0]
        
        for agent in self.agents:
            agent.do_action()
        
        for agents in self.agents:
            agent.learn()

        print(road_cnt)

class Driver:
    cell = (0, 0)
    
    def __init__(self, _world):
        self.world = _world
    
        self.ai = QLearn(actions=[0, 1])
        self.ai.agent = self

        self.last_action = None
        self.last_state = None

    def do_action(self):
        state = 0
        action = self.ai.chooseAction(state)

        self.last_state = state
        self.last_action = action

        self.world.road_cnt[action] += 1

    def learn(self):
        reward = self.calc_reward()
        self.ai.learn(self.last_state, self.last_action, reward, state)

    def calc_reward(self):
        return self.world.road_cap[last_action] - \
               self.world.road_cnt[last_action]


def worker(params):
    pass


def process(params):
    return map(int, params)


def run(params):
    timesteps, num_drivers = process(params)
    print(timesteps, num_drivers, "run nigger run")
    
    world = DriverWorld()
    for _ in range(num_drivers):
        agent = Driver(world)
        world.agents.append(agent)
        
    for _ in range(timesteps):
        world.update()
