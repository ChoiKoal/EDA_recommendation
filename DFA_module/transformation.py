import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
import pandas as pd
from collections import Counter, defaultdict

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

            if self.combination_dict[key]['column_count'] == 3:
                return 0


    def temporal_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            if column_1_type == 'tem' and column_2_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                self.calculate_match_performance_score(transformed, self.scenario_num - 1)
            if column_1_type == 'tem' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, transformed_2 = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)
            if column_2_type == 'tem' and column_1_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed = self.groupby_count(wrapped, combination_dict['column2'], combination_dict['column1'])
                self.calculate_match_performance_score(transformed, self.scenario_num - 1)
            if column_2_type == 'tem' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, transformed_2 = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'])
                self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def categorical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            # wrapped = self.pandas_container(combination_dict)
            if column_1_type == 'cat' and column_2_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            if column_1_type == 'cat' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, transformed_2 = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

            if column_2_type == 'cat' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, transformed_2 = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'])
                self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def numerical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            # if column_1_type == 'num' and column_2_type != 'num':
            #     wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
            #     print ("Bin by X, CNT by Y")
            if column_1_type == 'num' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed = self.numerical_raw(wrapped, combination_dict['column1'], combination_dict['column2'])
                print ("Bin by X, AGG by Y")
            # if column_1_type != 'num' and column_2_type == 'num':
            #     wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
            #     print ("Bin by X, CNT by Y")

    def pandas_container(self, column1, column2):

        column_1_name = column1
        column_2_name = column2

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
        transform_scenario["Agg_func"] = "count"
        self.scenario_dict["%d" %self.scenario_num] = transform_scenario
        transform_scenario["transform_score"] = self.calculate_transformation_score(grouped, combination_dict2)
        transform_scenario["scenario_num"] = self.scenario_num

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        self.scenario_num += 1
        return grouped

    def groupby_agg(self, dataframe, combination_dict1, combination_dict2):

        grouped_sum = dataframe['column2'].groupby(dataframe['column1']).sum()

        transform_scenario = {}
        transform_scenario["transform"] = "Groupby %s Agg(sum) %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func"] = "sum"
        transform_scenario["transform_score"] = self.calculate_transformation_score(grouped_sum, combination_dict2)
        transform_scenario["scenario_num"] = self.scenario_num

        self.scenario_dict["%d" %self.scenario_num] = transform_scenario

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        self.scenario_num += 1

        grouped_avg = dataframe['column2'].groupby(dataframe['column1']).mean()
        transform_scenario = {}
        transform_scenario["transform"] = "Groupby %s Agg(avg) %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func"] = "avg"
        transform_scenario["transform_score"] = self.calculate_transformation_score(grouped_avg, combination_dict2)
        transform_scenario["scenario_num"] = self.scenario_num

        self.scenario_dict["%d" %self.scenario_num] = transform_scenario

        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        print ("Transformation score : %.4f" %self.scenario_dict["%d" %self.scenario_num]["transform_score"])
        self.scenario_num += 1
        return grouped_sum, grouped_avg

    def numerical_raw(self, dataframe, combination_dict1, combination_dict2):
        transform_scenario = {}
        transform_scenario["transform"] = "Numerical_raw_Column %s Column %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func"] = "raw"
        transform_scenario["transform_score"] = 0
        transform_scenario["scenario_num"] = self.scenario_num

        self.scenario_dict["%d" %self.scenario_num] = transform_scenario
        print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        self.scenario_num += 1
        return 0

    def calculate_transformation_score(self, aggregated, measure):
        original_data_count = self.data_dict[measure]["enum"]
        aggregated_data_count = len(aggregated)
        score = 1 - aggregated_data_count/original_data_count
        return score



    def calculate_match_performance_score(self, grouped, scenario_num):
        picked_scenario = self.scenario_dict["%d" % scenario_num]
        pie_chart_score = self.pie_chart_score(grouped)
        bar_chart_score = self.bar_chart_score(grouped)
        if self.data_dict[picked_scenario['X']]['data_type'] == "num" and self.data_dict[picked_scenario['Y']]['data_type'] == "num":
            scatter_chart_score = self.scatter_chart_score(grouped)
            print("Scatter Chart Score : %.4f" % scatter_chart_score)
        line_chart_score = self.line_chart_score(grouped)
        print ("Pie Chart Score : %.4f" % pie_chart_score)
        print ("Bar Chart Score : %.4f" % bar_chart_score)

        return 0

    def pie_chart_score(self, grouped):
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if distinct_enum_X == 1:
            score = 0
        if min(grouped) < 0:
            score = 0
        if picked_scenario["Agg_func"] == "avg":
            score = 0
        if distinct_enum_X >= 2 and distinct_enum_X <= 10:
            score += self.calculate_entropy(self.data_dict[picked_scenario["Y"]])
        if distinct_enum_X > 10:
            score += 10 * (self.calculate_entropy(self.data_dict[picked_scenario["Y"]])) / distinct_enum_X
        if score > 10:
            print ('omg')
        if distinct_enum_X >= 2 and distinct_enum_X <= 10:
            score += self.calculate_entropy(self.data_dict[picked_scenario["Y"]])
        return score

    def bar_chart_score(self, grouped):
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if distinct_enum_X == 1:
            score = 0
        if distinct_enum_X >= 2 and distinct_enum_X <= 20:
            score = 1
        if distinct_enum_X > 20:
            score = 20 / distinct_enum_X
        return score

    def scatter_chart_score(self, grouped):
        score = 0
        return 0

    def line_chart_score(self, grouped):
        return 0


    def entropy(self, prop):
        return sum(-p * math.log(p, 2) for p in prop if p is not 0)

    def class_probability(self, data):
        total_count = len(data['data'])
        return [float(count)/float(total_count) for count in Counter(data['data']).values()]

    def calculate_entropy(self, data):
        prop = self.class_probability(data)
        return self.entropy(prop)