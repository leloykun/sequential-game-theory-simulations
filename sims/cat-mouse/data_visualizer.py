import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

max_perf = 150
bounds = [i for i in range(0, max_perf + 1)]


def visualize(trials=100, steps=10, runs=10):
    layers = int(trials / steps)

    for depth in range(1, 5):
        start = time.time()

        data = [[[0 for layer in range(layers)]
                    for _ in range(11)] 
                    for _ in range(11)]
        for i in range(1, runs + 1):
            with open("data/" + str(depth) + "/data" + str(i) + ".txt") as f:
                temp = f.readlines()
                for line in temp:
                    alpha, gamma, *fed = map(int, line.split())
                    for layer in range(layers):
                        data[alpha][gamma][layer] += fed[layer] / runs

        for layer in range(layers):
            temp = [[0 for _ in range(11)] for _ in range(11)]
            for alpha in range(11):
                for gamma in range(11):
                    temp[alpha][gamma] = max_perf - (data[alpha][gamma][layer] - (
                        data[alpha][gamma][layer - 1] if layer > 0 else 0)) / steps

            plt.imshow(temp,
                       extent=[-0.5, 10.5, -0.5, 10.5],
                       origin='lower',
                       interpolation='nearest',
                       vmin=0,
                       vmax=max_perf,
                       cmap=sns.light_palette("Navy", as_cmap=True))

            plt.title("QLearning Parameters vs. Agent Performance\nVisual Depth = " +
                      str(depth) + " || Training Period: " + str(layer + 1))
            plt.xlabel("Discount Rate")
            plt.ylabel("Learning Rate")

            plt.colorbar(boundaries=bounds,
                         spacing='uniform',
                         label='Agent Performance',
                         ticks=[],
                         extend='max')
            plt.tight_layout()
            plt.savefig("data/" + str(depth) + "/plot" + str(layer + 1))
            plt.close()

        print("visual depth", depth, "run time:", time.time() - start)


if __name__ == '__main__':
    trials, steps, runs = map(int, input("params: ").split())
    visualize()
