import numpy as np
import math
import pandas as pd
from collections import Counter

class Transformation():
    def __init__(self, data_dict, combination_dict):
        """
        :param data_dict: data dictionary created by CLASS CreateDictionary
        :param combination_dict: combination dictionary created by CLASS ColumnCombination
        :param scenario_dict: scenario dictionary (scenario, X, X_agg, Y, Y_agg, transformation_score, m_score)
        :param agg_func: supporting aggregation function
        """
        self.data_dict = data_dict
        self.combination_dict = combination_dict
        self.scenario_dict = {}
        self.scenario_num = 0
        self.agg_func = ["sum", "avg"]

    def transformation(self):
        """
        decide which algorithm to be used with the meta info of combination_dict and data_dict
        after transformation, calculate m_score, normalize and pick the right visualization
        also, create scenario dictionary with metas
        :return: scenario dict
        """
        for key in self.combination_dict.keys():
            if self.combination_dict[key]['column_count'] == 2:
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'tem' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'tem':
                    self.temporal_transformation(self.combination_dict[key])
                elif self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'cat' or self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'cat':
                    self.categorical_transformation(self.combination_dict[key])
                elif self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'num' and self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'num':
                    self.numerical_transformation(self.combination_dict[key])

            elif self.combination_dict[key]['column_count'] == 3:
                num_count = 0
                num_column = []
                if self.data_dict[self.combination_dict[key]['column1']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(0)
                elif self.data_dict[self.combination_dict[key]['column2']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(1)
                elif self.data_dict[self.combination_dict[key]['column3']]['data_type'] == 'num':
                    num_count += 1
                    num_column.append(2)

                if num_count == 1:
                    self.three_column_groupby_logic(self.combination_dict[key], num_column)

        m_score_pie = []
        m_score_bar = []
        m_score_line = []
        m_score_scatter = []
        for key in self.scenario_dict:

            m_score_pie.append(self.scenario_dict[key]["Pie_chart_score"])
            m_score_bar.append(self.scenario_dict[key]["Bar_chart_score"])
            m_score_line.append(self.scenario_dict[key]["Line_chart_score"])
            m_score_scatter.append(self.scenario_dict[key]["Scatter_chart_score"])

        m_score_pie /= np.max(m_score_pie)
        m_score_bar /= np.max(m_score_bar)
        m_score_line /= np.max(m_score_line)
        m_score_scatter /= np.max(m_score_scatter)
        m_score = [m_score_pie, m_score_bar, m_score_line, m_score_scatter]
        match_index = np.argmax(m_score, axis = 0)
        for key in self.scenario_dict:
            if match_index[int(key)] == 0:
                self.scenario_dict[key]["Chart_Type"] = "pie"
            if match_index[int(key)] == 1:
                self.scenario_dict[key]["Chart_Type"] = "bar"
            if match_index[int(key)] == 2:
                self.scenario_dict[key]["Chart_Type"] = "line"
            if match_index[int(key)] == 3:
                self.scenario_dict[key]["Chart_Type"] = "scatter"
            self.scenario_dict[key]["m_score"] = m_score[match_index[int(key)]][int(key)]

        return self.scenario_dict


    def temporal_transformation(self, combination_dict):
        """
        if one of the column is temporal data column
        tem + cat -> GroupBy tem Count cat
        tem + num -> GroupBy tem Agg num
        :param combination_dict: picked combination
        :return: created scenario_dict
        """
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            if column_1_type == 'tem' and column_2_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            elif column_1_type == 'tem' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'])
                if complete == True:
                    self.calculate_match_performance_score(transformed, self.scenario_num-1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

            elif column_2_type == 'tem' and column_1_type == 'cat':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_count(wrapped, combination_dict['column2'], combination_dict['column1'])
                if complete == True:
                    self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            elif column_2_type == 'tem' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'])
                if complete == True:
                    self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def categorical_transformation(self, combination_dict, three_column = False):
        """
        if one of the column is categorical data column
        cat + num -> GroupBy cat Agg num
        :param combination_dict: picked combination
        :return: created scenario_dict
        """
        if combination_dict['column_count'] == 2:
            column_1_type = self.data_dict[combination_dict['column1']]['data_type']
            column_2_type = self.data_dict[combination_dict['column2']]['data_type']
            # wrapped = self.pandas_container(combination_dict)
            # if column_1_type == 'cat' and column_2_type == 'cat':
            #     wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
            #     transformed, complete = self.groupby_count(wrapped, combination_dict['column1'], combination_dict['column2'])
            #     if complete == True:
            #         self.calculate_match_performance_score(transformed, self.scenario_num - 1)

            if column_1_type == 'cat' and column_2_type == 'num':
                wrapped = self.pandas_container(combination_dict['column1'], combination_dict['column2'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column1'], combination_dict['column2'], three_column)
                if complete == True:
                    self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

            if column_2_type == 'cat' and column_1_type == 'num':
                wrapped = self.pandas_container(combination_dict['column2'], combination_dict['column1'])
                transformed, complete = self.groupby_agg(wrapped, combination_dict['column2'], combination_dict['column1'], three_column)
                if complete == True:
                    self.calculate_match_performance_score(transformed, self.scenario_num - 1)
                # self.scenario_dict["%d" % (self.scenario_num-1)]['m_score']  = self.calculate_match_performance_score(transformed_2, self.scenario_num - 1)

    def numerical_transformation(self, combination_dict):
        """
        if all columns are numerical column
        num + num -> raw data + scatter
        :param combination_dict: picked combination
        :return: created scenario_dict
        """
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
                self.calculate_match_performance_score(agg_data, self.scenario_num - 1)
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
        """
        special rules for 3+ column combination
        Group temoral and categorical columns and make it as one column
        Make it 2 column combination and go to categorical_transformation
        :param combination_dict: picked combination
        :param num_column: numerical column index
        :return: created scenario_dict
        """
        column_name = [combination_dict['column1'], combination_dict['column2'], combination_dict['column3']]
        num_column_name = column_name[num_column[0]]

        column_name.remove(num_column_name)
        if self.data_dict[column_name[0]]['data_type'] == "tem" and self.data_dict[column_name[1]]['data_type'] == "tem": # both temporal(difficult)
            return 0
        elif self.data_dict[column_name[0]]['data_type'] == "cat" and self.data_dict[column_name[0]]['distinct_enum'] > 5: # cat > 5
            return 0
        elif self.data_dict[column_name[1]]['data_type'] == "cat" and self.data_dict[column_name[1]]['distinct_enum'] > 5: # cat > 5
            return 0
        else:
            if self.data_dict[column_name[1]]['data_type'] == "tem":
                column_name.reverse()
            comb_column_name = column_name[0] + " " + column_name[1]
            self.data_dict[comb_column_name] = {}
            dimension_comb = [[str(i) for i in self.data_dict[column_name[0]]['data']], [str(i) for i in self.data_dict[column_name[1]]['data']]]
            self.data_dict[comb_column_name]['data'] = [dimension_comb[0][i] + " " + dimension_comb[1][i] for i in range(len(dimension_comb[0]))]
            self.data_dict[comb_column_name]['data_type'] = "cat"
            self.data_dict[comb_column_name]['isnull'] = self.data_dict[column_name[0]]['isnull']
            self.data_dict[comb_column_name]['distinct_enum'] = len(Counter(self.data_dict[comb_column_name]["data"]))
            self.data_dict[comb_column_name]['col1'] = column_name[0]
            self.data_dict[comb_column_name]['col2'] = column_name[1]
            combination_dict_new = {}
            combination_dict_new['column1'] = comb_column_name
            combination_dict_new['column2'] = num_column_name
            combination_dict_new['column_count'] = 2
            three_column = True
            self.categorical_transformation(combination_dict_new, three_column)
            self.scenario_dict["%s" % (self.scenario_num-1)]['transform'] = "GROUPBY %s GROUPBY %s Agg(sum) %s" %(column_name[0], column_name[1], num_column_name)
            self.scenario_dict["%s" % (self.scenario_num-1)]['X'] = column_name[0]
            self.scenario_dict["%s" % (self.scenario_num-1)]['X2'] = column_name[1]
            self.scenario_dict["%s" % (self.scenario_num-1)]['Agg_func_X2'] = "GROUPBY"
            self.scenario_dict["%s" % (self.scenario_num-1)]['3column'] = True
            self.data_dict.pop(comb_column_name, None)




    def pandas_container(self, column1, column2):
        """
        make pandas container to use agg function
        :param column1
        :param column2
        :return:
        """

        column_1_name = column1
        column_2_name = column2

        column_1 = self.data_dict[column_1_name]
        column_2 = self.data_dict[column_2_name]

        wrapped_data = pd.DataFrame({'column1' : column_1['data'],
                                     'column2' : column_2['data']})
        # grouped = wrapped_data['column1'].groupby['column2']
        return wrapped_data

    def groupby_count(self, dataframe, combination_dict1, combination_dict2):
        """
        GroupBy + Count
        :param combination_dict1: first column in combination_dict
        :param combination_dict2: second column in combination_dict
        :return:
        """

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
            transform_scenario["3column"] = False

            # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
            # print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
            self.scenario_num += 1
            complete = True
        return agg_data, complete



    def groupby_agg(self, dataframe, combination_dict1, combination_dict2, three_column = False):
        """
        GroupBy + Agg
        :param combination_dict1: first column in combination_dict
        :param combination_dict2: second column in combination_dict
        :param three_column: whether its three column case or not
        :return:
        """

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

        index = np.where((1-self.data_dict[combination_dict1]['isnull']) * (1-self.data_dict[combination_dict2]['isnull']) == True)[0]
        for i in index:
            agg_data += [self.data_dict[combination_dict1]['data'][i],
                             self.data_dict[combination_dict2]['data'][i]]
            count += 1

        agg_data = pd.DataFrame(np.reshape(agg_data, [-1, 2]))

        if count > 0:

            agg_data[1] = agg_data[1].astype(float) #type casting.... data_dict->agg data(str)
            agg_data = agg_data[1].groupby(agg_data[0]).sum()
            agg_data = pd.Series.sort_values(agg_data)
            transform_scenario = {}
            transform_scenario["transform"] = "Groupby %s Agg(sum) %s" %(combination_dict1, combination_dict2)
            transform_scenario["X"] = combination_dict1
            transform_scenario["Y"] = combination_dict2
            transform_scenario["Agg_func_X"] = "GROUPBY"
            transform_scenario["Agg_func_Y"] = "SUM"
            transform_scenario["transform_score"] = self.calculate_transformation_score(agg_data, combination_dict2)
            transform_scenario["scenario_num"] = self.scenario_num
            transform_scenario["3column"] = three_column

            self.scenario_dict["%d" %self.scenario_num] = transform_scenario

            # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
            # print ("Transformation score : %.4f" %self.scenario_dict["%d" %self.scenario_num]["transform_score"])
            self.scenario_num += 1
            complete = True
        return agg_data, complete


    def numerical_raw(self, dataframe, combination_dict1, combination_dict2):
        """
        make numerical column container
        :param dataframe: pandas dataframed data
        :param combination_dict1: first column in combination_dict
        :param combination_dict2: second column in combination_dict
        :return:
        """
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
        transform_scenario["3column"] = False

        self.scenario_dict["%d" %self.scenario_num] = transform_scenario
        # print (self.scenario_dict["%d" %self.scenario_num]["transform"])
        # print("Transformation score : %.4f" % self.scenario_dict["%d" % self.scenario_num]["transform_score"])
        self.scenario_num += 1
        return grouped

    def calculate_transformation_score(self, aggregated, measure):
        """
        calculate transformation score Q = 1 - |X'|/|X|
        :param aggregated: aggregated data
        :param measure: original data
        :return:
        """
        original_data_count = self.data_dict[measure]["distinct_enum"]
        aggregated_data_count = len(aggregated)
        score = 1 - aggregated_data_count/original_data_count
        return score



    def calculate_match_performance_score(self, grouped, scenario_num):
        """
        Rule-based scoring for visualization match performance
        :param grouped: aggregated data
        :param scenario_num
        :return:
        """
        picked_scenario = self.scenario_dict["%d" % scenario_num]

        pie_chart_score = 0
        bar_chart_score = 0
        scatter_chart_score = 0
        line_chart_score = 0
        if self.data_dict[picked_scenario['X']]['data_type'] == "num" and self.data_dict[picked_scenario['Y']]['data_type'] == "num":
            scatter_chart_score = self.scatter_chart_score(grouped)
            # print("Scatter Chart Score : %.4f" % scatter_chart_score)

        elif self.data_dict[picked_scenario['X']]['data_type'] == "tem" and picked_scenario['3column'] == True:
            if len(grouped) > 7:
                line_chart_score = self.line_chart_score(grouped)
            else:
                bar_chart_score = self.bar_chart_score(grouped)
        elif self.data_dict[picked_scenario['X']]['data_type'] == "cat" and picked_scenario['3column'] == True:
            bar_chart_score = self.bar_chart_score(grouped)
        elif self.data_dict[picked_scenario['X']]['data_type'] == "cat" and len(grouped) < 20 and picked_scenario['3column'] == False:
            grouped = pd.Series.sort_values(grouped)
            # if self.data_dict[picked_scenario['X']]['data_type'] == "tem":
            #     grouped = pd.Series.sort_index(grouped)
            bar_chart_score = self.bar_chart_score(grouped)
            line_chart_score = self.line_chart_score(grouped)
            if len(grouped) < 6:
                pie_chart_score = self.pie_chart_score(grouped)
        elif self.data_dict[picked_scenario['X']]['data_type'] == "tem" and picked_scenario['3column'] == False:
            if len(grouped) > 7:
                line_chart_score = self.line_chart_score(grouped)
            else:
                bar_chart_score = self.bar_chart_score(grouped)


        # print ("Pie Chart Score : %.4f" % pie_chart_score)
        # print ("Bar Chart Score : %.4f" % bar_chart_score)

        m_score = [pie_chart_score, bar_chart_score, line_chart_score, scatter_chart_score]
        self.scenario_dict["%d" % scenario_num]["Pie_chart_score"] = pie_chart_score
        self.scenario_dict["%d" % scenario_num]["Bar_chart_score"] = bar_chart_score
        self.scenario_dict["%d" % scenario_num]["Line_chart_score"] = line_chart_score
        self.scenario_dict["%d" % scenario_num]["Scatter_chart_score"] = scatter_chart_score


    def pie_chart_score(self, grouped):
        """
        calculate Match Performance Score between Data and Pie chart
        :return: m_score_pie
        """
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if min(grouped) < 0:
            score = 0
        elif distinct_enum_X == 1:
            score = 0
        elif picked_scenario["Agg_func_Y"] == "avg":
            score = 0
        elif distinct_enum_X >= 2 and distinct_enum_X <= 8:
            score += self.calculate_entropy(self.data_dict[picked_scenario["Y"]]) / 8
        elif distinct_enum_X > 8:
            score += 4 * (self.calculate_entropy(self.data_dict[picked_scenario["Y"]])) / distinct_enum_X
        if score > 3:
            score = 3
        return score

    def bar_chart_score(self, grouped):
        """
        calculate Match Performance Score between Data and Bar chart
        :return: m_score_bar
        """
        picked_scenario = self.scenario_dict["%d" % (self.scenario_num-1)]
        distinct_enum_X = self.data_dict[picked_scenario["X"]]['distinct_enum']
        score = 0
        if distinct_enum_X == 1:
            score = 0
        elif distinct_enum_X >= 2 and distinct_enum_X <= 20:
            score = 3
        elif distinct_enum_X > 20:
            score = 40 / distinct_enum_X
        return score

    def scatter_chart_score(self, grouped):
        """
        calculate Match Performance Score between Data and Scatter chart
        :return: m_score_scatter
        """
        score = np.abs(np.corrcoef(grouped.keys(), grouped.values)[0][1])
        if score > 0.3:
            score = 3
        return score

    def line_chart_score(self, grouped):
        """
        calculate Match Performance Score between Data and Line chart
        :return: m_score_line
        """
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
            line_score = 3
        return line_score


    def entropy(self, prop):
        return sum(-p * math.log(p, 2) for p in prop if p is not 0)

    def class_probability(self, data):
        total_count = len(data['data'])
        return [float(count)/float(total_count) for count in Counter(data['data']).values()]

    def calculate_entropy(self, data):
        prop = self.class_probability(data)
        return self.entropy(prop)