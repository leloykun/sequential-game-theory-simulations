import time
from sklearn import linear_model

def analyze(trials=100, steps=10, runs=10):
    layers = int(trials / steps)
    X = []
    Y = []

    for depth in range(1, 5):
        for run in range(1, runs + 1):
            with open("data/" + str(depth) + "/data" + str(run) + ".txt") as f:
                for line in f.readlines():
                    line = list(map(int, line.split()))
                    for i in range(2, 12):
                        X.append([(i - 1) * steps, depth, line[0]/10, line[1]/10])
                        Y.append(line[i])

    clf = linear_model.LinearRegression(n_jobs=-1)
    clf.fit(X, Y)

    print(str(round(clf.intercept_, 2)) + " + " + \
          str(round(clf.coef_[0], 2)) + "*step + " + \
          str(round(clf.coef_[1], 2)) + "*depth + " + \
          str(round(clf.coef_[2], 2)) + "*alpha + " + \
          str(round(clf.coef_[3], 2)) + "*gamma")

    print("R-squared:", str(round(clf.score(X, Y), 4)))

if __name__ == '__main__':
    analyze()
