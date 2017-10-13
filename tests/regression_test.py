import numpy as np

from ..regression_models import linear_regression


eps = 1e-10


def test_linear_regression():
    X0 = np.arange(100)
    X1 = np.random.random(100)
    X = np.array(list(zip(X0, X1)))
    Y = 3*X0 + X1

    lin_reg, coefs, r_squared = linear_regression(X, Y)

    assert len(coefs) == 3
    assert abs(coefs[0] - 0.0) < eps
    assert abs(coefs[1] - 3.0) < eps
    assert abs(coefs[2] - 1.0) < eps
    print(coefs)


if __name__ == '__main__':
    test_linear_regression()