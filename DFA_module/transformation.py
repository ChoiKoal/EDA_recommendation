import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
import pandas as pd

class Transformation():
    def __init__(self, data_dict, combination_dict, scenario_dict):
        self.data_dict = data_dict
        self.combination_dict = combination_dict
        self.scenario_dict = scenario_dict
        self.scenario_num = 0
        self.agg_func = ["sum", "avg"]

    def transformation(self):
        for key in self.combination_dict.keys():
            if self.combination_dict[key]['column_count'] == 2:
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'tem' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'tem':
                    self.temporal_transformation(self.combination_dict[key])
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'cat' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'cat':
                    self.categorical_transformation(self.combination_dict[key])
                else:
                    self.numerical_transformation(self.combination_dict[key])


    def temporal_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            wrapped = self.pandas_container(combination_dict)
            if column_1_type == 'tem' and column_2_type == 'cat':
                transformed = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
            if column_1_type == 'tem' and column_2_type == 'num':
                transformed = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                print ("Bin/Group by X, AGG by Y")
            if column_2_type == 'tem' and column_1_type == 'cat':
                transformed = self.groupby_count(wrapped, combination_dict['column2'], combination_dict['column1'])
                print ("Bin/Group by X, CNT by Y")
            if column_2_type == 'tem' and column_1_type == 'num':
                print ("Bin/Group by X, AGG by Y")

    def categorical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            wrapped = self.pandas_container(combination_dict)
            if column_1_type == 'cat' and column_2_type == 'cat':
                transformed = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                print ("Group by X, CNT by Y")
            if column_1_type == 'cat' and column_2_type == 'num':
                print ("Group by X, AGG by Y")
            if column_2_type == 'cat' and column_1_type == 'cat':
                transformed = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                print ("Group by X, CNT by Y")
            if column_2_type == 'cat' and column_1_type == 'num':
                print ("Group by X, AGG by Y")

    def numerical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            if column_1_type == 'num' and column_2_type != 'num':
                print ("Bin by X, CNT by Y")
            if column_1_type == 'num' and column_2_type == 'num':
                print ("Bin by X, AGG by Y")
            if column_1_type != 'num' and column_2_type == 'num':
                print ("Bin by X, CNT by Y")

    def pandas_container(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_name = combination_dict['column1']
            column_2_name = combination_dict['column2']

            column_1 = self.data_dict[column_1_name]
            column_2 = self.data_dict[column_2_name]

            wrapped_data = pd.DataFrame({'column1' : column_1['data'],
                                         'column2' : column_2['data']})
            # grouped = wrapped_data['column1'].groupby['column2']
            return wrapped_data

    def groupby_count(self, dataframe, combination_dict1, combination_dict2):
        grouped = dataframe['column2'].groupby(dataframe['column1']).count()
        transform_scenario = {}
        transform_scenario["transform"] = "Groupby %s Count %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        self.scenario_dict["%d" %self.scenario_num] = transform_scenario

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        self.scenario_num += 1
        return grouped

    def groupby_agg(self, dataframe, combination_dict1, combination_dict2):

        grouped_sum = dataframe['column2'].groupby(dataframe['column1']).sum()
        transform_scenario = {}
        transform_scenario["transform"] = "Groupby %s Agg(sum) %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func"] = "sum"
        self.scenario_dict["%d" %self.scenario_num] = transform_scenario

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        self.scenario_num += 1

        grouped_avg = dataframe['column2'].groupby(dataframe['column1']).agg
        transform_scenario = {}
        transform_scenario["transform"] = "Groupby %s Agg(avg) %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func"] = "avg"
        self.scenario_dict["%d" %self.scenario_num] = transform_scenario

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        self.scenario_num += 1
        return grouped_sum

    def bining(self, dataframe):
        return 0
