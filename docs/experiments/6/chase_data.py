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

    '''num_states = []
    with open(str(r) + "states.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            # print(line)
            if line[0] == "states:":
                num_states.append(int(line[1]))
    for xc in range(1, 1000):
        if num_states[xc] != num_states[xc - 1]:
            pl.axvline(x=xc, color='pink', linestyle='-', linewidth=1)'''

    #plot1 = pl.plot(time, data[0], c='#6677AA')
    plot2 = pl.plot(time, data[1], c='#0000FF')

    pl.title('Residual Entropy over Time')

    pl.xlabel('Time')
    pl.ylabel('Residual Entropy')

    pl.xticks(np.arange(0, 1001+1, 100.0))

    pl.xlim(0, 1001)
    pl.ylim(0.0, 1.0)

    pl.tight_layout()
    pl.savefig(str(r) + 'plot')
    pl.close()
