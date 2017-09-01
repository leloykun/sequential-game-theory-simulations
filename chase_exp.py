from world import World
from cells import Casual
from environment import Environment

from agents import Cheese
from agents import Mouse
from agents import Cat

import time
import multiprocessing

training_ages = 10**5
runs = 3

def worker(params):
    start = time.time()
    
    alpha, gamma = params
    #print("start:", alpha, gamma, training_age)
    env = Environment(world=World(map='worlds/box10x10.txt', Cell=Casual))
    
    mouse = Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha/10
    mouse.ai.gamma = gamma/10
    mouse.ai.temp  = 0.4
    env.world.mouse = mouse
    
    '''cat = Cat()
    env.add_agent(cat)
    env.world.cat = cat'''
    
    cheese = Cheese()
    env.add_agent(cheese)
    cheese.move = True
    env.world.cheese = cheese
    
    #env.show()
    global training_ages
    for i in range(training_ages):
        env.update()
    
    
    return (alpha, gamma, env.world.fed)
    
    end = time.time()
    #print(alpha/10, gamma/10, env.world.eaten, env.world.fed, end - start)

if __name__ == '__main__':
    for run in range(1, runs + 1):
        start = time.time()
        
        params = []
        for alpha in range(11):
            for gamma in range(11):
                params.append((alpha, gamma))
        
        pool = multiprocessing.Pool(4)
        result = pool.map(func=worker, iterable=params)
        pool.close()
        
        #print(result)
        
        to_save = ""
        for alpha, gamma, fed in result:
            to_save += "%d %d %d\n" % (alpha, gamma, fed)
        savefile = open("docs/experiments/2/data" + str(run) + ".txt", 'w')
        savefile.write(to_save)
        savefile.close()

        print("run time:", time.time() - start)