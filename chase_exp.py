import sys
import time
import math
import multiprocessing

from world import World
from cells import Casual
from environment import Environment

import agents

timesteps = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 100
runs = int(sys.argv[3]) if len(sys.argv) > 3 else 1
show = int(sys.argv[4]) if len(sys.argv) > 4 else 0


def worker(params):
    # calculation of Residual Entropy for each State (SRE)
    # should only be used when chooseAction method is boltzmann
    def calcSRE(peep, state):
        eprobs = peep.ai.getEProbs(state)
        # print("eprobs:", eprobs)
        return -sum([eprob * math.log10(eprob) for eprob in eprobs]) \
            / math.log10(env.world.num_dir)

    max_states = 40

    # calculation of the Average Residual Entropy for each Agent (ARE)
    def calcARE(peep):
        states = peep.ai.states
        if len(states) > 0:
            # return sum([calcSRE(peep, state) for state in states]) \
            #    / len(states)
            return (sum([calcSRE(peep, state) for state in states]) +
                    (max_states - len(states))) / max_states
        else:
            return 1

    alpha, gamma = params

    env = Environment(world=World(map='worlds/box20x10.txt', Cell=Casual))

    mouse = agents.Mouse()
    env.add_agent(mouse)
    mouse.ai.alpha = alpha/10
    mouse.ai.gamma = gamma/10
    mouse.ai.temp = 0.4
    env.world.mouse = mouse

    data_qvalues = ""
    data_states = ""
    data_sre = ""

    global timesteps, intervals, show
    if show == 1:
        env.show()
    for now in range(timesteps):
        env.update(losses=0, wins=env.world.mouse.score)

        data_qvalues += "qValues: " + str(len(mouse.ai.q)) + "\n"
        for qkey in mouse.ai.q:
            (a, b), c = qkey
            d = mouse.ai.q[qkey]
            data_qvalues += " ".join(map(str, [a, b, c, d])) + "\n"

            data_states += "states: " + str(len(mouse.ai.states)) + "\n"
        for state in mouse.ai.states:
            a, b = state
            data_states += " ".join(map(str, [a, b])) + "\n"

            data_sre += str(mouse.ai.aveSRE) + " " + str(calcARE(mouse)) + "\n"

        '''if now < 100:
            print("states:", mouse.ai.states)
            print(mouse.ai.aveSRE, calcARE(mouse))
            print()'''

    return (data_qvalues, data_states, data_sre)


def to_text(data):
    text = ""
    for num in data:
        text += " " + str(num)
    return text


if __name__ == '__main__':
    print("start: timesteps=%d, intervals=%d, runs=%d" %
          (timesteps, intervals, runs))
    start = time.time()

    params = []
    for run in range(runs):
        params.append((0.5, 0.5))

    pool = multiprocessing.Pool(4)
    results = pool.map(func=worker, iterable=params)
    pool.close()

    for r in range(1, runs + 1):
        # print(results[r - 1])
        data_qvalues, data_states, data_sre = results[r - 1]
        with open("docs/experiments/6/"+str(r)+"qvalues.txt", 'w') as f:
            f.write(data_qvalues)
        with open("docs/experiments/6/"+str(r)+"states.txt", 'w') as f:
            f.write(data_states)
        with open("docs/experiments/6/"+str(r)+"sre.txt", 'w') as f:
            f.write(data_sre)

    print("runtimme:", time.time() - start, "secs")
