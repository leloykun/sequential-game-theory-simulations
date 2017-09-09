import sys
import time
import random
import multiprocessing

from cell import Cell
from agent import Agent
from world import World
from qlearn import QLearn
from environment import Environment


sim_name = 'cat-mouse'
max_visual_depth = 4


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

    def update(self):
        if self.move:
            cell = self.cell
            while cell == self.cell:
                self.goInDirection(random.randrange(self.world.num_dir))


class Cat(Agent):
    colour = 'red'
    visual_depth = 2

    def __init__(self):
        self.ai = QLearn(
            actions=list(range(8)),     # world.num_dir = 8
            temp=5,
            alpha=0.9,
            gamma=0.9,
            epsilon=0.1)
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
            self.ai.learn(self.last_state, self.last_action, reward, state)

        state = self.calc_state()

        action = self.ai.chooseAction(state)
        self.last_state = state
        self.last_action = action

        self.goInDirection(action)

    # TODO: consider wrapping here
    def calc_state(self):
        mouse = self.world.mouse
        if abs(self.cell.x - mouse.cell.x) <= self.visual_depth and \
           abs(self.cell.y - mouse.cell.y) <= self.visual_depth:
            return ((self.cell.x - mouse.cell.x), (self.cell.y - mouse.cell.y))
        else:
            # default
            return (100, 100)

    def get_data(self):
        pass


def worker(params):
    alpha, gamma, trials, steps = params
    
    env = Environment(world=World(map='worlds/box10x10.txt', Cell=CasualCell))
    
    cat = Cat()
    env.add_agent(cat)
    cat.ai.alpha = alpha/10
    cat.ai.gamma = gamma/10
    cat.ai.temp = 0.4
    env.world.cat = cat
    
    mouse = Mouse()
    env.add_agent(mouse)
    mouse.move = True
    env.world.mouse = mouse
    
    env.world.fed = 0
    prev_fed = 0
    result = [alpha, gamma]
    while env.world.fed < trials:
        env.update(0, env.world.cat.fed)
        
        if env.world.fed is not prev_fed and (env.world.fed + 1) % steps == 0:
            result.append(env.world.age)
        prev_fed = env.world.fed
    
    return result
    
def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def run(trials=100, steps=10, runs=5):
    print("cat-mouse starting...")
    print("trials = %d,  steps = %d,  runs = %d" % (trials, steps, runs))
    sim_start = time.time()
    
    for depth in range(1, max_visual_depth + 1):
        Cat.visual_depth = depth
        print("   visual depth:", Cat.visual_depth)
        
        for run in range(1, runs + 1):
            run_start = time.time()
            
            params = []
            for alpha in range(11):
                for gamma in range(11):
                    params.append((alpha, gamma, trials, steps))
            
            pool = multiprocessing.Pool(4)
            results = pool.map(func=worker, iterable=params)
            pool.close()
            
            to_save = ""
            for result in results:
                to_save += ' '.join(map(str, result)) + '\n'
            savefile = open("sims/" + sim_name + "/data/" + str(depth) + "/data" + str(run) + ".txt", 'w')
            savefile.write(to_save)
            savefile.close()
            # print(worker((5, 5, depth, run)))
            
            print("     ", ord(run), "runtime:", time.time() - run_start, "secs")
    
    print("cat-mouse finished...")
    print("overall runtime:", time.time() - sim_start, "secs")
    print()
