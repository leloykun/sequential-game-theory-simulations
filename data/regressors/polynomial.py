import copy
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from collections import namedtuple
ModelData = namedtuple('ModelData',
                       'model degree r_sqaured powers coefs labels func')
XYPair = namedtuple('XYPair', 'X Y')


class PolynomialRegressor:
    """Polynomial Regression

    Does polynomial regression. The optimal degree of the polynomial will
    also be automatically determined when initialized with degree='auto'.

    Note: The original author do not have adequate experience in the
    industry so if bugs are found, please help him squash them.
    """
    def __init__(self, degree='auto', test_degrees=10, eps=0.01,
                 early_stopping=True, patience=3, to_cache=False):
        """Initialize the polynomial regressor

        Todo
        ----
        - add option to normalize the input values
        - add option to label the features

        Parameters
        ----------
        degree : int or {str: "auto"}, optional
            The degree of the polynomial estimator. By default, 'auto'
            which means cross_validation() will be run to determine the
            optimal degree of the polynomial estimate.
        test_degrees: int or array-like, optional
            The test degrees used in the cross_validation. By default, 10.
            If int, then it is first transformed into a list: x => [0..x]
        eps : float, optional
            The epsilon used in the cross_validation. By default 0.01.
        early_stopping : bool, optional
            Option to stop the cross_validation early. By default, True.
        patience : int, optional
            The number of consecutive iterrations where the performance
            of the polynomial estimate does not improve before
            cross_validation is stopped. By default 3.
        to_cache : bool, optional
            Option to cache the results of the polynomial regression. By
            default, True.
        """
        self.def_degree = degree
        if hasattr(test_degrees, "__iter__"):
            if not test_degrees:
                self.test_degrees = [0]
            self.test_degrees = test_degrees
        else:
            self.test_degrees = list(range(test_degrees + 1))

        self.eps = eps
        self.early_stopping = early_stopping
        self.patience = patience

        self.to_cache = to_cache
        self.cache = {}

    def fit(self, training_data, test_data=None, verbose=0):
        """Fit the data into the polynomial regressor

        Parameters
        ----------
        training_data : XYPair, shape=(2, n_samples, n_features)
            The training data of the polynomial regressor.
        test_data : XYPair, shape=(2, n_samples, 1), optional
            The test data of the polynomial regressor. By default, None.
        verbose : int {0, 1}, optional
            The verbosity of the operation. By default, 0 which means
            nothing will be printed.

        Returns
        -------
        self : instance
        """
        self.training_data = copy.deepcopy(training_data)
        self.test_data = copy.deepcopy(test_data)

        self.n_samples = len(self.training_data.X)
        if hasattr(self.training_data.X[0], '__len__'):
            self.n_features = len(self.training_data.X[0])
        else:
            self.n_features = 1

        self.cache = {}

        if self.def_degree == 'auto':
            self._regress(self._cross_validation(verbose), verbose)
        else:
            self._regress(self.def_degree, verbose)

        return self

    def _cross_validation(self, verbose=0):
        """Determine the best degree of the polynomial estimate

        Todo:
        -----
        - Add option to use k-folding

        Parameters
        ----------
        verbose : int {0, 1}, optional
            The verbosity of the operation. By default, 0 which means
            nothing will be printed.
        """
        best_degree = 0
        best_r_squared = 0.0
        been_patient = 0
        for i in range(len(self.test_degrees)):
            test_degree = self.test_degrees[i]
            self._regress(test_degree, verbose)
            if i == 0 or self.r_sqaured - best_r_squared > self.eps:
                best_degree = test_degree
                best_r_squared = self.r_sqaured
                been_patient = 0
            elif self.early_stopping:
                been_patient += 1
                if been_patient == self.patience:
                    break
        if verbose == 1:
            print("best_degree: {}  ||  best_r_squared: {}\n" .format(best_degree, best_r_squared))
        return best_degree

    def _regress(self, degree, verbose=0):
        """Do polynomial regression of given degree

        Parameters
        ----------
        degree : int
            The degree of the polynomial estimate.
        verbose : int {0, 1}, optional
            The verbosity of the operation. By default, 0 which means
            nothing will be printed.
        """
        if degree in self.cache:
            self.model, self.degree, self.r_sqaured, self.powers, self.coefs, self.labels, self.func = self.cache[degree]
        else:
            self.model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                                   ('linear', LinearRegression(fit_intercept=False))])
            self.model.fit(*self.training_data)
            self.degree = degree
            
            self.r_sqaured = self.score()

            self.powers = self.model.named_steps['poly'].powers_
            self.coefs = self.model.named_steps['linear'].coef_

            self.labels = self._calc_labels()
            self.func = list(zip(self.coefs[0], self.labels))

            if self.to_cache:
                self.cache[degree] = ModelData(self.model,
                                               self.degree,
                                               self.r_sqaured,
                                               self.powers,
                                               self.coefs,
                                               self.labels,
                                               self.func)

        if verbose == 1:
            print("degree: {}  ||  r_sqaured: {}".format(self.degree,
                                                         self.r_sqaured))

    def _calc_labels(self):
        """Return the feature names of the polynomial estimate

        Returns
        -------
        list
            The feature names of the polynomial estimate.
        """
        labels = self.model.named_steps['poly'].get_feature_names()
        return ['*'.join(label.split()) for label in labels]

    def print_func(self):
        """Print polynomial function"""
        print(' + '.join("%lf*%s" % nomial for nomial in self.func))

    def score(self, test_data=None):
        """Return the score of the polynomial estimate

        Parameters
        ----------
        test_data : XYPair, optional
            The test data of the scoring function. By default, None.

        Returns
        -------
        float
            The score of the polynomial estimate.
        """
        if test_data is None:
            if self.test_data is None:
                return self.model.score(*self.training_data)
            else:
                return self.model.score(*self.test_data)
        else:
            return self.model.score(*test_data)

    def predict(self, X=None):
        """Predict the corresponding output of the given input

        Parameters
        ----------
        X : array-like, optional
            The data used in the prediction. By default, None which means
            the training data will be used.

        Returns
        -------
        array-like
            The predicted output.
        """
        if X is None:
            X = self.training_data.X
        return self.model.predict(X)
