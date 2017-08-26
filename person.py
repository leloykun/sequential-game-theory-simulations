import random
import copy

import cellular
import qlearn
import settings

def pick_random_location(world):
    while True:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.getCell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell


class Person(cellular.Agent):
    def __init__(self, _id=0):
        self.ai = None
        self.ai = qlearn.QLearn(
            actions = list(range(settings.RESOURCE_COUNT)),
            temp    = settings.DEF_TEMP,
            alpha   = 0.25,
            gamma   = 0.9,
            epsilon = 0.1)
            
        self.lastState  = None
        self.lastAction = None

        self.colour = 'gray'
        self.age    = 0

        self.ID     = _id

        self.skillSet = [settings.DEF_SKILLS for _ in range(settings.RESOURCE_COUNT)]
        if settings.TO_RANDOMIZE_SKILLS:
            self.skillSet = [random.random() for _ in range(settings.RESOURCE_COUNT)]
            #self.skillSet = [0.90 + random.random()/10 for _ in range(settings.RESOURCE_COUNT)]

        self.resources = [settings.ENDOWMENT for _ in range(settings.RESOURCE_COUNT)]

        self.wealth = settings.ENDOWMENT * settings.RESOURCE_COUNT
        self.last_wealth = settings.ENDOWMENT * settings.RESOURCE_COUNT

    def update(self, agentType='learning'):
        if agentType == 'learning':
            state = self.calc_state()
            #state = self.calc_state(), self.world.age // 100
            #state = self.calc_state(), (self.world.age % 100) // 5
            #state = self.calc_state(), self.world.age % 100

            reward = self.calc_reward()

            if self.lastState is not None:
                self.ai.learn(self.lastState, self.lastAction, reward, state)

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
                             for a in range(settings.RESOURCE_COUNT)]
                workCell, action = workCells[0]
                for cell, a in workCells:
                    if cell.resources[a] > workCell.resources[action]:
                        workCell, action = cell, a
                if not workCell.wall:
                    break
        elif agentType == 'random':
            while True:
                i, j = random.choice(settings.NEARBY)
                workCell = self.world.getWrappedCell(self.cell.x + i,
                                                     self.cell.y + j)
                action = random.choice(list(range(settings.RESOURCE_COUNT)))
                if not workCell.wall and len(workCell.agents) == 0:
                    break

        self.last_wealth = copy.deepcopy(self.wealth)

        self.work(workCell, action)
        self.consume_resources()

        #  color code based on specialization
        self.colour = settings.COLOR_CODE[self.get_specialization()]

        self.age += 1

        if settings.AGENTS_CAN_TRADE:
            self.trade()

        if settings.AGENTS_CAN_DIE and self.meets_death_criteria():
            self.world.removeAgent(self)

        if settings.AGENTS_CAN_REPRODUCE and self.meets_birth_criteria():
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
            i for i in range(settings.RESOURCE_COUNT)
            if self.resources[i] >= settings.MATING_THRESHOLD
        ]) == settings.RESOURCE_COUNT and len(self.world.agents) <= settings.AGENT_COUNT_LIM

    def get_specialization(self):
        return self.resources.index(max(self.resources))

    def calc_state(self):
        #  totalNumOfStates = 200
        return ([
            self.world.getWrappedCell(self.cell.x + i,
                                      self.cell.y + j).resources[a] // 25
            for a in range(settings.RESOURCE_COUNT)
        ] for i, j in settings.NEARBY)

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
        self.skillSet[action] = min(self.skillSet[action] * settings.IMPROVE_RATE, 1.0)

    def consume_resources(self, amount=settings.DEF_RES_INTAKE):
        self.resources = [x - amount for x in self.resources]
        self.wealth -= amount * settings.RESOURCE_COUNT

    def find_best_work_cell(self, action, returnAll=False):
        bestCells = [self.cell]
        for i, j in settings.NEARBY:
            cell = self.world.getWrappedCell(self.cell.x + i, self.cell.y + j)
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
        for i in range(settings.RESOURCE_COUNT):
            while self.resources[i] < settings.AGENTS_CAN_REPRODUCE:
                deltaI = settings.AGENTS_CAN_REPRODUCE - self.resources[i]

                #  find resource to trade
                j = self.resources.index(max(self.resources))

                if self.resources[j] > settings.AGENTS_CAN_REPRODUCE:
                    delta = min(self.resources[j] - settings.AGENTS_CAN_REPRODUCE, deltaI)
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

                    if settings.OUTPUT_TYPE == 6:
                        global save
                        save += str(world.age) + " " + str(self.ID) + " " \
                              + str(tradePartner.settings.ID) + " " + str(delta) + '\n'
                else:
                    break

    def find_trade_partner(self, i, j, delta):
        tradePrio = []
        tradePeeps = []
        for agent in self.world.agents:
            if agent.resources[i] - settings.AGENTS_CAN_REPRODUCE >= delta:
                if agent.resources[j] < settings.AGENTS_CAN_REPRODUCE:
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
