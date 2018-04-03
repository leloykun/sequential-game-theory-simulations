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
from .sims import wolfpack
from .sims import wolfpack_reduction
from .sims import wolfpack_reduction_2
from .sims import wolfpack_scene


sim_modules = {"cat_mouse" : cat_mouse,
               "cat_mouse_cheese" : cat_mouse_cheese,
               "route_choice" : route_choice,
               "specialization" : specialization,
               "simple_migration" : simple_migration,
               "migration" : migration,
               "wolfpack" : wolfpack,
               "wolfpack_reduction" : wolfpack_reduction,
               "wolfpack_reduction_2" : wolfpack_reduction_2,
               "wolfpack_scene": wolfpack_scene}


def run(sims):
    """

    Parameters
    ----------
    list_file : str

    """
    # sims = load_sims(list_file)

    for sim_name in sims:
        params = sims[sim_name]

        print(sim_name, "started with params:", params)
        sim_start = time.time()

        if sim_name in sim_modules:
            sim_modules[sim_name].run(params)
        else:
            raise("simulation %s not found".format(sim_name))

        print(sim_name, "finished with runtime:", time.time() - sim_start, "secs\n")
