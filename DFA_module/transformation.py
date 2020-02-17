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
    def __init__(self, data_dict, combination_dict):
        self.data_dict = data_dict
        self.combination_dict = combination_dict
        self.scenario_dict = {}
        self.scenario_num = 0
        self.agg_func = ["sum", "avg"]

    def transformation(self):
        for key in self.combination_dict.keys():
            if self.combination_dict[key]['column_count'] == 2:
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'tem' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'tem':
                    self.temporal_transformation(self.combination_dict[key])
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'cat' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'cat':
                    self.categorical_transformation(self.combination_dict[key])
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'num' and self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'num':
                    self.numerical_transformation(self.combination_dict[key])

            if self.combination_dict[key]['column_count'] == 3:
                num_count = 0
                num_column = []
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(0)
                if self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(1)
                if self.data_dict[self.combination_dict[key]['column3']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(2)

                if num_count == 1:
                    self.three_column_groupby_logic(self.combination_dict[key], num_column)

        m_score = []
        for key in self.scenario_dict:

            m_score.append(self.scenario_dict[key]["m_score"])

        return self.scenario_dict


    def temporal_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            if column_1_type == 'tem' and column_2_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            if column_1_type == 'tem' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num-1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

            if column_2_type == 'tem' and column_1_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_count(wrapped, combination_dict['column2'], combination_dict['column1'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            if column_2_type == 'tem' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def categorical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            # wrapped = self.pandas_container(combination_dict)
            if column_1_type == 'cat' and column_2_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            if column_1_type == 'cat' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

            if column_2_type == 'cat' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def numerical_transformation(self, combination_dict):
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            # if column_1_type == 'num' and column_2_type != 'num':
            #     wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
            #     print ("Bin by X, CNT by Y")
            count = 0
            agg_data = []
            # for i in range(len(self.data_dict[combination_dict['column1']]['data'])):
            #     if self.data_dict[combination_dict['column1']]['isnull'][i] == False and self.data_dict[combination_dict['column2']]['isnull'][i] == False:
            #         count += 1
            #         agg_data += [self.data_dict[combination_dict['column1']]['data'][i], self.data_dict[combination_dict['column2']]['data'][i]]
            index = np.where((1 - self.data_dict[combination_dict['column1']]['isnull']) * (
                        1 - self.data_dict[combination_dict['column2']]['isnull']) == True)[0]
            for i in index:
                agg_data += [self.data_dict[combination_dict['column1']]['data'][i],
                             self.data_dict[combination_dict['column2']]['data'][i]]
                count += 1
            if count > 0:
                agg_data = pd.DataFrame(np.reshape(agg_data, [-1, 2]))
                agg_data = self.numerical_raw(agg_data, combination_dict['column1'], combination_dict['column2'])
                self.scenario_dict["%d" % (self.scenario_num-1)]['m_score'] = self.calculate_match_performance_score(agg_data, self.scenario_num - 1)
                return agg_data
            else:
                agg_data = pd.DataFrame(np.reshape(agg_data, [-1, 2]))
                return 0

            # wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
            # transformed = self.numerical_raw(wrapped, combination_dict['column1'], combination_dict['column2'])
            # if column_1_type != 'num' and column_2_type == 'num':
            #     wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
            #     print ("Bin by X, CNT by Y")

    def three_column_groupby_logic(self, combination_dict, num_column):
        # column_name = [combination_dict['column1'], combination_dict['column2'], combination_dict['column3']]
        # num_column_name = column_name[num_column]


        return 0


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

        agg_data = []
        count = 0
        complete = False
        # for i in range(len(self.data_dict[combination_dict1]['data'])):
        #     if self.data_dict[combination_dict1]['isnull'][i] == False and \
        #             self.data_dict[combination_dict2]['isnull'][i] == False:
        #         count += 1
        #         agg_data += [self.data_dict[combination_dict1]['data'][i],
        #                      self.data_dict[combination_dict2]['data'][i]]

        index = np.where((1-self.data_dict[combination_dict1]['isnull']) * (1-self.data_dict[combination_dict2]['isnull']) == True)[0]
        for i in index:
            agg_data += [self.data_dict[combination_dict1]['data'][i],
                             self.data_dict[combination_dict2]['data'][i]]
            count += 1
        agg_data = pd.DataFrame(np.reshape(agg_data, [-1, 2]))
        if count > 0:


            agg_data = agg_data[1].groupby(agg_data[0]).count()
            agg_data = pd.Series.sort_values(agg_data)
            transform_scenario = {}
            transform_scenario["transform"] = "Groupby %s Count %s" %(combination_dict1, combination_dict2)
            transform_scenario["X"] = combination_dict1
            transform_scenario["Y"] = combination_dict2
            transform_scenario["Agg_func_X"] = "GROUPBY"
            transform_scenario["Agg_func_Y"] = "COUNT"
            self.scenario_dict["%d" %self.scenario_num] = transform_scenario
            transform_scenario["transform_score"] = self.calculate_transformation_score(agg_data, combination_dict2)
            transform_scenario["scenario_num"] = self.scenario_num

            # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
            # print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
            self.scenario_num += 1
            complete = True
        return agg_data, complete



    def groupby_agg(self, dataframe, combination_dict1, combination_dict2):

        # grouped_sum = dataframe['column2'].groupby(dataframe['column1']).sum()
        # grouped_sum = pd.Series.sort_values(grouped_sum)
        #
        # transform_scenario = {}
        # transform_scenario["transform"] = "Groupby %s Agg(sum) %s" %(combination_dict1, combination_dict2)
        # transform_scenario["X"] = combination_dict1
        # transform_scenario["Y"] = combination_dict2
        # transform_scenario["Agg_func_X"] = "GROUPBY"
        # transform_scenario["Agg_func_Y"] = "SUM"
        # transform_scenario["transform_score"] = self.calculate_transformation_score(grouped_sum, combination_dict2)
        # transform_scenario["scenario_num"] = self.scenario_num
        #
        # self.scenario_dict["%d" %self.scenario_num] = transform_scenario
        #
        # # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        # # print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        # self.scenario_num += 1
        complete = False
        agg_data = []
        count = 0

        # for i in range(len(self.data_dict[combination_dict1]['data'])): #Null key detecting
        #     if self.data_dict[combination_dict1]['isnull'][i] == False and \
        #             self.data_dict[combination_dict2]['isnull'][i] == False:
        #         count += 1
        #         agg_data += [self.data_dict[combination_dict1]['data'][i],
        #                      self.data_dict[combination_dict2]['data'][i]]

        index = np.where((1-self.data_dict[combination_dict1]['isnull']) * (1-self.data_dict[combination_dict2]['isnull']) == True)[0]
        for i in index:
            agg_data += [self.data_dict[combination_dict1]['data'][i],
                             self.data_dict[combination_dict2]['data'][i]]
            count += 1

        agg_data = pd.DataFrame(np.reshape(agg_data, [-1, 2]))

        if count > 0:

            agg_data[1] = agg_data[1].astype(float) #type casting.... data_dict->agg data(str)
            agg_data = agg_data[1].groupby(agg_data[0]).mean()
            agg_data = pd.Series.sort_values(agg_data)
            transform_scenario = {}
            transform_scenario["transform"] = "Groupby %s Agg(avg) %s" %(combination_dict1, combination_dict2)
            transform_scenario["X"] = combination_dict1
            transform_scenario["Y"] = combination_dict2
            transform_scenario["Agg_func_X"] = "GROUPBY"
            transform_scenario["Agg_func_Y"] = "AVG"
            transform_scenario["transform_score"] = self.calculate_transformation_score(agg_data, combination_dict2)
            transform_scenario["scenario_num"] = self.scenario_num

            self.scenario_dict["%d" %self.scenario_num] = transform_scenario

            # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
            # print ("Transformation score : %.4f" %self.scenario_dict["%d" %self.scenario_num]["transform_score"])
            self.scenario_num += 1
            complete = True
        return agg_data, complete


    def numerical_raw(self, dataframe, combination_dict1, combination_dict2):
        grouped = pd.Series(dataframe[1].values, index=dataframe[0].values)
        grouped = pd.Series.sort_values(grouped)
        transform_scenario = {}
        transform_scenario["transform"] = "Numerical_raw_Column %s Column %s" %(combination_dict1, combination_dict2)
        transform_scenario["X"] = combination_dict1
        transform_scenario["Y"] = combination_dict2
        transform_scenario["Agg_func_X"] = "RAW"
        transform_scenario["Agg_func_Y"] = "RAW"
        transform_scenario["transform_score"] = 0
        transform_scenario["scenario_num"] = self.scenario_num

        self.scenario_dict["%d" %self.scenario_num] = transform_scenario
        # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        # print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        self.scenario_num += 1
        return grouped

    def calculate_transformation_score(self, aggregated, measure):
        original_data_count = self.data_dict[measure]["distinct_enum"]
        aggregated_data_count = len(aggregated)
        score = 1 - aggregated_data_count/original_data_count
        return score



    def calculate_match_performance_score(self, grouped, scenario_num):
        picked_scenario = self.scenario_dict["%d" % scenario_num]
        pie_chart_score = self.pie_chart_score(grouped)
        bar_chart_score = self.bar_chart_score(grouped)
        if self.data_dict[picked_scenario['X']]['data_type'] == "num" and self.data_dict[picked_scenario['Y']]['data_type'] == "num":
            scatter_chart_score = self.scatter_chart_score(grouped)
            # print("Scatter Chart Score : %.4f" % scatter_chart_score)
            line_chart_score = 0
        else:
            grouped = pd.Series.sort_values(grouped)
            if self.data_dict[picked_scenario['X']]['data_type'] == "tem":
                grouped = pd.Series.sort_index(grouped)
            line_chart_score = self.line_chart_score(grouped)
            # print("Line Chart Score : %.4f" % line_chart_score)
            scatter_chart_score = 0
        # print ("Pie Chart Score : %.4f" % pie_chart_score)
        # print ("Bar Chart Score : %.4f" % bar_chart_score)

        m_score = [pie_chart_score, bar_chart_score, line_chart_score, scatter_chart_score]
        m_score = m_score / np.max(m_score)
        match_index = np.argmax(m_score)
        if match_index == 0:
            self.scenario_dict["%d" % scenario_num]["Chart_Type"] = "PIE_CHART"
        if match_index == 1:
            self.scenario_dict["%d" % scenario_num]["Chart_Type"] = "BAR_CHART"
        if match_index == 2:
            self.scenario_dict["%d" % scenario_num]["Chart_Type"] = "LINE_CHART"
        if match_index == 3:
            self.scenario_dict["%d" % scenario_num]["Chart_Type"] = "SCATTER_CHART"

        return m_score[match_index]

    def pie_chart_score(self, grouped):
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if distinct_enum_X >= 2 and distinct_enum_X <= 8:
            score += self.calculate_entropy(self.data_dict[picked_scenario["Y"]])
        if distinct_enum_X > 8:
            score += 4 * (self.calculate_entropy(self.data_dict[picked_scenario["Y"]])) / distinct_enum_X
        if min(grouped) < 0:
            score = 0
        if distinct_enum_X == 1:
            score = 0
        if picked_scenario["Agg_func_Y"] == "avg":
            score = 0
        return score

    def bar_chart_score(self, grouped):
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if distinct_enum_X == 1:
            score = 0
        if distinct_enum_X >= 2 and distinct_enum_X <= 20:
            score = 1.5
        if distinct_enum_X > 20:
            score = 30 / distinct_enum_X
        return score

    def scatter_chart_score(self, grouped):
        score = np.abs(np.corrcoef(grouped.keys(), grouped.values)[0][1])
        return score

    def line_chart_score(self, grouped):
        keys = []
        score = []
        line_score = 0
        for i in range(len(grouped.keys())):
            keys.append(i+1)
        score.append(np.abs(np.corrcoef(keys, grouped.values)[0][1])) #linear match
        score.append(np.abs(np.corrcoef(keys, np.log(grouped.values))[0][1])) #log match
        score.append(np.abs(np.corrcoef(np.log(keys), grouped.values)[0][1]))  #exponential match

        final_score = np.max(score)
        if final_score > 0.3:
            line_score = 1
        return line_score


    def entropy(self, prop):
        return sum(-p * math.log(p, 2) for p in prop if p is not 0)

    def class_probability(self, data):
        total_count = len(data['data'])
        return [float(count)/float(total_count) for count in Counter(data['data']).values()]

    def calculate_entropy(self, data):
        prop = self.class_probability(data)
        return self.entropy(prop)