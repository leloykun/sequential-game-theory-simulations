import random

from qlearn import QLearn


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
            return self.get_cell_on_left()
        elif key == 'rightCell':
            return self.get_cell_on_right()
        elif key == 'aheadCell':
            return self.get_cell_ahead()
        raise AttributeError(key)'''

    def turn(self, amount):
        self.dir = (self.dir + amount) % self.world.num_dir

    def turn_left(self):
        self.turn(-1)

    def turn_right(self):
        self.turn(1)

    def turn_around(self):
        self.turn(self.world.num_dir / 2)

    # return True if successfully moved in that direction
    def go_in_direction(self, dir):
        target = self.cell.neighbour[dir]
        if getattr(target, 'wall', False):
            # print "hit a wall"
            return False
        self.cell = target
        return True

    def go_forward(self):
        self.go_in_direction(self.dir)

    def go_backward(self):
        self.turn_around()
        self.go_forward()
        self.turn_around()

    def get_cell_ahead(self):
        return self.cell.neighbour[self.dir]

    def get_cell_on_left(self):
        return self.cell.neighbour[(self.dir - 1) % self.world.num_dir]

    def get_cell_on_right(self):
        return self.cell.neighbour[(self.dir + 1) % self.world.num_dir]

    def go_towards(self, target):
        if self.cell == target:
            return
        best = None
        for n in self.cell.neighbours:
            if n == target:
                best = target
                break
            dist = (n.x - target.x)**2 + (n.y - target.y)**2
            if best is None or bestDist > dist:
                best = n
                bestDist = dist
        if best is not None:
            if getattr(best, 'wall', False):
                return
            self.cell = best
