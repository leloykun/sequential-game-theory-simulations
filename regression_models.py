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

    coefs = [lin_reg.intercept_] + lin_reg.coef_
    if labels is None:
        labels = ["1"] + ["x%d" % i for i in range(n)]
    func = zip(coefs, labels)

    r_squared = lin_reg.score(X, Y)

    if verbose:
        print("  " + " + ".join(str(term[0]) + "*" + term[1] for term in func))
        print("  R-squared:", round(r_squared, round_to))
        print("Linear Regression (end)\n")

    return lin_reg, coefs, r_squared
