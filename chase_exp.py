from world import World
from cells import Casual
from environment import Environment

import agents

import time
import multiprocessing

trials = 50
steps = 10
runs = 5

def worker(params):
    start = time.time()
    
    alpha, gamma = params
    env = Environment(world=World(map='worlds/box10x10.txt', Cell=Casual))
    
    mouse = agents.Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha/10
    mouse.ai.gamma = gamma/10
    mouse.ai.temp  = 0.4
    env.world.mouse = mouse
    
    '''cat = Cat()
    env.add_agent(cat)
    env.world.cat = cat'''
    
    cheese = agents.Cheese()
    env.add_agent(cheese)
    cheese.move = True
    env.world.cheese = cheese
    
    data = []
    
    #env.show()
    global trials, steps
    env.world.fed = 0
    prev_fed = 0
    while env.world.fed < trials:
        env.update()
        
        if env.world.fed is not prev_fed and (env.world.fed + 1) % steps == 0:
            data.append(env.world.age)
        prev_fed = env.world.fed

    return (alpha, gamma, tuple(data))

def to_text(data):
    text = ""
    for num in data:
        text += " " + str(num)
    return text
    
if __name__ == '__main__':
    for depth in range(1, 5):
        agents.visual_depth = depth
        print("visual depth:", agents.visual_depth)
        for run in range(1, runs + 1):
            start = time.time()
            
            params = []
            for alpha in range(11):
                for gamma in range(11):
                    params.append((alpha, gamma))
            
            pool = multiprocessing.Pool(4)
            result = pool.map(func=worker, iterable=params)
            pool.close()
            #worker((0.9, 0.9))
            
            #print(result)
            
            to_save = ""
            for alpha, gamma, age in result:
                to_save += "%d %d %s\n" % (alpha, gamma, to_text(age))
            savefile = open("docs/experiments/4/" + str(depth) + "/data" + str(run) + ".txt", 'w')
            savefile.write(to_save)
            savefile.close()

            print(run, "run time:", time.time() - start, "secs")
