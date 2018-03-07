import os
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
    '''  Calculates statistics of an ndarray

    Calculates the minimum, mean,
    maximum, and range of an ndarray

    Parameters
    ----------
    X : ndarray
        The ndarray to be processed

    Returns
    -------
    ArrayStats
        A named tuple of the form (min, ave, max, range)

    Examples
    --------
    >>> get_stats(X=np.linspace(1, 5, 5))
    ArrayStats(min=1.0, ave=3.0, max=5.0, range=4.0)
    '''
    xmin = np.amin(X)
    xmax = np.amax(X)
    return ArrayStats(xmin, sum(X.flatten()) / X.size, xmax, xmax - xmin)


def normalize(X, stats, invert=False):
    '''  Normalizes an ndarray to the range [0, 1]

    Normalizes the values of an ndarray
    to the range [0, 1] based on the
    stats of the trainer ndarray.

    Inverts the result when invert == True

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

    Examples
    --------
    >>> X = np.linspace(1, 5, 5)
    >>> normalize(X=X, stats=get_stats(X))
    [0.00 0.25 0.50 0.75 1.00]
    >>> normalize(X=X, stats=get_stats(X), invert=True)
    [1.00 0.75 0.50 0.25 0.00]
    '''
    X = (X - stats.min) / stats.range
    return 1 - X if invert else X


def gif_to_mp4(file, fps):
    '''  converts a gif into an mp4

    Creates an mp4 version of the
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


def plot_dist(X,
              ax,
              file_name,
              hist=False,
              shade=True,
              xticks=None,
              yticks=None):
    '''  Plots the distribution of the values of an ndarray

    Parameters
    ----------
    X : ndarray
        The ndarray to be plotted
    ax : AxesSubplot
        The axis to be plotted in
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


def animate(input_files, output_file, fps=1, vid=True):
    '''  Generates an animation from the given frames

    Generates an animation from the frames in the 'input_files'

    Parameters
    ----------
    input_files : str
        The format of the frames
    output_file : str
        The name of the output file
    fps : int, optional
        The number of frames per second of the animation,
        by default '1'
    vid : bool, optional
        Option wether to use mp4 or gif,
        by default 'True' or by using mp4

    Returns
    -------
    {HTML<video>, HTML<img>}
        The HTML format of the output file
    '''
    if vid:
        os.system("ffmpeg -r {} -i {}%03d.png -codec:v mpeg4 -y {}_viewable.mp4".format(fps, input_files, output_file))
        os.system("ffmpeg -r {} -i {}%03d.png -y {}.mp4".format(fps, input_files, output_file))
        return HTML('<video controls autoplay loop> <source src="{}.mp4" type="video/mp4"> </video>'.format(output_file))
    else:
        images = []
        for step in range(1, num_steps + 1):
            images.append(imageio.imread("{}{:03d}.png".format(input_files, step)))
        imageio.mimsave("{}.gif".format(output_file), images, fps=fps)
        return HTML('<img src="{}.gif">'.format(output_file))


def heatmap_preprocess(X,
                       save_file,
                       num_steps,
                       vmin=0.0,
                       vmax=1.0):
    '''  plots an animated heatmap into separate frames

    Parameters
    ----------
    X : ndarray
        The ndarray to be plotted
    save_file_format : str
        The format of the save files of the frames
    num_steps : int
        The number of steps or frames in the animation
    vmin : float, optional
        The minimum of the range of the plot
    vmax : float, optional
        The maximum of the range of the plot
    '''
    for step in range(1, num_steps + 1):
        fig, axes = plt.subplots(2, 3, figsize=(6.3, 6), gridspec_kw={'width_ratios':[1, 1, 0.1], 'height_ratios':[1, 1]})

        for i in range(2):
            for j in range(2):
                ax = sns.heatmap(X[2*i + j + 1][step],
                                 vmin=vmin, vmax=vmax,
                                 cmap=sns.color_palette("Blues", n_colors=100),
                                 ax=axes[i][j],
                                 cbar=False)

                if i == 1:
                    ax.set_xticks(np.linspace(0, 10, 6) + .5)
                    ax.set_xticklabels(np.linspace(0, 1, 6))
                else:
                    ax.set_xticks([])

                if j == 0:
                    ax.set_yticks(np.linspace(0, 10, 6) + 0.8)
                    ax.set_yticklabels(np.linspace(0, 1, 6))
                else:
                    ax.set_yticks([])

                ax.set_xlabel('')
                ax.set_ylabel('')

                ax.invert_yaxis()

        mappable = axes[0][0].get_children()[0]
        plt.colorbar(mappable, ax=axes, orientation='vertical', ticks=[], cax=axes[0][2], extend='max');
        plt.colorbar(mappable, ax=axes, orientation='vertical', ticks=[], cax=axes[1][2], extend='max');

        # plt.suptitle(\"{}\".format(step))

        plt.tight_layout()
        plt.savefig(save_file.format(step), transparent=True)
        plt.close()


def plot_3d_rotate(ax, save_file, degree):
    '''  rotates a 3d graph and saves each frame

    Parameters
    ----------
    ax : Axes3D
        The axes to be processed
    save_file : str
        The format of the save files of the frames
    degree : int
        The degree of the polynomial estimate. Only used for output
    '''
    for ii in range(0, 360, 1):
        ax.view_init(elev=30., azim=ii)
        plt.savefig(save_file.format(degree, ii), transparent=True)


def plot_3d_normed(model, degree, offsets=(1.5, 1.5, 0.0),
                   lims=((0.0, 1.5), (0.0, 1.5), (0.0, 1.5)),
                   cmap=plt.cm.coolwarm):
    '''  plots an animated heatmap into separate frames

    Parameters
    ----------
    model : PolynomialRegression
        
    degree : int
        
    offsets : tuple, optional
        

    Returns
    -------
    ax : Axes3D
        
    '''
    fig = plt.figure(figsize=(8.6, 8.6))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    p = model.plot(ax,
                   idx=(2, 3),
                   Z=model.Y, plot_type='wireframe',
                   show_contours=False,
                   cmap=cmap)
    q = model.plot(ax,
                   idx=(2, 3),
                   Z=model.process(degree=degree).predict(), 
                   lims=lims,
                   offsets=offsets,
                   show_labels=True,
                   labels=("Learning Rate",
                           "Discount Rate",
                           "Agent Performance"),
                   cmap=cmap)

    # formatter = ticker.ScalarFormatter(useMathText=True)
    # formatter.set_scientific(True) 
    # formatter.set_powerlimits((-1,1)) 
    # ax.zaxis.set_major_formatter(formatter)

    ax.set_xticks([])
    ax.set_yticks([])
    #ax.set_xticks(np.linspace(0, 1, 6))
    #ax.set_yticks(np.linspace(0, 1, 6))
    ax.set_zticks([lims[2][0], lims[2][1]])
    ax.set_zticklabels(['low', 'high'])
    
    # ax.invert_xaxis()
    # ax.invert_yaxis()
    # ax.invert_zaxis()

    fig.patch.set_alpha(0.)
    ax.patch.set_alpha(0.0)
    ax.grid(False)
    
    return ax


class PolynomialRegression:
    '''
    
    '''

    def __init__(self, X, Y, degree=None, labels=None):
        '''
        
        Parameters
        ----------
        X : ndarray
            
        Y : ndarray
            
        degree : int, optional
            
        labels : list_like, optional
            
        '''
        self.X = np.copy(X)
        self.Y = np.copy(Y)

        self.degree = degree

        self.n_params = len(self.X)
        self.dim = len(self.X[0])
        self.labels = labels

        self.X_flat = np.column_stack(tuple(self.X[i].ravel()
                                      for i in range(self.n_params)))
        self.Y_flat = self.Y.ravel()

        if degree is not None:
            self.regress(degree)
            self.Y_pred = self.predict()

    def regress(self, degree=2):
        '''
        
        Parameters
        ----------
        degree : int, optional
            
        '''
        self.model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                               ('linear', LinearRegression(fit_intercept=False))])
        self.model.fit(self.X_flat, self.Y_flat)
        self.r_squared = self.model.score(self.X_flat, self.Y_flat)

        self.powers = self.model.named_steps['poly'].powers_

        self.coefs = self.model.named_steps['linear'].coef_
        self.labels = self.calc_labels()
        self.func = zip(self.coefs, self.labels)

    def calc_labels(self):
        '''
        
        Returns
        -------
        list
            
        '''
        labels = self.model.named_steps['poly'].get_feature_names()
        return ['*'.join(label.split()) for label in labels]

    def print_func(self):
        '''
        
        '''
        print(' + '.join("%lf*%s" % nomial for nomial in self.func))

    def process(self, degree=None):
        '''
        Parameters
        ----------
        degree : int, optional
            
        
        Returns
        -------
        obj: PolynomialRegression
            
        '''
        if degree not in [self.degree, None]:
            self.degree = degree
            self.regress(degree)

            self.Y_pred = self.predict()

        return self

    def predict(self, X=None):
        '''
        
        Parameters
        ----------
        X : ndarray, optional
            
        
        Returns
        -------
        ndarray
            
        '''
        if X is None:
            X = self.X

        Y_pred = np.zeros(X[0].shape)
        for power in range(len(self.powers)):
            nomial = self.coefs[power]
            for i in range(self.n_params):
                nomial *= X[i] ** self.powers[power][i]
            Y_pred += nomial

        return Y_pred

    def plot(self, ax, idx=(0, 1), X=None, Y=None, Z=None,
             plot_type='surface', alpha=0.5,
             show_contours=True, cmap=plt.cm.coolwarm,
             tight=False, lims=((0.0, 1.5), (0.0, 1.5), (0, 1)),
             offsets=(1.5, 1.5, 0),
             show_labels=False, labels=("X0", "X1", "Y"),
             title=None):
        '''
        
        Parameters
        ----------
        ax : Axes3D
            
        idx : tuple of int, optional
            
        X : ndarray, optional
            
        Y : ndarray, optional
            
        Z : ndarray, optional
            
        plot_type : str, optional
            
        alpha : float, optional
            
        show_contours : bool, optional
            
        cmap : matplotlib.cm, optional
            
        tight : bool, optional
            
        lims : tuple of tuple of float, optional
            
        offsets : tuple of float, optional
            
        show_labels : bool, optional
            
        labels : tuple if str, optional
            
        title : str, optional
            

        Returns
        -------
        matplotlib.lines.Line2D
            
        '''
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
                              offset=offsets[0],
                              cmap=cmap)
            cset = ax.contour(X, Y, Z,
                              zdir='y',
                              offset=offsets[1],
                              cmap=cmap)
            cset = ax.contour(X, Y, Z,
                              zdir='z',
                              offset=offsets[2],
                              cmap=cmap)

        if not tight:
            ax.set_xlim3d(lims[0][0], lims[0][1]);
            ax.set_ylim3d(lims[1][0], lims[1][1]);
            ax.set_zlim3d(lims[2][0], lims[2][1]);
        
        if show_labels:
            ax.set_xlabel(labels[0], fontsize=24)
            ax.set_ylabel(labels[1], fontsize=24)
            ax.set_zlabel(labels[2], fontsize=24)

        if title is not None:
            t = plt.title(title)

        return p


def linear_regression(X, Y, verbose=False, labels=None, round_to=4):
    '''
    
    Parameters
    ----------
    X : ndarray
        
    Y : ndarray
        
    verbose : bool, optional
        
    labels : list of str, optional
        
    round_to : int, optional
        

    Returns
    -------
    tuple(sklearn.linear_regression.LinearRegression,
          list of float,
          float)
        
    '''
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
    '''

    Parameters
    ----------
    X : ndarray
        
    Y : ndarray
        
    degree : int
        
    verbose : bool, optional
        
    labels : list of str, optional
        
    round_to : int, optional
        

    Returns
    -------
    tuple(sklearn.pipeline.Pipeline,
          list of float,
          float)
    '''
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
