import numpy as np
import scipy.stats
import scipy.spatial
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import warnings
import sys

warnings.simplefilter("error")


def compute_cost(R_trained, R_test):
    """
    :return: test error
    """
    xi, yi = R_test.nonzero()
    cost = 0
    for x, y in zip(xi, yi):
        cost += pow(R_test[x, y] - R_trained[x, y], 2)
    return np.sqrt(cost) / len(xi)

class CollaborativeFiltering():
    def __init__(self, R, k, learning_rate,  epochs, verbose=False):
        """

        :param R:
        :param k:
        :param learning_rate:
        :param reg_param:
        :param epochs:
        :param verbose:
        """
        self._R = R
        # self._k = k
        self._learning_rate = learning_rate
        self._epochs = epochs
        # self._verbose = verbose
        self._user_size, self._item_size = np.shape(self._R)

