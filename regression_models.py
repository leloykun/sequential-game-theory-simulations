import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class PolynomialRegression:
    X = []
    Y = []
    Y_pred = []
    labels = []
    n_params = 1
    dim = 10

    def __init__(self, X, Y, degree=None, labels=None, ravel=True):
        self.X = X
        self.Y = Y

        self.n_params = len(X)
        self.degree = degree
        self.dim = len(self.X[0])
        PolynomialRegression.dim = self.dim

        self.labels = labels

        if ravel:
            self.X_flat = np.column_stack(tuple(X[i].ravel() for i in range(self.n_params)))
            self.Y_flat = Y.ravel()
        else:
            self.X_flat = X
            self.Y_flat = Y

        if degree is not None:
            self.regress(degree)
            self.Y_pred = self.predict()

    def regress(self, degree=2):
        self.model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                               ('linear', LinearRegression(fit_intercept=False))])
        self.model.fit(self.X_flat, self.Y_flat)
        self.r_squared = self.model.score(self.X_flat, self.Y_flat)

        self.powers = self.model.named_steps['poly'].powers_

        self.coefs = self.model.named_steps['linear'].coef_
        self.labels = self.calc_labels()
        self.func = zip(self.coefs, self.labels)

    def calc_labels(self):
        labels = self.model.named_steps['poly'].get_feature_names()
        return ['*'.join(label.split()) for label in labels]

    def print_func(self):
        print(' + '.join("%lf*%s" % nomial for nomial in self.func))

    def process(self, degree=None):
        if degree not in [self.degree, None]:
            self.degree = degree
            self.regress(degree)

            self.Y_pred = self.predict()

        return self

    def predict(self, X=None):
        if X is None:
            X = self.X

        Y_pred = np.zeros((self.dim, self.dim))
        for power in range(len(self.powers)):
            nomial = self.coefs[power]
            for i in range(self.n_params):
                nomial *= X[i] ** self.powers[power][i]
            Y_pred += nomial

        return Y_pred

    @classmethod
    def plot(cls, ax, X=None, Y=None, Z=None, idx=(0, 1),
             wireframe=False, alpha=0.5,
             show_contours=True,
             tight=False, lims=((-2, 10), (0, 12), (0, 10000)),
             show_labels=False, labels=("X0", "X1", "Y"),
             title=None):
        if X is None:
            X = cls.X[idx[0]]
        if Y is None:
            Y = cls.X[idx[1]]
        if Z is None:
            Z = cls.Y if cls.Y_pred == [] else cls.Y_pred

        if wireframe:
            p = ax.plot_wireframe(X, Y, Z,
                                  rstride=cls.dim//10,
                                  cstride=cls.dim//10,
                                  alpha=alpha)
        else:
            p = ax.plot_surface(X, Y, Z,
                                rstride=cls.dim//10,
                                cstride=cls.dim//10,
                                alpha=alpha)

        if show_contours:
            cset = ax.contour(X, Y, Z,
                              zdir='x',
                              offset=lims[0][0],
                              cmap=plt.cm.coolwarm)
            cset = ax.contour(X, Y, Z,
                              zdir='y',
                              offset=lims[1][1],
                              cmap=plt.cm.coolwarm)
            cset = ax.contour(X, Y, Z,
                              zdir='z',
                              offset=lims[2][0],
                              cmap=plt.cm.coolwarm)

        if not tight:
            ax.set_xlim3d(lims[0][0], lims[0][1]);
            ax.set_ylim3d(lims[1][0], lims[1][1]);
            ax.set_zlim3d(lims[2][0], lims[2][1]);
        
        if show_labels:
            ax.set_xlabel(labels[0])
            ax.set_ylabel(labels[1])
            ax.set_zlabel(labels[2])

        if title is not None:
            t = plt.title(title)

        return p


def linear_regression(X, Y, verbose=False, labels=None, round_to=4):
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
        print("  " + " + ".join(str(term[0]) + "*" + term[1] for term in func), "\n")
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
        labels = ['*'.join(label.split()) for label in labels]

    func = zip(coefs, labels)

    r_squared = model.score(X, Y)

    if verbose:
        print("  " + " + ".join(str(term[0]) + "*" + term[1] for term in func), "\n")
        print("  R-squared:", round(r_squared, round_to))
        print("Polynomial Regression (end)\n")

    return model, coefs, r_squared
