import sys
import time
import random
import multiprocessing

from cell import Cell
from agent import Agent
from world import World
from qlearn import QLearn
from environment import Environment

sim_name = 'simple-migration'
output_dir = 'sims/' + sim_name + '/data/'


class CasualCell(Cell):
    wall = False

    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'

    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False

    def num_agents(self):
        return len(self.agents)


class Mouse(Agent):
    colour = 'grey'

    def __init__(self):
        self.ai = QLearn(actions=list(range(8)))
        self.ai.agent = self

        self.eaten = 0
        self.fed = 0
        self.score = 0

        self.last_action = None
        self.last_state = None

    def update(self):
        state = self.calc_state()
        reward = state[0]
        self.score += reward

        if self.last_state is not None:
            self.ai.learn(self.last_state, self.last_action, reward,
                          state)

        action = self.ai.chooseAction(state)
        self.last_state = state
        self.last_action = action

        self.goInDirection(action)

    def calc_state(self):
        day = self.world.age % 100
        if day < 50:
            return (self.cell.y - 10, 0)
        else:
            return (11 - self.cell.y, 1)


def worker(params):
    alpha, gamma, temp_power, timesteps, run = params

    env = Environment(world=World(
        map='worlds/box20x10.txt', Cell=CasualCell))

    mouse = Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha / 10
    mouse.ai.gamma = gamma / 10
    mouse.ai.temp = 2**temp_power
    env.world.mouse = mouse

    scores = []
    positions = []
    res_ent = []
    num_states = []

    env.show()

    for now in range(1, timesteps + 1):
        env.update(0, mouse.score)

        scores.append(mouse.score)
        positions.append(mouse.cell.y)
        res_ent.append(
            str(mouse.ai.stat_ARE) + " " + str(mouse.ai.dyna_ARE))
        num_states.append(len(mouse.ai.states))

    output_dir_dir = output_dir + str(temp_power) + "/" + str(run)

    with open(output_dir_dir + "scores.txt", 'w') as f:
        f.write(' '.join(map(str, scores)))

    with open(output_dir_dir + "pos.txt", 'w') as f:
        f.write(' '.join(map(str, positions)))

    with open(output_dir_dir + "res_ent.txt", 'w') as f:
        f.write('\n'.join(map(str, res_ent)))

    with open(output_dir_dir + "num_states", 'w') as f:
        f.write(' '.join(map(str, num_states)))

def process(params):
    return map(int, params)


def run(params):
    timesteps, runs, temp_powers = process(params)

    print("cat-mouse-cheese starting...")
    print("timesteps = %d,  runs = %d" % (timesteps, runs))
    sim_start = time.time()

    params = []
    for run in range(1, runs + 1):
        for power in range(-temp_powers, temp_powers + 1):
            params.append((0.5, 0.5, power, timesteps, run))

    with multiprocessing.Pool(4) as pool:
        pool.map(func=worker, iterable=params)

    print("cat-mouse-cheese finished...")
    print("overall runtime:", time.time() - sim_start, "secs")
    print()
