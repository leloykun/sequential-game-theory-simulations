import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import seaborn as sns
sns.set()

from IPython.display import HTML
import ffmpy

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from collections import namedtuple
ArrayStats = namedtuple('ArrayStats', 'min ave max range')


def get_stats(X):
    '''
    Calculate the minimum, average,
    maximum, and range of an ndarray

    Example
    -------
    Input: (X=[1, 2, 3, 4, 5])
    Output: ArrayStats(min=1, ave=3, max=5, range=4)

    Parameters
    ----------
    X : ndarray
        The ndarray to be processed

    Returns
    -------
    ArrayStats
        A named tuple of the form (min, ave, max, range)
    '''
    xmin = np.amin(X)
    xmax = np.amax(X)
    return ArrayStats(xmin, sum(X.flatten()) / X.size, xmax, xmax - xmin)


def normalize(X, stats, invert=False):
    '''
    Normalize the values of an ndarray
    to the range [0, 1] based on the
    stats of the trainer ndarray.

    Invert the result when invert == True

    Example
    -------
    Input: (X=[1, 2, 3, 4, 5], stats=(1, 3, 5, 4), invert=True)
    Output: [1.00, 0.75, 0.50, 0.25, 0.00]

    Parameters
    ----------
    X : ndarray
        The ndarray to be normalized
    stats: ArrayStats
        The stats of the trainer ndarray
    invert: bool, optional
        Option to invert the result

    Returns
    -------
    ndarray
        The normalized ndarray X
    '''
    X = (X - stats.min) / stats.range
    return 1 - X if invert else X


def gif_to_mp4(file, fps):
    '''
    Create an mp4 version of the
    inputted gif in the same directory

    Parameters
    ----------
    file : string
        The filename of the gif to be converted
    fps : int
        The number of frames per second of the output mp4
    '''
    ff = ffmpy.FFmpeg(inputs={'%s.gif' % file: '-y -r %d' % fps},
                      outputs={'%s.mp4' % file: None})
    ff.run()


def plot_dist(X, ax, file_name,
              hist=False, shade=True,
              xticks=None, yticks=None):
    '''
    Plots the distribution of
    the values of an ndarray

    Parameters
    ----------
    X : ndarray
        The ndarray to be plotted
    ax : AxesSubplot
        The axes to be plotted in
    file_name: str
        The filename of the output images
    hist : bool, optional
        Option to show the histogram, by default 'False'
    shade : bool, optional
        Option to shade the distribution plot, by default 'True'
    xticks : array_like, optional
        The xticks of the axes, by default 'None'.
        If 'None' the xticks of the axes are set to the defaults
    yticks : array_like, optional
        The yticks of the axes, by default 'None'.
        If 'None' the yticks of the axes are set to the defaults

    Returns
    -------
    HTML
        The HTML format of the saved image
    '''
    ax = sns.distplot(X,
                      hist=hist,
                      color="b",
                      kde_kws={"shade": shade},
                      ax=ax)

    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    plt.tight_layout()
    plt.savefig("%s.png" % file_name, transparent=True)

    return HTML('<img src="%s.png">' % file_name)


class PolynomialRegression:
    X = []
    Y = []

    X_flat = []
    Y_flat = []

    Y_pred = []

    labels = []
    n_params = 1
    dim = 10

    def __init__(self, X, Y, degree=None, labels=None, ravel=True):
        self.X = np.copy(X)
        self.Y = np.copy(Y)

        self.n_params = len(self.X)
        self.degree = degree
        self.dim = len(self.X[0])
        PolynomialRegression.dim = self.dim

        self.labels = labels

        if ravel:
            self.X_flat = np.column_stack(tuple(self.X[i].ravel()
                                          for i in range(self.n_params)))
            self.Y_flat = self.Y.ravel()
        else:
            self.X_flat = np.copy(X)
            self.Y_flat = np.copy(Y)

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

    def plot(self, ax, idx=(0, 1), X=None, Y=None, Z=None,
             plot_type='surface', alpha=0.5,
             show_contours=True, cmap=plt.cm.coolwarm,
             tight=False, lims=((-2, 10), (0, 12), (0, 10000)),
             show_labels=False, labels=("X0", "X1", "Y"),
             title=None):
        if X is None:
            X = self.X[idx[0]]
        if Y is None:
            Y = self.X[idx[1]]
        if Z is None:
            Z = self.Y if self.Y_pred == [] else self.Y_pred

        if plot_type == 'wireframe':
            p = ax.plot_wireframe(X, Y, Z,
                                  rstride=self.dim//10,
                                  cstride=self.dim//10,
                                  alpha=alpha)
        elif plot_type == 'surface':
            p = ax.plot_surface(X, Y, Z,
                                rstride=self.dim//10,
                                cstride=self.dim//10,
                                alpha=alpha)

        if show_contours:
            cset = ax.contour(X, Y, Z,
                              zdir='x',
                              offset=lims[0][1],
                              cmap=cmap)
            cset = ax.contour(X, Y, Z,
                              zdir='y',
                              offset=lims[1][1],
                              cmap=cmap)
            cset = ax.contour(X, Y, Z,
                              zdir='z',
                              offset=lims[2][0],
                              cmap=cmap)

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
