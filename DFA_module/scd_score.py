import numpy as np
import math
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.datasets import elec_equip as ds
from pandas import DataFrame as df
import pandas as pd
from matplotlib import pyplot as plt



class Special_Case_Detection():

    def __init__(self, data_dict, scenario_dict, window_year=12, window_month=28):

        self.window_year = window_year
        self.window_month = window_month
        self.bin_unit_year = 'Year'
        self.bin_unit_month = 'Month'
        self.data_dict = data_dict
        self.scenario_dict = scenario_dict

    def get_subdimension_column(self, i):

        if 'year' in self.scenario_dict[i]['X']:
            X_name = self.scenario_dict[i]['X']
            X_unit = 'Year'
            X_name_sub = X_name.replace('year', 'month')
            Y_name = self.scenario_dict[i]['Y']
            agg_func = self.scenario_dict[i]['Agg_func_Y']

            wrapped = pd.DataFrame({'%s' % (X_name): self.data_dict[X_name]['data'],
                                    '%s' % (X_name_sub): self.data_dict[X_name_sub]['data'],
                                    '%s' % (Y_name): self.data_dict[Y_name]['data']})

            if 'COUNT' in agg_func:
                Y = wrapped.groupby(by=[X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y = wrapped.groupby(by=[X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y = wrapped.groupby(by=[X_name, X_name_sub]).mean()

            Y_shape = Y.shape[0]
            count = 0
            for values in Y[Y_name].values:
                if values == 0:
                    count += 1
            zero_ratio = count / Y_shape

            null_ratio = 0
            # null_ratio = np.divide(Y.isnull().sum(), Y_shape)

            print("null test ", Y[Y_name].isnull().sum())

        elif 'month' in self.scenario_dict[i]['X']:

            X_name_sub = self.scenario_dict[i]['X']
            X_unit = 'Year'
            X_name = X_name_sub.replace('month', 'year')
            Y_name = self.scenario_dict[i]['Y']
            agg_func = self.scenario_dict[i]['Agg_func_Y']


            # X_name = self.scenario_dict[i]['X']
            # X_unit = 'Month'
            # X_name_sub = X_name.replace('month', 'day')
            # Y_name = self.scenario_dict[i]['Y']
            # agg_func = self.scenario_dict[i]['Agg_func_Y']

            wrapped = pd.DataFrame({'%s' % (X_name): self.data_dict[X_name]['data'], '%s' % (X_name_sub): self.data_dict[X_name_sub]['data'],'%s' % (Y_name): self.data_dict[Y_name]['data']})

            if 'COUNT' in agg_func:
                Y = wrapped.groupby(by = [X_name, X_name_sub]).count()
            if 'SUM' in agg_func:
                Y = wrapped.groupby(by = [X_name, X_name_sub]).sum()
            if 'AVG' in agg_func:
                Y = wrapped.groupby(by = [X_name, X_name_sub]).mean()

            Y_shape = Y.shape[0]
            count = 0
            for values in Y[Y_name].values:
                if values == 0:
                    count += 1
            zero_ratio = count / Y_shape
            null_ratio = 0
            print("scenario %s" %i, "*******************")
            print("null test ", Y[Y_name].isnull().sum())
            print(Y[Y_name])
            # null_ratio = np.divide(Y.isnull().sum(), Y_shape)
        else:
            Y = 0
            X_unit = 0
            Y_shape = 0
            zero_ratio = 1
            null_ratio = 1

        return Y, X_unit, Y_shape, zero_ratio, null_ratio


    def get_scd_Score(self):

        for i in self.scenario_dict.keys():
            if 'year' or 'month' in self.scenario_dict[i]['X']:
                data, data_unit, data_size, zero_ratio, null_ratio = self.get_subdimension_column(i)

                if zero_ratio >= 0.2 or null_ratio > 0.2:
                    least_window = 0
                if zero_ratio < 0.2 and null_ratio < 0.2:
                    if data_unit == self.bin_unit_year:
                        if data_size < self.window_year * 2:
                            least_window = 0
                        if data_size >= self.window_year * 2:
                            # if data_temp.count(0) >= np.multiply(data_temp.shape[0], 0.1):
                            #     least_window = 0
                            # if data_temp.count(0) < np.multiply(data_temp.shape[0], 0.1):
                            least_window = 1
                            stl = seasonal_decompose(data, model='additive', period=self.window_year)
                            # stl = seasonal_decompose(data, model='multiplicative', period=self.window_year)
                    elif data_unit == self.bin_unit_month:
                        if data_size < self.window_month * 2:
                            least_window = 0
                        if data_size >= self.window_month * 2:
                            # if data_temp.count(0) >= np.multiply(data_temp.shape[0], 0.1):
                            #     least_window = 0
                            # if data_temp.count(0) < np.multiply(data_temp.shape[0], 0.1):
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
                        score = 2

                self.scenario_dict[i]['scd_score'] = score/1.5

                if score > 0:
                    print(self.scenario_dict[i])
                    print(trend)
                    # plt.plot(trend)
                    # print(data, data_unit)

            else:
                # if X is not temporal data
                self.scenario_dict[i]['scd_score'] = 0
                # print(self.scenario_dict[i])

        # return scd_score, score, least_window
        # return scd_score

