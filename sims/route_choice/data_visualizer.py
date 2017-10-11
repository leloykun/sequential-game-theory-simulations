import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))


def visualize(runs=10):
    for run in range(1, runs + 1):
        data = [[], [], [], []]
        time = []

        dir_input = 'data/dis/' + str(run) + 'run.txt'
        with open(os.path.join(dir_path, dir_input)) as f:
            for line in f.readlines():
                a, b, c, d = map(int, line.split())
                time.append(len(time) + 1)
                data[0].append(a)
                data[1].append(b)
                data[2].append(c)
                data[3].append(d)

        _, ax = plt.subplots()

        plt.xlim(1, 1000)
        plt.ylim(1, 50)

        time = np.array(time)
        for i in range(4):
            sns.regplot(x=time[:1000],
                        y=np.array(data[i][:1000]),
                        ax=ax,
                        ci=100,
                        marker="+",
                        n_boot=10000,
                        scatter=False)

        dir_output = 'data/dis/' + str(run) + 'plot1K.png'
        plt.savefig(os.path.join(dir_path, dir_output))
        plt.close()
        print("done with run %d" % run)


if __name__ == '__main__':  # pragma: no cover
    visualize()
