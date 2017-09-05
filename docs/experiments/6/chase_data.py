import numpy as np
import pylab as pl
import copy

# pl.figure(figsize=(10, 10))
runs = 10

for r in range(1, runs+1):
    time = [0]
    data = [[1.0], [1.0]]
    with open(str(r) + "sre.txt") as f:
        temp = [list(map(float, line.split())) for line in f.readlines()]
        for i in range(1000):
            time.append(i+1)
            data[0].append(temp[i][0])
            data[1].append(temp[i][1])
        
    # print(len(data[1]))
    # print(data[1])
        
    plot1 = pl.plot(time, data[0], c='#6677AA')
    plot2 = pl.plot(time, data[1], c='#0000FF')
    
    pl.title('Residual Entropy over Time')

    pl.xlabel('training age')
    pl.ylabel('residual entropy')

    pl.xticks(np.arange(0, 1001+1, 100.0))

    pl.xlim(0, 1001)
    pl.ylim(0.0, 1.0)

    #pl.xticks(np.arange(0, 10000+1, 100))

    pl.tight_layout()
    pl.savefig(str(r) + 'plot-both')
    pl.close()
