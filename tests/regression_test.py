import numpy as np

from ..src.data.analysis_tools import linear_regression
from ..src.data.analysis_tools import polynomial_regression


eps = 1e-10


def test_regression_models():
    n = 10

    X0 = np.arange(n)
    X1 = np.random.random(n) * n
    X = np.array(list(zip(X0, X1)))
    Y = 5 + 3*X0 + 2*X1 + 4*X0**2 + 3*X0*X1 + X1**2

    lin_reg, coefs, r_squared = linear_regression(X, Y, verbose=True)
    pol_reg, coefs, r_squared = polynomial_regression(X, Y, 2, verbose=True)

    assert abs(coefs[0] - 5.0) < eps
    assert abs(coefs[1] - 3.0) < eps
    assert abs(coefs[2] - 2.0) < eps
    assert abs(coefs[3] - 4.0) < eps
    assert abs(coefs[4] - 3.0) < eps
    assert abs(coefs[5] - 1.0) < eps


if __name__ == '__main__':
    test_linear_regression()
