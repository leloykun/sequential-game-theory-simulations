class Cell:
    wall = False
    world = None
    
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
        
class Casual(Cell):
    wall = False
    
    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'
    
    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False
    
    def num_agents(self):
        return len(self.agents)
    