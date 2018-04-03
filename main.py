import os
import argparse

from src import portal


def load_sims(list_file):
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


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--simulation", nargs='+',
                    help="increase output verbosity", default="all")
args = parser.parse_args()


default_params = {"cat_mouse" : [10, 100, 10],
                  "cat_mouse_cheese" : [10, 10000, 1000],
                  "route_choice" : [10, 1000, 100, 10, 20, 30, 40],
                  "simple_migration" : [10, 10000, 5],
                  "migration" : [1, 100000, 3],
                  "wolfpack" : [10, 100, 100],
                  "wolfpack_reduction" : [10, 20, 20, 50],
                  "wolfpack_scene": [1000, 0, 100]}


if __name__ == '__main__':
    sims = {}
    if args.simulation == "all":
        list_file = os.path.join(os.path.dirname(__file__), 'src/sims/list.txt')
        sims = load_sims(list_file)
    elif args.simulation[0] in default_params:
        if len(args.simulation[1:]) != len(default_params[args.simulation[0]]):
            print("invalid parameters")
            sims = {args.simulation[0]: default_params[args.simulation[0]]}
        else:
            sims = {args.simulation[0]: args.simulation[1:]}
    portal.run(sims)
