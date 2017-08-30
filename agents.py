
class Agent:
    def __setattr__(self, key, val):
        if key == 'cell':
            # transfer the agent:
            # old -> val
            old = self.__dict__.get(key, None)
            if old is not None:
                old.agents.remove(self)
            if val is not None:
                val.agents.append(self)
        self.__dict__[key] = val
    
    def __init__(self, env=None, world=None, cell=None):
        self.env   = env
        self.world = world
        self.cell  = cell

class Mouse(Agent):
    alpha = 0.2
    gamma = 0.9
    temp  = 5
    colour = 'grey'
    
    def get_date(self):
        pass
    
class Cat(Agent):
    colour = 'red'
    
    def get_data(self):
        pass
