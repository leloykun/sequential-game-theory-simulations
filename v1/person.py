import random
import copy

import cellular
import qlearn

NEARBY = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]

COLOR_CODE = ['#332532', '#644D52', '#F77A52', '#FF974F', '#A49A87']

ID = 0
RESOURCE_COUNT = 5
MAX_RES_AMOUNT = 100
DEF_GROWTH_RATE = [0.02] * RESOURCE_COUNT  # 0.05
TO_UPDATE_CELLS = True
TO_COLOR_CELLS = True

AGENT_COUNT_INIT = 5
AGENT_COUNT_LIM = 100
AGENTS_CAN_TRADE = True
AGENTS_CAN_DIE = True
AGENTS_CAN_REPRODUCE = True

ENDOWMENT = 100
DEF_RES_INTAKE = 15
TRADING_THRESHOLD = 15
MATING_THRESHOLD = 10 * ENDOWMENT

DEF_SKILLS = 1.00  # 0.75
TO_RANDOMIZE_SKILLS = False
IMPROVE_RATE = 1.00

DEF_TEMP = 5

TO_SIMULATE_SEASONS = True
TO_DISPLAY_WORLD = True
TO_DISPLAY_AVE_POS = True
LEN_TRAINING_AGE = 10000

OUTPUT_LOCATION = "tests/test/"
FILENAMES = [
    'std_out', 'resEnt', 'ineqGini', 'resOfAgents', 'specsOfAgents',
    'numberOfAgents', 'trading', 'avePos', 'netRes'
]
OUTPUT_TYPE = 1


def pick_random_location(world):
    while True:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.getCell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell


class Person(cellular.Agent):
    def __init__(self, _id):
        self.ai = None
        self.ai = qlearn.QLearn(
            actions=list(range(RESOURCE_COUNT)),
            temp=DEF_TEMP,
            alpha=0.25,
            gamma=0.9,
            epsilon=0.1)

        self.lastState = None
        self.lastAction = None

        self.colour = 'gray'
        self.age = 0

        self.id = _id

        self.skillSet = [DEF_SKILLS for _ in range(RESOURCE_COUNT)]
        if TO_RANDOMIZE_SKILLS:
            self.skillSet = [random.random()
                             for _ in range(RESOURCE_COUNT)]
            #self.skillSet = [0.90 + random.random()/10 for _ in range(RESOURCE_COUNT)]

        self.resources = [ENDOWMENT for _ in range(RESOURCE_COUNT)]

        self.wealth = ENDOWMENT * RESOURCE_COUNT
        self.last_wealth = ENDOWMENT * RESOURCE_COUNT

    def update(self, agentType='learning'):
        if agentType == 'learning':
            state = self.calc_state()
            #state = self.calc_state(), self.world.age // 100
            #state = self.calc_state(), (self.world.age % 100) // 5
            #state = self.calc_state(), self.world.age % 100

            reward = self.calc_reward()

            if self.lastState is not None:
                self.ai.learn(self.lastState,
                              self.lastAction, reward, state)

            #state = self.calc_state()
            #state = self.calc_state(), self.world.age // 100
            #state = self.calc_state(), (self.world.age % 100) // 5
            #state = self.calc_state(), self.world.age % 100

            action = self.ai.chooseAction(state, type=1)
            workCell = self.find_best_work_cell(action)

            self.lastState = state
            self.lastAction = action
        elif agentType == 'greedy':
            while True:
                workCells = [(self.find_best_work_cell(a), a)
                             for a in range(RESOURCE_COUNT)]
                workCell, action = workCells[0]
                for cell, a in workCells:
                    if cell.resources[a] > workCell.resources[action]:
                        workCell, action = cell, a
                if not workCell.wall:
                    break
        elif agentType == 'random':
            while True:
                i, j = random.choice(NEARBY)
                workCell = self.world.getWrappedCell(self.cell.x + i,
                                                     self.cell.y + j)
                action = random.choice(list(range(RESOURCE_COUNT)))
                if not workCell.wall and len(workCell.agents) == 0:
                    break

        self.last_wealth = copy.deepcopy(self.wealth)

        self.work(workCell, action)
        self.consume_resources()

        #  color code based on specialization
        self.colour = COLOR_CODE[self.get_specialization()]

        self.age += 1

        if AGENTS_CAN_TRADE:
            self.trade()

        if AGENTS_CAN_DIE and self.meets_death_criteria():
            self.world.removeAgent(self)

        if AGENTS_CAN_REPRODUCE and self.meets_birth_criteria():
            self.world.addAgent(
                Person(self.world.freeID),
                cell=pick_random_location(self.world)
            )
            self.world.freeID += 1
            #  give resources to child (sort of)
            self.consume_resources(amount=100)

    def meets_death_criteria(self):
        return True if self.wealth <= 0 else False

    def meets_birth_criteria(self):
        return len([
            i for i in range(RESOURCE_COUNT)
            if self.resources[i] >= MATING_THRESHOLD
        ]) == RESOURCE_COUNT and len(self.world.agents) <= AGENT_COUNT_LIM

    def get_specialization(self):
        return self.resources.index(max(self.resources))

    def calc_state(self):
        #  totalNumOfStates = 200
        return ([
            self.world.getWrappedCell(self.cell.x + i,
                                      self.cell.y + j).resources[a] // 25
            for a in range(RESOURCE_COUNT)
        ] for i, j in NEARBY)

    def calc_reward(self):
        return self.wealth - self.last_wealth

    def work(self, workCell, action):
        delta = workCell.resources[action] * self.skillSet[action]
        self.wealth += delta
        self.resources[action] += delta
        workCell.resources[action] -= delta

        # transfer
        self.cell = workCell

        self.improve_skills(action)

    def improve_skills(self, action):
        self.skillSet[action] = min(
            self.skillSet[action] * IMPROVE_RATE, 1.0)

    def consume_resources(self, amount=DEF_RES_INTAKE):
        self.resources = [x - amount for x in self.resources]
        self.wealth -= amount * RESOURCE_COUNT

    def find_best_work_cell(self, action, returnAll=False):
        bestCells = [self.cell]
        for i, j in NEARBY:
            cell = self.world.getWrappedCell(
                self.cell.x + i, self.cell.y + j)
            if cell.wall or len(cell.agents) > 0:
                continue
            elif cell.resources[action] > bestCells[0].resources[action]:
                bestCells = [cell]
            elif cell.resources[action] == bestCells[0].resources[action]:
                bestCells.append(cell)
        if returnAll:
            return bestCells
        else:
            return random.choice(bestCells)

    def trade(self):
        for i in range(RESOURCE_COUNT):
            while self.resources[i] < TRADING_THRESHOLD:
                deltaI = TRADING_THRESHOLD - self.resources[i]

                #  find resource to trade
                j = self.resources.index(max(self.resources))

                if self.resources[j] > TRADING_THRESHOLD:
                    delta = min(
                        self.resources[j] - TRADING_THRESHOLD, deltaI)
                else:
                    break

                #  find trade partner
                tradePartner = self.find_trade_partner(i, j, delta)

                if tradePartner is not None:
                    #  exchange
                    self.resources[i] += delta
                    tradePartner.resources[i] -= delta

                    self.resources[j] -= delta
                    tradePartner.resources[j] += delta

                    if OUTPUT_TYPE == 6:
                        global save
                        save += str(world.age) + " " + str(self.id) + " " \
                            + str(tradePartner.id) + \
                            " " + str(delta) + '\n'
                else:
                    break

    def find_trade_partner(self, i, j, delta):
        tradePrio = []
        tradePeeps = []
        for agent in self.world.agents:
            if agent.resources[i] - TRADING_THRESHOLD >= delta:
                if agent.resources[j] < TRADING_THRESHOLD:
                    tradePrio.append(agent)
                else:
                    tradePeeps.append(agent)
        if len(tradePrio) > 0:
            return random.choice(tradePrio)
        elif len(tradePeeps) > 0:
            return random.choice(tradePeeps)
        else:
            return None

    def printStats(self, state):
        print(state)
        print(["{0:0.2f}".format(i) for i in self.skillSet])
