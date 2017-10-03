import numpy as np
import pylab as pl
import copy
import seaborn as sns

# pl.figure(figsize=(10, 10))
runs = 10
temp_powers = 5

for temp_power in range(-temp_powers, temp_powers + 1):
    for r in range(1, runs+1):
        time = [0]
        data = [[1.0], [1.0]]
        with open('data/' + str(temp_power) + '/' + str(r) + "res_ent.txt") as f:
            temp = [list(map(float, line.split())) for line in f.readlines()]
            for i in range(1000):
                time.append(i+1)
                data[0].append(temp[i][0])
                data[1].append(temp[i][1])

        num_states = []
        with open('data/' + str(temp_power) + '/' + str(r) + "num_states.txt") as f:
            num_states = list(map(int, f.readline().split()))
        for xc in range(1, 1000):
            if num_states[xc] != num_states[xc - 1]:
                pl.axvline(x=xc, color='pink', linestyle='-', linewidth=1)

        plot1 = pl.plot(time, data[0], c='#6677AA')
        plot2 = pl.plot(time, data[1], c='#0000FF')

        pl.title('Residual Entropy over Time')

        pl.xlabel('Time')
        pl.ylabel('Residual Entropy')

        pl.xticks(np.arange(0, 1001+1, 100.0))

        pl.xlim(0, 1001)
        pl.ylim(0.0, 1.0)

        pl.tight_layout()
        pl.savefig('data/' + str(temp_power) + '/' + str(r) + 'plot')
        pl.close()
