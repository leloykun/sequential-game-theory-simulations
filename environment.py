import random
from itertools import count

class Environment:
    def __init__(self, world):
        self.world = world
        self.agents = []
        self.database = []
        self.data_output = ""
        
        self.world.display.activate(size=30)
        self.world.display.delay = 1
    
    def add_agent(self, agent, cell=None):
        agent.env = self
        agent.world = self.world
        agent.id = self.get_next_id()
        if cell is None:
            cell = self.get_random_avail_cell()
        agent.cell = cell
        
        self.world.agents.append(agent)
        self.agents.append(agent)
        
    def get_next_id(self):
        for id in count(0):
            yield id
    
    def get_random_avail_cell(self):
        while True:
            x = random.randrange(self.world.width)
            y = random.randrange(self.world.height)
            cell = self.world.get_cell(x, y)
            if not (cell.wall or cell.num_agents() > 0):
                return cell
    
    def update(self):
        #print("update env")
        self.world.update(self.world.mouse.eaten, self.world.mouse.fed)
    
    def get_data(self):
        pass
