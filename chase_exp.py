import sys
import time
import multiprocessing

from world import World
from cells import Casual
from environment import Environment

import agents

timesteps = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 100
runs      = int(sys.argv[3]) if len(sys.argv) > 3 else 1

def worker(params):
    start = time.time()
    alpha, gamma = params
    
    env = Environment(world=World(map='worlds/box20x10.txt', Cell=Casual))
    
    mouse = agents.Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha/10
    mouse.ai.gamma = gamma/10
    mouse.ai.temp  = 0.4
    env.world.mouse = mouse
    
    '''cat = Cat()
    env.add_agent(cat)
    env.world.cat = cat'''
    
    '''cheese = agents.Cheese()
    env.add_agent(cheese)
    cheese.move = True
    env.world.cheese = cheese'''
    
    data = []
    
    #env.show()
    global timesteps, intervals
    for now in range(timesteps):
        env.update()
        
        if (now + 1) % intervals == 0:
            data.append(env.world.mouse.score)
    
    return (alpha, gamma, tuple(data))

def to_text(data):
    text = ""
    for num in data:
        text += " " + str(num)
    return text
    
if __name__ == '__main__':
    print("start: trials=%d, steps=%d, runs=%d" % (timesteps, intervals, runs))
    start = time.time()
    
    params = []
    for r in range(runs):
        params.append((0.5, 0.5))
    
    pool = multiprocessing.Pool(4)
    results = pool.map(func=worker, iterable=params)
    pool.close()
    
    #print(result)
    
    for r in range(1, runs + 1):
        print(results[r - 1])
        _, _, res = results[r - 1]
        savefile = open("docs/experiments/5/data"+str(r)+".txt", 'w')
        savefile.write(to_text(res))
        savefile.close()

    print("run time:", time.time() - start, "secs")
