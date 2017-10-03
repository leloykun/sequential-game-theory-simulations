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
                    X.append([depth, line[0], line[1]])
                    Y.append(line[-1])
    
    clf = linear_model.LinearRegression()
    clf.fit(X, Y)
    
    print(str(clf.intercept_) + " + " + str(clf.coef_[0]) + "*depth + " + str(clf.coef_[1]) + "*learning_rate + " + str(clf.coef_[2]) + "*discount_rate")
    # print(clf.coef_)
    # print(clf.intercept_)

if __name__ == '__main__':
    analyze()
