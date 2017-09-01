from world import World
from cells import Casual
from environment import Environment

from agents import Cheese
from agents import Mouse
from agents import Cat

import time
import _thread

results = [[(0, 0) for _ in range(11)] for _ in range(11)]
done = 0

lock = _thread.allocate_lock()

def sim(alpha, gamma, training_age):
    start = time.time()
    #print("start:", alpha, gamma, training_age)
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
    for i in range(training_age):
        env.update()
    
    end = time.time()
    
    lock.acquire()
    global results, done
    results[alpha][gamma] = (env.world.eaten, env.world.fed)
    done += 1
    lock.release()
    
    #print(alpha/10, gamma/10, env.world.eaten, env.world.fed, end - start)

if __name__ == '__main__':
    start = time.time()
    
    try:
        for alpha in range(11):
            for gamma in range(11):
                #sim(alpha, gamma, 10**4)
                _thread.start_new_thread(sim, (alpha, gamma, 10**5))
    except:
        print("Error: unable to start thread")
    
    while done != 121:
        pass
    
    to_save = ""
    for i in range(11):
        for j in range(11):
            eaten, fed = results[i][j]
            to_save += "%d %d %d %d\n" % (i, j, eaten, fed)
    savefile = open("data.txt", 'w')
    savefile.write(to_save)
    savefile.close()
    
    print("run time:", time.time() - start)