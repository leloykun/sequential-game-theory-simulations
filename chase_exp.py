from world import World
from cells import Casual
from environment import Environment

from agents import Cheese
from agents import Mouse
from agents import Cat

if __name__ == '__main__':
    
    for alpha in range(1, 10):
        for gamma in range(1, 10):
            env = Environment(world=World(map='worlds/waco.txt', Cell=Casual))
            
            mouse = Mouse()
            env.add_agent(mouse)
            mouse.ai.alpha = alpha/10
            mouse.ai.gamma = gamma/10
            env.world.mouse = mouse
            
            cat = Cat()
            env.add_agent(cat)
            env.world.cat = cat
            
            cheese = Cheese()
            env.add_agent(cheese)
            env.world.cheese = cheese
            
            #env.show()
            
            for i in range(100000):
                env.update()
                if i == 99999:
                    print(alpha/10, gamma/10, env.world.eaten, env.world.fed)
    