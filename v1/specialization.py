import time
import random
import shelve

import copy

import pdb

import cellular

from person import *


class Cell(cellular.Cell):
    resources = [MAX_RES_AMOUNT for _ in range(RESOURCE_COUNT)]
    wall = False

    def colour(self):
        if self.wall:
            return 'black'
        elif TO_COLOR_CELLS:
            ratio = sum(self.resources) / \
                (MAX_RES_AMOUNT * RESOURCE_COUNT)
            gradient = hex(int(ratio * 64) + 191)[2:]
            if len(gradient) < 2:
                gradient = '0' + gradient
            return '#ffff' + gradient
        else:
            return '#eeeff7'

    def load(self, data):
        if data == 'X':
            self.wall = True
            self.resources = [0 for _ in range(RESOURCE_COUNT)]
            self.growthRate = [1 for _ in range(RESOURCE_COUNT)]
        else:
            self.wall = False
            self.resources = [
                MAX_RES_AMOUNT for _ in range(RESOURCE_COUNT)]
            self.growthRate = DEF_GROWTH_RATE

    def update(self):
        if TO_UPDATE_CELLS:
            for i in range(RESOURCE_COUNT):
                self.resources[i] += MAX_RES_AMOUNT * self.growthRate[i]
                # normalize
                self.resources[i] = min(self.resources[i], MAX_RES_AMOUNT)


world = cellular.World(
    Cell, directions=8, filename='../worlds/smallbox3.txt')
world.age = 0


def change_growth_rate(x0, y0, x1, y1, newGrowthRate):
    for i in range(x0, x1 + 1):
        for j in range(y0, y1 + 1):
            world.getWrappedCell(i, j).growthRate = newGrowthRate


world.freeID = 0
for _ in range(AGENT_COUNT_INIT):
    world.addAgent(Person(world.freeID), cell=pick_random_location(world))
    world.freeID += 1


def get_indiv_specializations():
    return [agent.get_specialization() for agent in world.agents]


def get_indiv_wealths():
    return [agent.wealth for agent in world.agents]


def get_gini_inequality(wealths=None):
    if wealths is None:
        wealths = sorted(get_indiv_wealths())
    numAgents = len(world.agents)
    G = sum(wealths[i] * (i + 1) for i in range(numAgents))
    G = (2 * G) / (numAgents * sum(wealths))
    return G - (1 + 1 / numAgents)


def get_ave_positions():
    numAgents = len(world.agents)
    if numAgents > 0:
        aveX = sum(agent.cell.x for agent in world.agents) / numAgents
        aveY = sum(agent.cell.y for agent in world.agents) / numAgents
        return aveX, aveY
    else:
        return 10, 10


def get_learning_entropy():
    return sum(agent.ai.aveSRE for agent in world.agents) / \
        len(world.agents)


if TO_DISPLAY_WORLD:
    world.display.activate(size=30)
    world.display.delay = 1

save = ''

endAge = world.age + LEN_TRAINING_AGE
while world.age < endAge:
    world.update()

    #  check progress
    if (world.age + 1) % 100 == 0:
        # world.display.saveImage()
        print(world.age + 1)

    save += str(world.age) + " "
    if OUTPUT_TYPE == 0:
        # Aggregate Output
        save += str(get_learning_entropy()) + " " + str(get_gini_inequality()) + \
            ' ' + str(len(world.agents)) + '\n'
    elif OUTPUT_TYPE == 1:
        # Average Residual Entropy of all agents
        save += str(get_learning_entropy()) + ' ' + str(
            len(world.agents)) + '\n'
    elif OUTPUT_TYPE == 2:
        # Gini's measurement of wealth inequality
        save += str(get_gini_inequality(get_indiv_wealths())) + "\n"
    elif OUTPUT_TYPE == 3:
        # net resources
        save += ' '.join(map(str, get_indiv_wealths())) + "\n"
    elif OUTPUT_TYPE == 4:
        # all specializations
        save += ' '.join(map(str, get_indiv_specializations())) + '\n'
    elif OUTPUT_TYPE == 5:
        # number of agents
        save += str(len(world.agents)) + '\n'
    elif OUTPUT_TYPE == 7:
        # average position
        x, y = get_ave_positions()
        save += str(x) + " " + str(y) + '\n'
    elif OUTPUT_TYPE == 8:
        # net resources
        save += str(sum(get_indiv_wealths())) + '\n'

    if TO_DISPLAY_WORLD and TO_DISPLAY_AVE_POS:
        x, y = get_ave_positions()
        world.display.screen.fill((255, 0, 0),
                                  (30 * x + 5, 30 * y + 5, 20, 20))
        world.display.update()

    if TO_SIMULATE_SEASONS:
        if world.age % 200 == 0:
            change_growth_rate(1, 1, 20, 10, [0] * RESOURCE_COUNT)
            change_growth_rate(1, 11, 20, 20, DEF_GROWTH_RATE)
        elif world.age % 100 == 0:
            change_growth_rate(1, 1, 20, 10, DEF_GROWTH_RATE)
            change_growth_rate(1, 11, 20, 20, [0] * RESOURCE_COUNT)

save += str(world.numDeaths) + ' ' + str(world.cumulativePop) + '\n'

savefile = open(OUTPUT_LOCATION + FILENAMES[OUTPUT_TYPE] + ".txt", 'w')
savefile.write(save)
savefile.close()
