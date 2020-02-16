import numpy as np
import pandas as pd


class CreateDataFrame():
    #def __init__(self, csv_data, column1, column2, agg_func):
    def __init__(self, csv_data, scenario_dict, data_dict):

        self.csv_data = csv_data
        self.scenario_dict = scenario_dict
        self.data_dict = data_dict
        self.data = pd.read_csv(self.csv_data)

    def find_column_info_agg_func(self):

        # X_temp = self.scenario_dict['X']
        # X_type = self.data_dict[X_temp]['data_type']
        # Y_temp = self.scenario_dict['Y']
        # Y_type = self.data_dict[Y_temp]['data_type']
        # Agg_func_temp = self.scenario_dict['Agg_func']

        self.X = self.scenario_dict['X']
        self.Y = self.scenario_dict['Y']
        self.agg_func = self.scenario_dict['Agg_func']
        self.X_type = self.data_dict[self.X]['data_type']
        self.Y_type = self.data_dict[self.Y]['data_type']

        print("X_temp: ", self.X, self.X_type)
        print("Y_temp: ", self.Y, self.Y_type)

        print("scenario_dict:", self.scenario_dict)
        # print("combination_dict: ", column_combination[i])


    def transformation(self):

        self.find_column_info_agg_func()

        for items in self.data.columns:
            if items in self.X:
                self.X_name = items
                if 'year' in self.X:
                    self.X_unit = 'Year'
                if 'month' in self.X:
                    self.X_unit = 'Month'
                # if 'day' in self.X:
                #     self.X_unit = 'Day'
            if items in self.Y:
                self.Y_name = items

        wrapped_data = pd.DataFrame({self.X_name : self.data[self.X_name], self.Y_name : self.data[self.Y_name]})

        # wrapped_data = wrapped_data.dropna(axis = self.Y_name)
        # print(wrapped_data)

        wrapped_data[self.X_name] = pd.to_datetime(wrapped_data[self.X_name])
        wrapped_data = wrapped_data.set_index(wrapped_data[self.X_name])
        # wrapped_data.drop(X_name)
        # print(wrapped_data)

        if 'avg' in self.agg_func:
            #grouped = wrapped_data[Y_name].groupby(wrapped_data[X_name]).mean()
            #grouped = wrapped_data[Y_name].resample('MS').mean()
            if self.X_unit == 'Year':
                grouped = wrapped_data[self.Y_name].resample('MS').mean()
            if self.X_unit == 'Month':
                grouped = wrapped_data[self.Y_name].resample('W').mean()

        if 'sum' in self.agg_func:
            #grouped = wrapped_data[Y_name].groupby(wrapped_data[X_name]).sum()
            #grouped = wrapped_data[Y_name].groupby(wrapped_data[X_name]).sum()
            if self.X_unit == 'Year':
                grouped = wrapped_data[self.Y_name].resample('MS').sum()
            if self.X_unit == 'Month':
                grouped = wrapped_data[self.Y_name].resample('W').sum()
        if 'count' in self.agg_func:
            #grouped1 = wrapped_data[Y_name].groupby(wrapped_data[X_name]).count()
            # grouped = wrapped_data[Y_name].groupby(wrapped_data[X_name]).count()
            if self.X_unit == 'Year':
                grouped = wrapped_data[self.Y_name].resample('MS').count()
            if self.X_unit == 'Month':
                grouped = wrapped_data[self.Y_name].resample('W').count()

        # print(grouped)
        # grouped = grouped.set_index(X_name)

        #temp = grouped[0].set_index(grouped[X_name], inplace=True)

        size = grouped.shape[0]
        null_ratio = np.divide(grouped.isnull().sum(), size)

        binUnit = self.X_unit
        grouped = grouped.fillna(0)

        print("null_ratio: ", null_ratio)
        print("size: ", size)

        return grouped, binUnit, null_ratio

