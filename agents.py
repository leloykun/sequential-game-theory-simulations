import random

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
    def __getattr__(self, key):
        if key == 'leftCell':
            return self.getCellOnLeft()
        elif key == 'rightCell':
            return self.getCellOnRight()
        elif key == 'aheadCell':
            return self.getCellAhead()
        raise AttributeError(key)

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
    
    def __init__(self, env=None, world=None, cell=None):
        self.env   = env
        self.world = world
        self.cell  = cell

class Cheese(Agent):
    colour = 'yellow'
    
    def update(self):
        pass
        
class Mouse(Agent):
    alpha = 0.2
    gamma = 0.9
    temp  = 5
    colour = 'grey'
    
    def update(self):
        if self.cell == self.world.cat.cell:
            self.cell = self.env.get_random_avail_cell()
    
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
