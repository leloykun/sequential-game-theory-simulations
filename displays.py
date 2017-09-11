import sys
import time
import pygame
import collections


class PygameDisplay:
    activated = False
    paused = False
    title = ''
    updateEvery = 1
    delay = 0
    screen = None

    def __init__(self, world):
        self.world = world

    def activate(self, size=4):
        self.size = size
        pygame.init()
        w = self.world.width * size
        h = self.world.height * size
        if self.world.num_dir == 6:
            w += size // 2
        if PygameDisplay.screen is None \
                or PygameDisplay.screen.get_width() != w \
                or PygameDisplay.screen.get_height() != h:
            PygameDisplay.screen = pygame.display.set_mode(
                (w, h), pygame.RESIZABLE, 32)
        self.activated = True
        self.defaultColour = self.getColour(
            self.world.grid[0][0].__class__())
        self.redraw()

    def redraw(self):
        if not self.activated:
            return
        self.screen.fill(self.defaultColour)
        hexgrid = self.world.num_dir == 6
        self.offsety = (
            self.screen.get_height() - self.world.height * self.size) // 2
        self.offsetx = (
            self.screen.get_width() - self.world.width * self.size) // 2
        sy = self.offsety
        odd = False
        for row in self.world.grid:
            sx = self.offsetx
            if hexgrid and odd:
                sx += self.size // 2
            for cell in row:
                if len(cell.agents) > 0:
                    c = self.getColour(cell.agents[0])
                else:
                    c = self.getColour(cell)
                if c != self.defaultColour:
                    try:
                        self.screen.fill(c,
                                         (sx, sy, self.size, self.size))
                    except TypeError:
                        print(('Error: invalid colour:', c))
                sx += self.size
            odd = not odd
            sy += self.size

    def redrawCell(self, x, y):
        if not self.activated:
            return
        sx = x * self.size + self.offsetx
        sy = y * self.size + self.offsety
        if y % 2 == 1 and self.world.num_dir == 6:
            sx += self.size // 2

        cell = self.world.grid[y][x]
        if len(cell.agents) > 0:
            c = self.getColour(cell.agents[0])
        else:
            c = self.getColour(cell)

        self.screen.fill(c, (sx, sy, self.size, self.size))

    def update(self):
        if not self.activated:
            return
        if self.world.age % self.updateEvery != 0 and not self.paused:
            return
        self.setTitle(self.title)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.onResize(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if self.delay > 0:
                    self.delay -= 1
                else:
                    self.updateEvery *= 2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if self.updateEvery > 1:
                    self.updateEvery //= 2
                else:
                    self.delay += 1
                if self.delay > 10:
                    self.delay = 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
            # display Wealth Distribution
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                WdgWealth.display(self.world.agents, self.world.age)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                WdgSpecs.display(self.world.agents, self.world.age)

        pygame.display.flip()
        if self.delay > 0:
            time.sleep(self.delay * 0.1)

    def setTitle(self, title):
        if not self.activated:
            return
        self.title = title
        title += ' %s' % self.make_title()
        if pygame.display.get_caption()[0] != title:
            pygame.display.set_caption(title)

    def pause(self, event=None):
        self.paused = not self.paused
        while self.paused:
            self.update()

    def onResize(self, event):
        if not self.activated:
            return
        pygame.display.set_mode(event.size, pygame.RESIZABLE, 32)
        oldSize = self.size
        scalew = event.size[0] // self.world.width
        scaleh = event.size[1] // self.world.height
        self.size = min(scalew, scaleh)
        if self.size < 1:
            self.size = 1
        self.redraw()

    def getColour(self, obj):
        c = getattr(obj, 'colour', None)
        if c is None:
            c = getattr(obj, 'color', 'white')
        if isinstance(c, collections.Callable):
            c = c()
        if isinstance(c, type(())):
            if isinstance(c[0], type(0.0)):
                c = (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
            return c
        return pygame.color.Color(c)

    def saveImage(self, filename=None):
        if filename is None:
            filename = 'animations/test/' + '%03d.png' % (self.world.age +
                                                          1)
        pygame.image.save(self.screen, filename)

    def make_title(self):
        text = 'age: %d' % self.world.age
        extra = []
        if self.world.eaten is not None:
            extra.append('eaten=%d' % self.world.eaten)
        if self.world.fed is not None:
            extra.append('fed=%d' % self.world.fed)
        if self.paused:
            extra.append('paused')
        if self.updateEvery != 1:
            extra.append('skip=%d' % self.updateEvery)
        if self.delay > 0:
            extra.append('delay=%d' % self.delay)

        if len(extra) > 0:
            text += ' [%s]' % ', '.join(extra)
        return text
