import numpy as np
import pylab as pl

class WdgSpecs():
    @classmethod
    def display(cls, agents, age):
        data = []
        for agent in agents:
            data.append(agent.getSpecialization()+1)
            
        fig, ax = pl.subplots(1,1)
        
        bins = np.arange(1.0, 7.0, 1.0)
        
        ax.hist(data, bins = bins, align = 'left')
        ax.set_xticks(bins[:-1])
        
        pl.title('Number of Specialist per Resource')
        
        pl.xlim(0.5, 5.5)
        #pl.ylim(0, 10)
        
        pl.ylabel('specialists')
        pl.xlabel('resource')
        
        pl.figtext(0.15, 0.85, 'age: ' + str(age))
        
        pl.show()