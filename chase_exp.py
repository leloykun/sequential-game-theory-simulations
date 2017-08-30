from world import World
from cells import Casual
from environment import Environment

from agents import Mouse
from agents import Cat

if __name__ == '__main__':

    env = Environment(world=World(map='worlds/waco.txt', Cell=Casual))
    
    # add 5 mice
    for _ in range(5):
        env.add_agent(Mouse())
    
    # add 1 cat
    for _ in range(1):
        env.add_agent(Cat())
    

    
    # for 10_000 training ages
    for _ in range(10000):
        env.update()
        env.world.display.paused = True
    