neighbor_synonyms = ('neighbours', 'neighbors', 'neighbour', 'neighbor')


class Cell:
    wall = False
    world = None

    def __getattr__(self, key):
        if key in neighbor_synonyms:
            pts = [
                self.world.getPointInDirection(self.x, self.y, dir)
                for dir in range(self.world.num_dir)
            ]
            ns = tuple([self.world.grid[y][x] for (x, y) in pts])
            for n in neighbor_synonyms:
                self.__dict__[n] = ns
            return ns
        raise AttributeError(key)

    def __init__(self, world=None, x=None, y=None):
        self.world = world
        self.x = x
        self.y = y
        self.agents = []

    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'

    #def load(self):
    #    pass

    #def update(self):
    #    pass

    #def randomize(self):
    #    pass

    #def get_data(self):
    #    pass
