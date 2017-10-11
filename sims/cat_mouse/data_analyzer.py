import os
import time
import math

import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures

dir_path = os.path.dirname(os.path.realpath(__file__))


def do_linear_regression(X, Y):
    print("Linear Regression (start):")
    
    lin_reg = LinearRegression(n_jobs=-1)
    lin_reg.fit(X, Y)

    print("  " + str(round(lin_reg.intercept_, 3)) + " + " +
                 str(round(lin_reg.coef_[0], 3)) + "*step + " +
                 str(round(lin_reg.coef_[1], 3)) + "*depth + " +
                 str(round(lin_reg.coef_[2], 3)) + "*alpha + " +
                 str(round(lin_reg.coef_[3], 3)) + "*gamma")

    print("  R-squared:", str(round(lin_reg.score(X, Y), 4)))
    print("Linear Regression (end)")
    print("\n")

    return lin_reg


def do_logistic_regression(X, Y):
    print("Logistic Regression (start):")

    print(len(X))
    log_reg = LogisticRegression(C=1e7,
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

    print("  R-squared:", round(log_reg.score(X, Y), 4))
    X_test = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [100, 1, 0.5, 0.5]]
    Y_test = log_reg.predict(X_test)
    print(Y_test)
    print("Logistic Regression (end):")
    print("\n")

    return log_reg


def do_polynomial_regression(X, Y, degree):
    print("Polynomial Regression (start):")

    print("  Degree of Polynomial:", degree, "\n")

    poly = PolynomialFeatures(degree=degree)
    X_test = [[2, 3, 5, 7]]
    print("  X's original structure:", ' '.join(map(str, X_test[0])))
    print(["1", "x0", "x1", "x2", "x3"])
    Y_test = poly.fit_transform(X_test)
    Y_test = map(int, Y_test[0])
    print("  X's polynomial structure:", ' '.join(map(str, Y_test)))
    print(poly.get_feature_names())
    print()

    model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                     ('linear', LinearRegression(fit_intercept=False))])
    model = model.fit(X, Y)
    coefs = model.named_steps['linear'].coef_
    print("  coefs:", coefs)
    print()

    sign = -1 if coefs[0] < 0 else 1
    a = (abs(coefs[0])) ** (1 / degree)
    denom = sign * degree * a**(degree-1)
    b = coefs[1] / denom
    c = coefs[2] / denom
    d = coefs[3] / denom
    e = coefs[4] / denom

    print("NOTE: the following is note perfect yet")
    print("  perf = (" + str(round(a, degree + 1)) + " + " +
                         str(round(b, degree + 1)) + "*step + " +
                         str(round(c, degree + 1)) + "*depth + " +
                         str(round(d, degree + 1)) + "*alpha + " +
                         str(round(e, degree + 1)) + "*gamma) ^ " +
                    str(degree))

    print("  R-squared:", round(model.score(X, Y), 4))
    print("Polynomial Regression (end)\n")

    return model


def analyze(trials=100, steps=10, runs=10):  # pragma: no cover
    start = time.time()

    X_ave = []
    Y_ave = []

    X_full = []
    Y_full = []

    X_temp = {}

    for depth in range(1, 5):
        for run in range(1, runs + 1):
            dir_input = "data/" + str(depth) + "/data" + str(run) + ".txt"
            with open(os.path.join(dir_path, dir_input)) as f:
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
                        X_full.append(temp)
                        Y_full.append(line[i])

    for key in X_temp:
        X_ave.append(list(key))
        Y_ave.append(X_temp[key] / 10)

    lin_reg = do_linear_regression(X_full, Y_full)
    # log_reg = do_logistic_regression(X, Y)
    pol_reg = do_polynomial_regression(X_full, Y_full, 3)

    print("Tests (start):")
    X_test = [[10, 1, 0, 0], [50, 1, 0.5, 0.5], [100, 1, 1, 1]]
    print("  Params:", X_test)
    print("  Original:   =>", list(X_temp[tuple(x)]/10 for x in X_test))
    print("  Linear:     =>", lin_reg.predict(X_test))
    print("  Polynomial: =>", pol_reg.predict(X_test))
    print("Tests (end)\n")
    print("run time:", time.time() - start, "secs")


if __name__ == '__main__':  # pragma: no cover
    analyze()
