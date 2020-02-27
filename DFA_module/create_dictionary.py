import numpy as np
from collections import Counter

class CreateDictionary():
    def __init__(self, csv_data, data_type_meta):
        """

        :param csv_data: raw data table
        :param data_type_meta: data type of each column (Temporal, Numerical, Categorical)
        """

        self.csv_data = csv_data
        self.data_type_meta = data_type_meta

    def initialize_dic(self):
        """
        column dictionary :
        "data" : column data
        "data_type" : column data type
        "avg" : column data average (if "data_type" = numerical)
        "min" : column data minimum (if "data_type" = numerical)
        "max" : column data maximum (if "data_type" = numerical)
        "trend" : column data trend value
        :return:
        """
        csv_contents = self.csv_data[0]
        csv_data_table = self.csv_data[1:]

        count = 0
        column_dic = {}
        for item in csv_contents:
            column_dic[item] = {}
            column_dic[item]["data"] = np.transpose(csv_data_table)[count]
            column_dic[item]["data_type"] = self.data_type_meta[count]
            column_dic[item]["isnull"] = np.zeros(len(column_dic[item]["data"]), dtype=bool)
            column_dic[item]["distinct_enum"] = len(Counter(column_dic[item]["data"]))
            enum = len(column_dic[item]["data"])
            for i in range(len(column_dic[item]["data"])):
                if column_dic[item]["data"][i] == "":
                    column_dic[item]["isnull"][i] = True
                    enum -= 1
            column_dic[item]["enum"] = enum


            if column_dic[item]["data_type"] == "num":
                column_dic[item] = self.create_numerical_dic(column_dic[item])

            if column_dic[item]["data_type"] == "tem":
                column_dic[item]["year"] = []
                column_dic[item]["month"] = []
                column_dic[item]["day"] = []
                column_dic[item]["year+month"] = []
                column_dic[item] = self.create_temporal_dic(column_dic[item])

                column_dic[item + ",year"] = {}
                column_dic[item + ",year"]["data"] = column_dic[item]["year"]
                column_dic[item + ",year"]["data_type"] = "tem"
                column_dic[item + ",year"]["enum"] = column_dic[item]["enum"]
                column_dic[item + ",year"]["isnull"] = column_dic[item]["isnull"]
                column_dic[item + ",year"]["distinct_enum"] = len(Counter(column_dic[item + ",year"]["data"]))

                column_dic[item + ",month"] = {}
                column_dic[item + ",month"]["data"] = column_dic[item]["month"]
                column_dic[item + ",month"]["data_type"] = "tem"
                column_dic[item + ",month"]["enum"] = column_dic[item]["enum"]
                column_dic[item + ",month"]["isnull"] = column_dic[item]["isnull"]
                column_dic[item + ",month"]["distinct_enum"] = len(Counter(column_dic[item + ",month"]["data"]))

                column_dic[item + ",day"] = {}
                column_dic[item + ",day"]["data"] = column_dic[item]["day"]
                column_dic[item + ",day"]["data_type"] = "tem"
                column_dic[item + ",day"]["enum"] = column_dic[item]["enum"]
                column_dic[item + ",day"]["isnull"] = column_dic[item]["isnull"]
                column_dic[item + ",day"]["distinct_enum"] = len(Counter(column_dic[item + ",day"]["data"]))


                column_dic[item + ",year+month"] = {}
                column_dic[item + ",year+month"]["data"] = column_dic[item]["year+month"]
                column_dic[item + ",year+month"]["data_type"] = "tem"
                column_dic[item + ",year+month"]["enum"] = column_dic[item]["enum"]
                column_dic[item + ",year+month"]["isnull"] = column_dic[item]["isnull"]
                column_dic[item + ",year+month"]["distinct_enum"] = len(Counter(column_dic[item + ",year+month"]["data"]))


                del column_dic[item]
            count += 1


        return column_dic

    def create_numerical_dic(self, column):
        """
        get statistical meta info
        :param column:
        column: numerical column
        :return: column
        """
        for i in range(len(column["data"])):
            if column["data"][i] == "":
                column["isnull"][i] = True
                column["data"][i] = "0"
        column["data"] = column["data"].astype(float)
        column["avg"] = self.calculate_Avg(column["data"])
        column["min"], column["max"], column["std"], column["var"], \
        column["qua_1"], column["med"], column["qua_3"] = self.calculate_Stat(
            column["data"])
        column["qua_range"] = column["qua_3"] - column["qua_1"]
        return column

    def create_temporal_dic(self, column):
        """
        get temporal data meta
        parsing with delimeter (global rule : "-")
        Y, D, M : type casting to int
        year+month : str type
        :param column: temporal column
        :return: column
        """
        # for enum in range(len(column['data'])):
        #     if column['isnull'][enum] != True:
        #         column['month'].append(int(column['data'][enum].split("/")[0]))
        #         column['day'].append(int(column['data'][enum].split("/")[1]))
        #         column['year'].append(int(column['data'][enum].split("/")[2]))
        #         column['year+month'].append(column['data'][enum].split("/")[2] + " " + column['data'][enum].split("/")[0])
        #     else:
        #         column['year'].append(0)
        #         column['month'].append(0)
        #         column['day'].append(0)
        #         column['year+month'].append(0)
        # return column
        for enum in range(len(column['data'])):
            if column['isnull'][enum] != True:
                column['year'].append(int(column['data'][enum].split("-")[0]))
                column['month'].append(int(column['data'][enum].split("-")[1]))
                column['day'].append(int(column['data'][enum].split("-")[2]))
                column['year+month'].append(column['data'][enum].split("-")[0] + " " + column['data'][enum].split("-")[1])
            else:
                column['year'].append(0)
                column['month'].append(0)
                column['day'].append(0)
                column['year+month'].append(0)

        return column
        # for enum in range(len(column['data'])):
        #     if column['isnull'][enum] != True:
        #         column['year'].append(int(column['data'][enum].split(".")[0]))
        #         column['month'].append(int(column['data'][enum].split(".")[1]))
        #         column['day'].append(int(column['data'][enum].split(".")[2]))
        #         column['year+month'].append(column['data'][enum].split(".")[0] + " " + column['data'][enum].split(".")[1])
        #     else:
        #         column['year'].append(0)
        #         column['month'].append(0)
        #         column['day'].append(0)
        #         column['year+month'].append(0)
        #
        # return column

    def calculate_Avg(self, column):
        """
        enum : count nonzero elements
        avg : calculate average of nonzero elements
        :param column: input column
        :return: enum, avg
        """
        avg = np.sum(column)/np.count_nonzero(column)
        return avg

    def create_nonzero_column(self, column):
        """
        create nonzero column for calculate statistical info
        :param column: column
        :return: nonzero column
        """
        nonzero_index = np.nonzero(column)
        nonzero_column = []
        for item in nonzero_index:
            nonzero_column.append(column[item])
        return nonzero_column

    def calculate_Stat(self, column):
        """
        min, max, std, var : statistical data of column
        qua_1, med, qua_3 : quantile(0.25, 0.5, 0.75) of column data
        :param column: input column
        :return: min, max, std, var, qua_1, med, qua_3
        """
        nonzero_column = self.create_nonzero_column(column)
        qua_1 = np.quantile(nonzero_column, 0.25)
        med = np.quantile(nonzero_column, 0.5)
        qua_3 = np.quantile(nonzero_column, 0.75)
        min = np.min(nonzero_column)
        max = np.max(nonzero_column)
        std = np.std(nonzero_column)
        var = np.var(nonzero_column)
        return min, max, std, var, qua_1, med, qua_3
