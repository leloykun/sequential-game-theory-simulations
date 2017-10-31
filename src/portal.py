import os
import sys
import time
import inspect
import importlib

from .sims import cat_mouse
from .sims import cat_mouse_cheese
from .sims import route_choice
from .sims import specialization
from .sims import simple_migration
from .sims import migration


sim_modules = {"cat_mouse" : cat_mouse,
               "cat_mouse_cheese" : cat_mouse_cheese,
               "route_choice" : route_choice,
               "specialization" : specialization,
               "simple_migration" : simple_migration,
               "migration" : migration}


def load_sims(list_file=os.path.join(os.path.dirname(__file__),
                                     'sims/list.txt')):
    """
    
    Parameters
    ----------
    list_file : str
        

    Returns
    -------
    dict {str : list of str}
        
    """
    sims = {}

    with open(list_file) as f:
        sims_list = f.readlines()

        for line in sims_list:
            if line[0] != '#':
                sim_name, *params = line.split()
                sims[sim_name] = params

    return sims


def run(list_file=os.path.join(os.path.dirname(__file__),
                               'sims/list.txt')):
    """
    
    Parameters
    ----------
    list_file : str
        
    """
    sims = load_sims(list_file)
    
    for sim_name in sims:
        params = sims[sim_name]

        print(sim_name, "started with params:", params)
        sim_start = time.time()

        if sim_name in sim_modules:
            sim_modules[sim_name].run(params)
        else:
            raise("simulation %s not found".format(sim_name))

        print(sim, "finished with runtime:", time.time() - sim_start, "secs\n")
