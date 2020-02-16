import numpy as np
import math
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.datasets import elec_equip as ds
from pandas import DataFrame as df



class Special_Case_Detection():

    def __init__(self, data, binUnit, null_ratio, window_year = 12, window_month = 7):

        self.window_year = window_year
        self.window_month = window_month
        self.bin_unit_year = 'Year'
        self.bin_unit_month = 'Month'
        self.binUnit = binUnit
        self.data = data
        self.null_ratio = null_ratio

    def get_scd_Score(self):

        #binUnit_temp = 'Year'
        binUnit_temp = self.binUnit

        #data_temp = ds.load(as_pandas=True).data
        data_temp = self.data

        if self.null_ratio >= 0.3:
            least_window = 0
        if self.null_ratio < 0.3:
            if binUnit_temp == self.bin_unit_year:
                if data_temp.shape[0] < self.window_year*2:
                    least_window = 0
                if data_temp.shape[0] >= self.window_year*2:
                    # if data_temp.count(0) >= np.multiply(data_temp.shape[0], 0.1):
                    #     least_window = 0
                    # if data_temp.count(0) < np.multiply(data_temp.shape[0], 0.1):
                        least_window = 1
                        stl = seasonal_decompose(data_temp, model='additive', period = self.window_year)
            elif binUnit_temp == self.bin_unit_month:
                if data_temp.shape[0] < self.window_month*2:
                    least_window = 0
                if data_temp.shape[0] >= self.window_month*2:
                    # if data_temp.count(0) >= np.multiply(data_temp.shape[0], 0.1):
                    #     least_window = 0
                    # if data_temp.count(0) < np.multiply(data_temp.shape[0], 0.1):
                        least_window = 1
                        stl = seasonal_decompose(data_temp, model='additive', period = self.window_month)
            else:
                print("stl window error")

        '''
        if binUnit == self.bin_unit_year:
            stl = seasonal_decompose(data, model='additive', period = self.window_year)
        elif binUnit == self.bin_unit_month:
            stl = seasonal_decompose(data, model='additive', period = self.window_month)
        else
            print("stl window error")
        '''

        if least_window == 0:
            score = 0
            scd_score = 0
        if least_window == 1:
            residual = stl.resid
            nobs = stl.nobs
            recent_ratio = 0.75
            recent_point = np.multiply(nobs, recent_ratio)

            residual_mean = np.mean(residual)
            residual_std = np.std(residual)
            residual_norm = (residual - residual_mean)/residual_std

            outlier = np.where(abs(residual_norm) > 3)
            score = []

            for i in range(len(outlier[0])):
                if outlier[0][i] > recent_point:
                    score_temp = math.log(math.exp(1)*(1+(outlier[0][i]-recent_point)/(nobs-recent_point))/2)
                    score.append(score_temp)
                else:
                    score.append(0)

            scd_score = sum(score)

        return scd_score, score, least_window
