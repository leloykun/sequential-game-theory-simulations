from world import World
from cells import Casual
from environment import Environment

from agents import Cheese
from agents import Mouse
from agents import Cat

if __name__ == '__main__':

    env = Environment(world=World(map='worlds/waco.txt', Cell=Casual))
    
    mouse = Mouse()
    env.add_agent(mouse)
    env.world.mouse = mouse
    
    cat = Cat()
    env.add_agent(cat)
    env.world.cat = cat
    
    cheese = Cheese()
    env.add_agent(cheese)
    env.world.cheese = cheese
    
    # for 10_000 training ages
    for _ in range(1000000):
        env.update()
    