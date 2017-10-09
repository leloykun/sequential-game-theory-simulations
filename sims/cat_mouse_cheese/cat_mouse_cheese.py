import sys
import time
import random
import multiprocessing

from ..utils import ord, process

from ...cell import CasualCell
from ...agent import Agent
from ...agent import Prey as Cheese
from ...world import World
from ...qlearn import QLearn
from ...environment import Environment

sim_name = 'cat_mouse_cheese'
max_visual_depth = 4


class Mouse(Agent):
    colour = 'gray'
    visual_depth = 1
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
        cat = self.world.cat
        cheese = self.world.cheese

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

        return tuple([
            cell_value(self.world.get_wrapped_cell(self.cell.x + j, 
                                                   self.cell.y +i))
            for i, j in self.lookcells
        ])

    def going_to_obstacle(self, action):
        cell = self.world.get_point_in_direction(self.cell.x,
                                              self.cell.y,
                                              action)
        return self.world.get_cell(cell[0], cell[1]).wall


class Cat(Agent):
    colour = 'red'

    def update(self):
        cell = self.cell
        if cell != self.world.mouse.cell:
            self.go_towards(self.world.mouse.cell)
            while cell == self.cell:
                self.go_in_direction(random.randrange(self.world.num_dir))


def worker(params):
    alpha, gamma, timesteps, interval = params

    env = Environment(world=World(map='worlds/waco.txt', Cell=CasualCell))

    mouse = Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha / 10
    mouse.ai.gamma = gamma / 10
    mouse.ai.temp = 0.5
    env.world.mouse = mouse

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
        env.update(mouse.eaten, mouse.fed)

        if now % interval == 0:
            losses.append(mouse.eaten)
            wins.append(mouse.fed)

    losses = " ".join(map(str, losses))
    wins = " ".join(map(str, wins))

    return str(alpha) + " " + str(gamma) + " " + losses + " " + wins


def run(params):
    runs, timesteps, interval = process(params)

    for depth in range(1, max_visual_depth + 1):
        Mouse.visual_depth = depth
        print("   visual depth:", Mouse.visual_depth)

        for run in range(1, runs + 1):
            run_start = time.time()

            params = []
            for alpha in range(11):
                for gamma in range(11):
                    params.append((alpha, gamma, timesteps, interval))

            with multiprocessing.Pool(4) as pool:
                results = pool.map(worker, params)

            with open("sims/" + sim_name + "/data/" + str(depth) + "/data"
                      + str(run) + ".txt", 'w') as f:
                f.write("\n".join(results))

            print("     ", ord(run), "runtime:", time.time() - run_start, "secs")
