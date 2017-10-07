import numpy as np
import pylab as pl


class WdgWealth():
    @classmethod
    def display(cls, agents, age):
        data = []
        for agent in agents:
            data.append(agent.wealth)
        pl.hist(data)

        pl.title('Wealth Distribution of Agents')

        pl.ylabel('number of agents agents')
        pl.xlabel('amount of resources')

        pl.figtext(0.15, 0.85, 'age: ' + str(age))

        pl.show()
