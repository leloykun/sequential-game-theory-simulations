import random

from qlearn import QLearn

'''lookcells = [(1, 1), (1, 0), (1, -1), 
             (0, 1), (0, 0), (0, -1),
             (-1, 1), (-1, 0), (-1, -1)]'''
lookcells = []
for i in range(-3, 3):
    for j in range(-3, 3):
        lookcells.append((i, j))
        
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
    
    '''def __getattr__(self, key):
        if key == 'leftCell':
            return self.getCellOnLeft()
        elif key == 'rightCell':
            return self.getCellOnRight()
        elif key == 'aheadCell':
            return self.getCellAhead()
        raise AttributeError(key)'''

    def turn(self, amount):
        self.dir = (self.dir + amount) % self.world.num_dir

    def turnLeft(self):
        self.turn(-1)

    def turnRight(self):
        self.turn(1)

    def turnAround(self):
        self.turn(self.world.num_dir / 2)

    # return True if successfully moved in that direction
    def goInDirection(self, dir):
        target = self.cell.neighbour[dir]
        if getattr(target, 'wall', False):
            #print "hit a wall"
            return False
        self.cell = target
        return True

    def goForward(self):
        self.goInDirection(self.dir)

    def goBackward(self):
        self.turnAround()
        self.goForward()
        self.turnAround()

    def getCellAhead(self):
        return self.cell.neighbour[self.dir]

    def getCellOnLeft(self):
        return self.cell.neighbour[(self.dir - 1) % self.world.num_dir]

    def getCellOnRight(self):
        return self.cell.neighbour[(self.dir + 1) % self.world.num_dir]

    def goTowards(self, target):
        if self.cell == target:
            return
        best = None
        for n in self.cell.neighbours:
            if n == target:
                best = target
                break
            dist = (n.x - target.x) ** 2 + (n.y - target.y) ** 2
            if best is None or bestDist > dist:
                best = n
                bestDist = dist
        if best is not None:
            if getattr(best, 'wall', False):
                return
            self.cell = best

class Cheese(Agent):
    colour = 'yellow'
    
    def update(self):
        pass
        
class Mouse(Agent):
    colour = 'grey'
    
    def __init__(self):
        self.ai = QLearn(
            actions = list(range(8)), # world.num_dir = 8
            temp    = 5,
            alpha   = 0.9,
            gamma   = 0.9,
            epsilon = 0.1)
        
        self.eaten = 0
        self.fed   = 0
        
        self.last_action = None
        self.last_state  = None
    
    def update(self):
        state = self.calc_state()
        reward = -1
        
        if self.cell == self.world.cat.cell:
            self.eaten += 1
            reward = -100
            if self.last_state is not None:
                self.ai.learn(self.last_state, self.last_action, reward, state)
            
            self.last_state = None
            self.cell = self.env.get_random_avail_cell()
            return
        
        if self.cell == self.world.cheese.cell:
            self.fed += 1
            reward = 50
            self.world.cheese.cell = self.env.get_random_avail_cell()
        
        state = self.calc_state()
        print(state)
        action = self.ai.chooseAction(state)
        self.last_state = state
        self.last_action = action
        
        self.goInDirection(action)
        
    def calc_state(self):
        cat = self.world.cat
        cheese = self.world.cheese
        def cell_value(cell):
            if cat.cell is not None and (cell.x == cat.cell.x and
                                         cell.y == cat.cell.y):
                return 3
            elif cheese.cell is not None and (cell.x == cheese.cell.x and
                                              cell.y == cheese.cell.y):
                return 2
            elif cell.wall:
                return 1
            else:
                return 0
        return tuple([cell_value(self.world.get_wrapped_cell(self.cell.x + j, self.cell.y + i))
                      for i,j in lookcells])
        
    def get_date(self):
        pass
    
class Cat(Agent):
    colour = 'red'
    
    def update(self):
        cell = self.cell
        if cell != self.world.mouse.cell:
            self.goTowards(self.world.mouse.cell)
            while cell == self.cell:
                self.goInDirection(random.randrange(self.world.num_dir))
    
    def get_data(self):
        pass
