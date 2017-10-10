import time
import multiprocessing as mp

from ..utils import to_ordinal, process

from ...agent import Agent
from ...world import World
from ...qlearn import QLearn
from ...cell import CasualCell
from ...agent import Prey as Mouse
from ...environment import Environment

sim_name = 'cat_mouse'
output_dir = 'sims/' + sim_name + '/data/'

max_visual_depth = 4


class Cat(Agent):
    colour = 'red'
    visual_depth = 2

    def __init__(self):
        self.ai = QLearn(actions=list(range(8)))
        self.ai.agent = self

        self.eaten = 0
        self.fed = 0

        self.last_action = None
        self.last_state = None

    def update(self):
        state = self.calc_state()
        reward = -1

        if self.cell == self.world.mouse.cell:
            self.fed += 1
            reward = 50
            self.world.mouse.cell = self.env.get_random_avail_cell()

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

    # TODO: consider wrapping here
    def calc_state(self):
        mouse = self.world.mouse
        if abs(self.cell.x - mouse.cell.x) <= self.visual_depth and \
           abs(self.cell.y - mouse.cell.y) <= self.visual_depth:
            return ((self.cell.x - mouse.cell.x),
                    (self.cell.y - mouse.cell.y))
        else:
            # default
            return (100, 100)

    def going_to_obstacle(self, action):
        cell = self.world.get_point_in_direction(self.cell.x,
                                                 self.cell.y,
                                                 action)
        return self.world.get_cell(cell[0], cell[1]).wall

    def get_data(self):
        pass


def worker(params):
    alpha, gamma, trials, steps, test = params

    env = Environment(world=World(outline='worlds/box10x10.txt',
                                  Cell=CasualCell))

    cat = Cat()
    env.add_agent(cat)
    cat.ai.alpha = alpha / 10
    cat.ai.gamma = gamma / 10
    cat.ai.temp = 0.4
    env.world.cat = cat

    mouse = Mouse()
    env.add_agent(mouse)
    mouse.move = True
    env.world.mouse = mouse

    # env.show()

    env.world.fed = 0
    prev_fed = 0
    result = [alpha, gamma]
    while env.world.fed < trials:
        env.update(0, env.world.cat.fed)

        if env.world.fed is not prev_fed and (
                env.world.fed + 1) % steps == 0:
            result.append(env.world.age)
        prev_fed = env.world.fed

    return result


def run(params, test=False):
    runs, trials, steps = process(params)

    for depth in range(1, max_visual_depth + 1):
        Cat.visual_depth = depth
        print("   visual depth:", Cat.visual_depth)

        for run in range(1, runs + 1):
            run_start = time.time()

            params = []
            for alpha in range(11):
                for gamma in range(11):
                    params.append((alpha, gamma, trials, steps, test))

            if test:
                params = [(5, 5, trials, steps, test)]

            pool = mp.Pool(mp.cpu_count())
            results = pool.map(func=worker, iterable=params)
            pool.close()

            if not test:
                to_save = ""
                for result in results:
                    to_save += ' '.join(map(str, result)) + '\n'
                savefile = open(output_dir + str(depth) + "/data" + str(run) +
                                ".txt", 'w')
                savefile.write(to_save)
                savefile.close()

            print(
                "     ",
                to_ordinal(run),
                "runtime:",
                time.time() -
                run_start,
                "secs")
