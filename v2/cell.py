import settings


class Cell:
    resources = [settings.MAX_RES_AMOUNT for _ in range(
        settings.RESOURCE_COUNT)]
    wall = False
    world = None

    def __getattr__(self, key):
        if key in settings.NEIGHBOUR_SYNONYMS:
            pts = [
                self.world.getPointInDirection(self.x, self.y, dir)
                for dir in range(self.world.directions)
            ]
            ns = tuple([self.world.grid[y][x] for (x, y) in pts])
            for n in settings.NEIGHBOUR_SYNONYMS:
                self.__dict__[n] = ns
            return ns
        raise AttributeError(key)

    def num_agents(self):
        return len(self.agents)

    def colour(self):
        if self.wall:
            return 'black'
        elif settings.TO_COLOR_CELLS:
            ratio = sum(self.resources) / \
                (settings.MAX_RES_AMOUNT * settings.RESOURCE_COUNT)
            gradient = hex(int(ratio * 64) + 191)[2:]
            if len(gradient) < 2:
                gradient = '0' + gradient
            return '#ffff' + gradient
        else:
            return '#eeeff7'

    def load(self, data):
        if data == 'X':
            self.wall = True
            self.resources = [0 for _ in range(settings.RESOURCE_COUNT)]
            self.growthRate = [1 for _ in range(settings.RESOURCE_COUNT)]
        else:
            self.wall = False
            self.resources = [settings.MAX_RES_AMOUNT for _ in range(
                settings.RESOURCE_COUNT)]
            self.growthRate = settings.DEF_GROWTH_RATE

    def update(self):
        if settings.TO_UPDATE_CELLS:
            for i in range(settings.RESOURCE_COUNT):
                self.resources[i] += settings.MAX_RES_AMOUNT * \
                    self.growthRate[i]
                # normalize
                self.resources[i] = min(
                    self.resources[i], settings.MAX_RES_AMOUNT)
