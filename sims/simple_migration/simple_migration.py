import multiprocessing as mp

from ...agent import Agent
from ...world import World
from ...qlearn import QLearn
from ...cell import CasualCell
from ...environment import Environment

from ..utils import process

sim_name = 'simple_migration'
output_dir = 'sims/' + sim_name + '/data/'


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
            self.ai.learn(self.last_state,
                          self.last_action,
                          reward,
                          state)

        action = self.ai.choose_action(state)
        self.last_state = state
        self.last_action = action

        self.go_in_direction(action)

    def calc_state(self):
        day = self.world.age % 100
        if day < 50:
            return (self.cell.y - 10, 0)
        else:
            return (11 - self.cell.y, 1)


def worker(params):
    alpha, gamma, temp_power, timesteps, run, test = params

    env = Environment(world=World(outline='worlds/box20x10.txt',
                                  Cell=CasualCell))

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

    # env.show()

    for _ in range(1, timesteps + 1):
        env.update(0, mouse.score)

        scores.append(mouse.score)
        positions.append(mouse.cell.y)
        res_ent.append(
            str(mouse.ai.stat_are) + " " + str(mouse.ai.dyna_are))
        num_states.append(len(mouse.ai.states))

    output_dir_dir = output_dir + str(temp_power) + "/" + str(run)

    if not test:
        with open(output_dir_dir + "scores.txt", 'w') as f:
            f.write(' '.join(map(str, scores)))

        with open(output_dir_dir + "pos.txt", 'w') as f:
            f.write(' '.join(map(str, positions)))

        with open(output_dir_dir + "res_ent.txt", 'w') as f:
            f.write('\n'.join(map(str, res_ent)))

        with open(output_dir_dir + "num_states.txt", 'w') as f:
            f.write(' '.join(map(str, num_states)))


def run(params, test=False):
    runs, timesteps, temp_powers = process(params)

    params = []
    for run in range(1, runs + 1):
        for power in range(-temp_powers, temp_powers + 1):
            params.append((0.5, 0.5, power, timesteps, run, test))

    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(func=worker, iterable=params)
