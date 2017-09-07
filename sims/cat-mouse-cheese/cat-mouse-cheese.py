import sys
import time
import random
import multiprocessing

from cell import Cell
from agent import Agent
from world import World
from qlearn import QLearn
from environment import Environment


class Driver:
    def __init__(self):
        self.ai.QLearn(
            actions=[0, 1],
            temp=5,
            alpha=0.5,
            gamma=0.5,
            epsilon=0.1)
        self.ai.agent = self
        
        self.last_action = None
        self.last_state = None


def process(params):
    return map(int, params)

def run(params):
    trials, runs = process(params)
    
    print("cat-mouse-cheese starting...")
    print("trials = %d,  runs = %d" % (trials, runs))
    sim_start = time.time()
    
    print("cat-mouse-cheese finished...")
    print("overall runtime:", time.time() - sim_start, "secs")
    print()
