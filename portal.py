import os, sys, inspect
import importlib

import cell
import agent

# add current directory to pythonpath
cmd_folder = os.path.realpath(
    os.path.abspath(
        os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# get list of simulations
sims_list = sys.argv[1] if len(sys.argv) > 1 else 'sims/list.txt'

if __name__ == '__main__':
    # run each simulation
    with open(sims_list) as f:
        sims_list = f.readlines()
        for sim in sims_list:
            sim, *params = sim.split()
            #print(sim, params)
            if sim != "#":
                sim = importlib.import_module('sims.' + sim + '.' + sim)
                sim.run(params)
