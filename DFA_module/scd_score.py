import numpy as np
import math
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.datasets import elec_equip as ds
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import pandas as pd
import time



class Special_Case_Detection():

    def __init__(self, data_dict, scenario_dict, window_year=12, window_month=28):
        """
        :param data_dict: data dictionary
        :param scenario_dict: scenario dictionary
        :param window_year: year window for Moving average
        :param window_month: month window for Moving average
        """


        self.window_year = window_year
        self.window_month = window_month
        self.bin_unit_year = 'Year'
        self.bin_unit_month = 'Month'
        self.data_dict = data_dict
        self.scenario_dict = scenario_dict

    def get_subdimension_column(self, i, date_dictionary):
        """
        Transform original grouped data to grouped data by sub-dimension
            Transform original grouped data by 'Year' to grouped data by 'Month'
        :param i: scenario dictionary index
        :param date_dictionary: date_key dictionary to deal with empty date
        :return:
        Y: transformed data
        X_unit: grouped unit of original data
        Y_shape: data size, it must be larger than MA_window * 2
        zero_ratio: # of zero value / data size
        """

        if 'year+month' in self.scenario_dict[i]['X']:

            X = self.scenario_dict[i]['X']
            X_name = self.scenario_dict[i]['X'].split(',')[0] + 'Year'
            X_name_sub = self.scenario_dict[i]['X'].split(',')[0] + 'Month'
            X_unit = 'Year'
            Y_name = self.scenario_dict[i]['Y']
            Y_type = self.data_dict[Y_name]['data_type']
            agg_func = self.scenario_dict[i]['Agg_func_Y']


            time_data_copy1 = time.time()
            col = {}
            col[X_name] = []
            col[X_name_sub] = []
            col[Y_name] = []
            for enum in range(len(self.data_dict[X]['data'])):
                if self.data_dict[X]['data'][enum] != 0:
                    col[X_name].append(int(self.data_dict[X]['data'][enum].split(' ')[0]))
                    col[X_name_sub].append(int(self.data_dict[X]['data'][enum].split(' ')[1]))
                    if not self.data_dict[Y_name]['isnull'][enum]:
                        col[Y_name].append(self.data_dict[Y_name]['data'][enum])
                    else:
                        col[Y_name].append(None)
                        # col[Y_name].append(0)
                else:
                    col[X_name].append(0)
                    col[X_name_sub].append(0)
                    col[Y_name].append(0)

            wrapped = pd.DataFrame(col)
            # wrapped.fillna(method = 'ffill', inplace=True)
            if Y_type == 'tem':
                wrapped.fillna(method='ffill', inplace=True)
                wrapped.fillna(method='bfill', inplace=True)
            else:
                wrapped.interpolate(inplace=True)

            if 'COUNT' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).mean()

            for key_year, key_month in Y_temp[Y_name].keys():
                if key_year == 0 or key_month == 0:
                    del Y_temp[Y_name][key_year, key_month]
                elif key_year < min(date_dictionary[X].keys())[0]:
                    del Y_temp[Y_name][key_year, key_month]

            Y_dict = Y_temp[Y_name].to_dict()
            #
            # min_date_year, min_date_month = list(zip(Y_dict.keys()))[0][0]
            # max_date_year, max_date_month = list(zip(Y_dict.keys()))[len(Y_dict.keys()) - 1][0]

            # date_dictionary_keys = date_dictionary[X].keys()
            # for date_key_year, date_key_month in date_dictionary_keys:
            #     if date_key_year > max_date_year and date_key_month > max_date_month:
            #         del date_dictionary[X][date_key_year, date_key_month]
            #     if date_key_year < min_date_year and date_key_month < min_date_month:
            #         del date_dictionary[X][date_key_year, date_key_month]

            date_dictionary[X].update(Y_dict)

            Y = pd.DataFrame.from_dict(date_dictionary[X], orient='index')
            # Y.interpolate(inplace=True)
            # # Y.fillna(method='ffill', limit = 20, inplace=True)
            # Y.fillna(method='bfill', inplace=True)
            Y.fillna(0, inplace=True)

            time_data_copy2 = time.time()
            time_data_copy = time_data_copy2 - time_data_copy1

            Y_shape = Y.shape[0]
            count = 0
            for values in Y.values:
                if values == 0:
                    count += 1
            zero_ratio = count / Y_shape

        else:
            Y = 0
            X_unit = 0
            Y_shape = 0
            zero_ratio = 1

        return Y, X_unit, Y_shape, zero_ratio


    def get_scd_Score(self):
        """
        Special Case Detection score
        """
        date_dictionary = self.full_date_key_generation()
        scene = []
        scene_score = []

        for i in self.scenario_dict.keys():

            if 'year' or 'month' in self.scenario_dict[i]['X']:

                runtime3 = time.time()

                data, data_unit, data_size, zero_ratio = self.get_subdimension_column(i, date_dictionary)

                if zero_ratio >= 0.5:
                    least_window = 0
                if zero_ratio < 0.5:
                    if data_unit == self.bin_unit_year:
                        if data_size < self.window_year * 2:
                            least_window = 0
                        if data_size >= self.window_year * 2:
                            least_window = 1
                            stl = seasonal_decompose(data, model='additive', period=self.window_year)
                            # stl = seasonal_decompose(data, model='multiplicative', period=self.window_year)
                    elif data_unit == self.bin_unit_month:
                        if data_size < self.window_month * 2:
                            least_window = 0
                        if data_size >= self.window_month * 2:
                            least_window = 1
                            stl = seasonal_decompose(data, model='additive', period=self.window_month)
                            # stl = seasonal_decompose(data, model='multiplicative', period=self.window_year)
                    else:
                        print("stl window error")

                if least_window == 0:
                    score = 0
                    self.scenario_dict[i]['scd_score'] = score
                if least_window == 1:
                    trend = stl.trend
                    seasonal = stl.seasonal
                    residual = stl.resid
                    nobs = stl.nobs

                    # if nobs[0] > 240:
                    #     recent_ratio = 0.95
                    # elif nobs[0] > 120:
                    #     recent_ratio = 0.9
                    # elif nobs[0] > 60:
                    #     recent_ratio = 0.8
                    # else:
                    #     recent_ratio = 0.75
                    recent_ratio = 0.5

                    recent_point = np.multiply(nobs, recent_ratio)

                    residual_mean = np.mean(residual)
                    residual_std = np.std(residual)
                    residual_norm = (residual - residual_mean) / residual_std

                    outlier = np.where(abs(residual_norm) > 3)
                    score = 0
                    score_dict = {}
                    count = 0
                    for j in range(len(outlier[0])):
                        # if outlier[0][j] > recent_point and outlier[0][j] < len(nobs) - 6:
                        if outlier[0][j] > recent_point:
                            score_temp = math.log(
                                math.exp(1) * (1 + (outlier[0][j] - recent_point) / (nobs - recent_point)) / 2)
                            score += score_temp
                            score_dict[count] = score_temp
                            count += 1

                    if score > 2:
                        score = 2

                    scene.append(i)

                self.scenario_dict[i]['scd_score'] = score/2

                runtime4 = time.time()

                if score == 2:
                    print("************* score 2 **********************************************")
                if score > 0:
                    # print(i, "scenario scd time *****************************************")
                    # print("score : " , score/2)
                    # print("each score :", score_dict)
                    # print("runtime : ",runtime4 - runtime3)
                    # print("data")
                    scene_score.append(i)
                    #
                    # fig = plt.figure()
                    # ax1 = fig.add_subplot(4,1,1)
                    # ax1.plot(data.values)
                    # ax2 = fig.add_subplot(4,1,2)
                    # ax2.plot(trend.values)
                    # ax3 = fig.add_subplot(4,1,3)
                    # ax3.plot(seasonal.values)
                    # ax4 = fig.add_subplot(4,1,4)
                    # ax4.plot(residual_norm.values)
                    # plt.show()

            else:
                self.scenario_dict[i]['scd_score'] = 0

        return scene, scene_score

    def full_date_key_generation(self):
        """
        date key generation for empty date
        :return: date_dictionary
        """
        date_dictionary = {}

        for item in self.data_dict.keys():
            if 'year+month' in item:

                date_dictionary[item] = {}
                date_list = []
                for date in self.data_dict[item]['data']:
                    if date != 0:
                        date_list.append((int(date.split(" ")[0]), int(date.split(" ")[1])))

                key_year_min, key_month_min = min(date_list)
                key_year_max, key_month_max = max(date_list)

                if key_year_max - key_year_min > 20:
                    key_year_min = key_year_max - 20
                    key_month_min = 1

                for temp_year in range(key_year_max - key_year_min + 1):
                    if temp_year == 0 and key_year_max == key_year_min:
                        for temp_month in range(key_month_max - key_month_min + 1):
                            month = temp_month + key_month_min
                            date = (key_year_min, month)
                            # date_dictionary[item][date] = 0
                            date_dictionary[item][date] = None
                    elif temp_year == 0 and key_year_max != key_year_min:
                        for temp_month in range(12 - key_month_min + 1):
                            month = temp_month + key_month_min
                            date = (key_year_min, month)
                            # date_dictionary[item][date] = 0
                            date_dictionary[item][date] = None
                    elif temp_year == key_year_max - key_year_min:
                        for temp_month in range(key_month_max):
                            month = temp_month + 1
                            date = (key_year_max, month)
                            # date_dictionary[item][date] = 0
                            date_dictionary[item][date] = None
                    else:
                        for temp_month in range(12):
                            year = key_year_min + temp_year
                            month = temp_month + 1
                            date = (year, month)
                            # date_dictionary[item][date] = 0
                            date_dictionary[item][date] = None

        return date_dictionary