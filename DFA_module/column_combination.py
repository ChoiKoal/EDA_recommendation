import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv

class ColumnCombination():
    def __init__(self, data_dictionary):
        """

        :param data_dictionary : data dictionary
        """

        self.data_dictionary = data_dictionary
        self.data_name = np.array(list(self.data_dictionary.keys()))
        self.data_type = []
        for i in range(len(self.data_name)):
            self.data_type.append(self.data_dictionary[self.data_name[i]]['data_type'])
        self.columnset_dict = {}


    def create_combination(self):
        self.combination_2column()
        self.combination_3column()
        return self.columnset_dict

    def combination_2column(self):
        for i in range(100):
            self.columnset_dict["%d" %i] = {}
            self.columnset_dict["%d" %i]["column1"] = self.data_name[0]
            self.columnset_dict["%d" %i]["column2"] = self.data_name[1]

    def combination_3column(self):
        for i in range(100):
            self.columnset_dict["%d" %i] = {}
            self.columnset_dict["%d" %i]["column1"] = self.data_name[0]
            self.columnset_dict["%d" %i]["column2"] = self.data_name[1]
            self.columnset_dict["%d" %i]["column3"] = self.data_name[2]
