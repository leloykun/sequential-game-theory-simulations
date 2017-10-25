import os
import sys
import time
import inspect
import importlib


'''
# add current directory to pythonpath
cmd_folder = os.path.realpath(
    os.path.abspath(
        os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# get list of simulations
sims_list = sys.argv[1] if len(sys.argv) > 1 else 'sims/list.txt'
'''


def run_sims():
    from .sims import cat_mouse_cheese as sim
    sim.run((10, 10000, 1000))


if __name__ == '__main__':
    run_sims()
    
"""
    # run each simulation
    with open(sims_list) as f:
        sims_list = f.readlines()

        for sim in sims_list:
            sim, *params = sim.split()

            if sim != "#":
                print(sim, "starting with params:", params)
                sim_start = time.time()

                sim = importlib.import_module('sims.' + sim)
                sim.run(params)

                print(
                    sim,
                    "finished with runtime:",
                    time.time() -
                    sim_start,
                    "secs\n")
"""
