import numpy as np
import math
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.datasets import elec_equip as ds
from pandas import DataFrame as df
import pandas as pd



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


    def get_subdimension_column(self, i):
        """
        Transform original grouped data to grouped data by sub-dimension
            1. Transform original grouped data by 'Year' to grouped data by 'Month'
            2. Transform original grouped data by 'Month' to grouped data by 'Day'
        :param i: scenario dictionary index
        :return:
        Y: transformed data
        X_unit: grouped unit of original data
        Y_shape: data size, it must be larger than MA_window * 2
        zero_ratio: # of zero value / data size
        """

        if 'year' in self.scenario_dict[i]['X']:
            X_name = self.scenario_dict[i]['X']
            X_unit = 'Year'
            X_name_sub = X_name.replace('year', 'month')
            Y_name = self.scenario_dict[i]['Y']
            agg_func = self.scenario_dict[i]['Agg_func_Y']


            wrapped = pd.DataFrame({'%s' % (X_name): self.data_dict[X_name]['data'],'%s' % (X_name_sub): self.data_dict[X_name_sub]['data'],'%s' % (Y_name): self.data_dict[Y_name]['data']})

            # print("scenario %s" % i, "*******************")

            if 'COUNT' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name, X_name_sub]).mean()

            # del wrong date key
            for key_year, key_month in Y_temp[Y_name].keys():
                if key_year == 0 or key_month == 0:
                    del Y_temp[Y_name][key_year, key_month]

            keys_temp, keys_min, keys_max = self.date_key_generation(Y_temp[Y_name], X_unit)

            # adding empty date key
            for k1, k2 in keys_temp:
                if not(k1,k2) in Y_temp[Y_name].keys():
                    Y_temp[Y_name][k1,k2] = 0

            Y = pd.DataFrame(Y_temp[Y_name])
            Y = Y.sort_index()

            Y_shape = Y.shape[0]
            count = 0
            for values in Y.values:
                if values == 0:
                    count += 1
            zero_ratio = count / Y_shape

        elif 'month' in self.scenario_dict[i]['X']:

            X_name = self.scenario_dict[i]['X']
            X_unit = 'Month'
            X_name_sub = X_name.replace('month', 'day')
            X_name_sup = X_name.replace('month', 'year')
            Y_name = self.scenario_dict[i]['Y']
            agg_func = self.scenario_dict[i]['Agg_func_Y']

            wrapped = pd.DataFrame({'%s' % (X_name_sup): self.data_dict[X_name_sup]['data'],
                                    '%s' % (X_name): self.data_dict[X_name]['data'],
                                    '%s' % (X_name_sub): self.data_dict[X_name_sub]['data'],
                                    '%s' % (Y_name): self.data_dict[Y_name]['data']})

            # print("scenario %s" % i, "*******************")

            if 'COUNT' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name_sup, X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name_sup, X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y_temp = wrapped.groupby(by=[X_name_sup, X_name, X_name_sub]).mean()

            # del wrong date key
            for key_year, key_month, key_day in Y_temp[Y_name].keys():
                if key_year == 0 or key_month == 0 or key_day == 0:
                    del Y_temp[Y_name][key_year, key_month, key_day]

            keys_temp, keys_min, keys_max = self.date_key_generation(Y_temp[Y_name], X_unit)


            # adding empty date key
            for k1, k2, k3 in keys_temp:
                if not (k1, k2, k3) in Y_temp[Y_name].keys():
                    Y_temp[Y_name][k1, k2, k3] = 0

            Y_add = pd.DataFrame(Y_temp[Y_name])
            Y_add = Y_add.sort_index()
            # print("adding empty date ********")
            # print(Y_add)

            key_year_max = keys_max[0]

            for key_year, key_month, key_day in Y_temp[Y_name].keys():
                if key_year != key_year_max:
                    del Y_add[Y_name][key_year, key_month, key_day]

            Y = pd.DataFrame(Y_add[Y_name])

            # only for group by month
            '''
            wrapped = pd.DataFrame({'%s' % (X_name): self.data_dict[X_name]['data'],
                                    '%s' % (X_name_sub): self.data_dict[X_name_sub]['data'],
                                    '%s' % (Y_name): self.data_dict[Y_name]['data']})


            print("scenario %s" % i, "*******************")

            if 'COUNT' in agg_func:
                Y_temp = wrapped.groupby(by = [X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y_temp = wrapped.groupby(by = [X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y_temp = wrapped.groupby(by = [X_name, X_name_sub]).mean()


            for key_year, key_month in Y_temp[Y_name].keys():
                if key_year == 0 or key_month == 0:
                    del Y_temp[Y_name][key_year, key_month]

            key_year_min, key_month_min = min(Y_temp[Y_name].keys())
            key_year_max, key_month_max = max(Y_temp[Y_name].keys())

            # print(Y_temp[Y_name])
            # print(key_year_min, key_month_min)
            # print(key_year_max, key_month_max)
            keys_temp = []
            month_size = [31,29,31,30,31,30,31,31,30,31,30,31]

            for temp_month in range(key_year_max-key_year_min+1):
                if temp_month == 0:
                    for temp_day in range(month_size[temp_month]-key_month_min+1):
                        keys_temp.append((key_year_min+temp_month, key_month_min+temp_day))
                elif temp_month == key_year_max-key_year_min:
                    for temp_day in range(key_month_max):
                        keys_temp.append((key_year_min+temp_month, 1+temp_day))
                else:
                    for temp2 in range(month_size[temp_month]):
                        keys_temp.append((key_year_min + temp_month, 1 + temp_day))

            for k1, k2 in keys_temp:
                if not(k1,k2) in Y_temp[Y_name].keys():
                    Y_temp[Y_name][k1,k2] = 0
            '''

            Y_shape = Y.shape[0]
            count = 0
            for values in Y[Y_name].values:
                if values == 0:
                    count += 1
            zero_ratio = count / Y_shape

            # print(Y)
            # print(zero_ratio)

        else:
            Y = 0
            X_unit = 0
            Y_shape = 0
            zero_ratio = 1

        return Y, X_unit, Y_shape, zero_ratio


    def get_scd_Score(self):

        for i in self.scenario_dict.keys():
            if 'year' or 'month' in self.scenario_dict[i]['X']:
                data, data_unit, data_size, zero_ratio = self.get_subdimension_column(i)

                if zero_ratio >= 0.2:
                    least_window = 0
                if zero_ratio < 0.2:
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
                    recent_ratio = 0.75
                    recent_point = np.multiply(nobs, recent_ratio)

                    residual_mean = np.mean(residual)
                    residual_std = np.std(residual)
                    residual_norm = (residual - residual_mean) / residual_std

                    outlier = np.where(abs(residual_norm) > 3)
                    score = 0

                    for j in range(len(outlier[0])):
                        if outlier[0][j] > recent_point:
                            score_temp = math.log(
                                math.exp(1) * (1 + (outlier[0][j] - recent_point) / (nobs - recent_point)) / 2)
                            score += score_temp

                    if score > 1.5:
                        score = 1.5

                self.scenario_dict[i]['scd_score'] = score/1.5

                if score > 0:
                    print("scenario %s" % i, "*******************")
                    print(self.scenario_dict[i])
                    print(data)
                    # plt.plot(trend)
                    # print(data, data_unit)

            else:
                # if X is not temporal data
                self.scenario_dict[i]['scd_score'] = 0
                # print(self.scenario_dict[i])

            # print(data)
            # print(self.scenario_dict[i])

        # return scd_score, score, least_window
        # return scd_score


    def date_key_generation(self, grouped, X_unit):
        """
        :param grouped:
        :param X_unit:
        :return:
        """

        if X_unit == 'Year':

            key_year_min, key_month_min = min(grouped.keys())
            keys_min = min(grouped.keys())
            key_year_max, key_month_max = max(grouped.keys())
            keys_max = max(grouped.keys())

            keys_temp = []

            # print(key_year_min, key_month_min)
            # print(key_year_max, key_month_max)

            for temp_month in range(key_year_max - key_year_min + 1):
                if temp_month == 0:
                    for temp_day in range(13 - key_month_min):
                        keys_temp.append((key_year_min + temp_month, key_month_min + temp_day))
                elif temp_month == key_year_max - key_year_min:
                    for temp_day in range(key_month_max):
                        keys_temp.append((key_year_min + temp_month, 1 + temp_day))
                else:
                    for temp_day in range(12):
                        keys_temp.append((key_year_min + temp_month, 1 + temp_day))

        elif X_unit == 'Month':

            key_year_min, key_month_min, key_day_min = min(grouped.keys())
            keys_min = min(grouped.keys())
            key_year_max, key_month_max, key_day_max = max(grouped.keys())
            keys_max = max(grouped.keys())

            keys_temp = []
            month_size = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            # print(key_year_min, key_month_min, key_day_min)
            # print(key_year_max, key_month_max, key_day_max)

            for temp_year in range(key_year_max - key_year_min + 1):
                if temp_year == 0 and key_year_max == key_year_min:
                    for temp_month in range(key_month_max - key_month_min + 1):
                        if temp_month == 0:
                            for temp_day in range(month_size[key_month_min+temp_month] - key_day_min + 1):
                                keys_temp.append((key_year_min, key_month_min + temp_month, key_day_min + temp_day))
                        elif temp_month == key_month_max - key_month_min:
                            for temp_day in range(key_day_max):
                                keys_temp.append((key_year_min, key_month_min + temp_month, 1 + temp_day))
                        else:
                            for temp_day in range(month_size[key_month_min+temp_month]):
                                keys_temp.append((key_year_min+temp_year, key_month_min + temp_month, 1 + temp_day))
                # elif temp_year == 0 and key_year_max != key_year_min:
                #     for temp_month in range(13 - key_month_min):
                #         if temp_month == 0 and key_month_min == 12:
                #             for temp_day in range(month_size[key_month_min-1] - key_day_min + 1):
                #                 keys_temp.append((key_year_min, key_month_min, key_day_min + temp_day))
                #         elif temp_month == 0 and key_month_min != 12:
                #             for temp_day in range(month_size[key_month_min+temp]):
                #                 keys_temp.append((key_year_min, key_month_min+temp_month, temp_day+1))
                #         else:
                #             for temp_day in range(month_size[temp_month]):
                #                 keys_temp.append((key_year_min+temp_year, key_month_min + temp_month, 1 + temp_day))
                elif temp_year == key_year_max - key_year_min and key_year_max != key_year_min:
                    for temp_month in range(key_month_max):
                        if temp_month == 0:
                            for temp_day in range(month_size[temp_month]):
                                keys_temp.append((key_year_min+temp_year, 1 + temp_month, 1 + temp_day))
                        elif temp_month == key_month_max:
                            for temp_day in range(key_day_max):
                                keys_temp.append((key_year_min+temp_year, 1 + temp_month, 1 + temp_day))
                        else:
                            for temp_day in range(month_size[temp_month]):
                                keys_temp.append((key_year_min+temp_year, 1 + temp_month, 1 + temp_day))
                # else:
                #     for temp_month in range(12):
                #         for temp2 in range(month_size[temp_month]):
                #             keys_temp.append((key_year_min+temp_year, temp+1, 1 + temp2))

        return keys_temp, keys_min, keys_max
