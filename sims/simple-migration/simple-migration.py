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
            self.ai.learn(self.last_state, self.last_action, reward, state)

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
    alpha, gamma, temp, timesteps, interval = params

    env = Environment(world=World(map='worlds/box20x10.txt', Cell=CasualCell))

    mouse = Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha/10
    mouse.ai.gamma = gamma/10
    mouse.ai.temp = temp
    env.world.mouse = mouse

    scores = []

    # env.show()
    for now in range(1, timesteps + 1):
        env.update(0, env.world.mouse.score)

        if now % interval == 0:
            scores.append(env.world.mouse.score)

    return str(temp) + ' ' + ' '.join(map(str, scores))

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def process(params):
    return map(int, params)

def run(params):
    timesteps, interval, runs, temp_powers = process(params)

    print("cat-mouse-cheese starting...")
    print("timesteps = %d,  runs = %d" % (timesteps, runs))
    sim_start = time.time()

    for run in range(1, runs + 1):
        run_start = time.time()

        params = []
        for power in range(-temp_powers, temp_powers + 1):
            params.append((0.5, 0.5, 2**power, timesteps, interval))

        with multiprocessing.Pool(4) as pool:
            results = pool.map(func=worker, iterable=params)

        with open('sims/' + sim_name + '/data/run' + str(run) + '.txt', 'w') as f:
            f.write('\n'.join(results))

        print("  ", ord(run), "runtime:", time.time() - run_start, "secs")

    print("cat-mouse-cheese finished...")
    print("overall runtime:", time.time() - sim_start, "secs")
    print()
