import time
import math
import random
import multiprocessing as mp

from ..world import World
from ..qlearn import QLearn
from ..cell import CasualCell
from ..agent import DumbPrey as Cheese


def to_ordinal(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {
        1: "st",
        2: "nd",
        3: "rd"
    }.get(n % 10, "th"))


def process(params):
    if isinstance(params, str):
        params = params.split()
    assert type(params) in [list, tuple]
    return list(map(int, params))


class Simulation:
    sim_name = __name__.split('.')[-1]
    output_dir = 'sims/' + sim_name + '/data/'
    world_outline = 'worlds/box10x10.txt'
    test = False

    def worker(self, params):
        world = World(outline=self.world_outline, Cell=CasualCell))

    def run(self, params, test=False):
        self.test = test
