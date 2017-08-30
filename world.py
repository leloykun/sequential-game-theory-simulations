from displays import PygameDisplay

class World:
    map     = None
    width   = None
    height  = None
    
    Cell    = None
    num_dir = 8
    
    data    = None
    grid    = None
    backup  = None
    
    agents = []
    age    = 0
    
    total_deaths = 0
    total_borns  = 0
    
    def __init__(self, map='worlds/box5v5', Cell=None, num_dir=8):
        self.map = map
        self.Cell = Cell
        self.num_dir = num_dir
        
        self.display = PygameDisplay(self)
        
        self.rebuild()
    
    def get_data(self):
        pass
    
    def rebuild(self, new_map=None):
        if new_map is not None:
            self.map = new_map
        
        with open(self.map) as m:
            self.data = m.readlines()
        self.data = [row.rstrip() for row in self.data]
        
        if self.height is None:
            self.height = len(self.data)
        if self.width is None:
            self.width  = max([len(row.rstrip()) for row in self.data])
        
        self.reset()
        self.load()
        
    def reset(self):
        self.grid   = [[self.make_cell(i, j) for i in range(self.width)]
                                             for j in range(self.height)]
        self.backup = [[{} for i in range(self.width)]
                           for j in range(self.height)]
        
        self.agents = []
        self.age    = 0
        
        self.total_deaths = 0
        self.total_borns  = 0
        
    def load(self):
        if not hasattr(self.Cell, 'load'):
            return
        
        
        #self.reset()
        for j in range(self.height):
            for i in range(min(self.width, len(self.data[j]))):
                self.grid[j][i].load(self.data[j][i])
    
    def update(self):
        if hasattr(self.Cell, 'update'):
            for agent in self.agents:
                agent.update()
            for j, row in enumerate(self.grid):
                for i, cell in enumerate(row):
                    self.backup[j][i].update(cell.__dict__)
                    cell.update()
                    cell.__dict__, self.backup[j][i] = self.backup[j][i], cell.__dict__
            for j, row in enumerate(self.grid):
                for i, cell in enumerate(row):
                    cell.__dict__, self.backup[j][i] = self.backup[j][i], cell.__dict__
            self.display.redraw()
        else:
            for agent in self.agents:
                old_cell = agent.cell
                agent.update()
                if old_cell != agent.cell:
                    self.display.redraw_cell(old_cell.x, old_cell.y)
                self.display.redraw_cell(agent.cell.x, agent.cell.y)
        self.display.update()
        self.age += 1
    
    def make_cell(self, x, y):
        return self.Cell(self, x, y)
        
    def get_cell(self, x, y):
        return self.grid[y][x]
    
    def get_wrapped_cell(self, x, y):
        return self.grid[y % self.height][x % self.width]
    
    def randomize(self):
        if not hasattr(self.Cell, 'randomize'):
            return
        for row in self.grid:
            for cell in row:
                cell.randomize()
        
    