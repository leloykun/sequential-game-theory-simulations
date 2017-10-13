import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures


def linear_regression(X,
                      Y,
                      verbose=False,
                      labels=None,
                      round_to=4):
    n = len(X)

    if verbose:
        print("Linear Regression (start):")

    lin_reg = LinearRegression(n_jobs=-1)
    lin_reg.fit(X, Y)

    coefs = np.concatenate((np.array([lin_reg.intercept_]),
                            np.array(lin_reg.coef_)), axis=0)

    if labels is None:
        labels = ["1"] + ["x%d" % i for i in range(n)]

    func = zip(coefs, labels)

    r_squared = lin_reg.score(X, Y)

    if verbose:
        print("  " + " + ".join(str(term[0]) + "*" + term[1] for term in func))
        print("  R-squared:", round(r_squared, round_to))
        print("Linear Regression (end)\n")

    return lin_reg, coefs, r_squared


def polynomial_regression(X,
                          Y,
                          degree,
                          verbose=False,
                          labels=None,
                          round_to=4):
    n = len(X)

    if verbose:
        print("Polynomial Regression (start):")
        print("  Degree:", degree, "\n")

    model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                     ('linear', LinearRegression(fit_intercept=False))])
    model = model.fit(X, Y)
    coefs = model.named_steps['linear'].coef_

    if labels is None or len(labels) is n:
        labels = model.named_steps['poly'].get_feature_names()

    func = zip(coefs, labels)

    r_squared = model.score(X, Y)

    if verbose:
        print("  " + " + ".join(str(term[0]) + "*" + term[1] for term in func))
        print("  R-squared:", round(r_squared, round_to))
        print("Linear Regression (end)\n")

    return model, coefs, r_squared


if __name__ == '__main__':
    n = 10

    X0 = np.arange(n)
    X1 = np.random.random(n) * n
    X = np.array(list(zip(X0, X1)))
    Y = 5 + 3*X0 + 2*X1 + 4*X0**2 + 3*X0*X1 + X1**2

    print(X0)
    print(X1)
    print(Y)
    print()

    lin_reg, coefs, r_squared = linear_regression(X, Y, verbose=True)
    pol_reg, coefs, r_squared = polynomial_regression(X, Y, 2, verbose=True)

