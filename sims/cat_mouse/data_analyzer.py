import time
from sklearn import linear_model


def analyze(trials=100, steps=10, runs=10):
    start = time.time()

    X = []
    Y = []

    X_temp = {}

    for depth in range(1, 5):
        for run in range(1, runs + 1):
            with open("data/" + str(depth) + "/data" + str(run) + ".txt") as f:
                for line in f.readlines():
                    line = list(map(int, line.split()))
                    for i in range(2, 12):
                        temp = ((i - 1) * steps,
                                depth,
                                line[0] / 10,
                                line[1] / 10)
                        if temp in X_temp:
                            X_temp[temp] += line[i]
                        else:
                            X_temp[temp] = line[i]

    for key in X_temp:
        X.append(list(key))
        Y.append(int(X_temp[key] / 10))

    lin_reg = linear_model.LinearRegression(n_jobs=-1)
    lin_reg.fit(X, Y)

    print(str(round(lin_reg.intercept_, 2)) + " + " +
          str(round(lin_reg.coef_[0], 2)) + "*step + " +
          str(round(lin_reg.coef_[1], 2)) + "*depth + " +
          str(round(lin_reg.coef_[2], 2)) + "*alpha + " +
          str(round(lin_reg.coef_[3], 2)) + "*gamma")

    print("R-squared:", str(round(lin_reg.score(X, Y), 4)))
    print()

    print(len(X))
    log_reg = linear_model.LogisticRegression(C=1e7,
                                              tol=1e-5,
                                              max_iter=100,
                                              class_weight='balanced')
    log_reg.fit(X, Y)
    print()

    with open('data/coef.txt', 'w') as f:
        f.write('\n'.join(' '.join(map(str, line))
                          for line in log_reg.coef_))
    with open('data/intercept.txt', 'w') as f:
        f.write(' '.join(map(str, log_reg.intercept_)))
    with open('data/r-squared.txt', 'w') as f:
        f.write(str(log_reg.score(X, Y)))

    print("R-squared:", round(log_reg.score(X, Y), 4))
    X_test = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [100, 1, 0.5, 0.5]]
    Y_test = log_reg.predict(X_test)
    print(Y_test)

    print("time taken:", time.time() - start)


if __name__ == '__main__':
    analyze()
