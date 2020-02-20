import numpy as np


class ColumnCombination():
    def __init__(self, data_dictionary):
        """
        :param data_dictionary : data dictionary
        :param data_name : data name
        :param data_type : either tem, num, cat
        :param columnset_dict : combination of columns
        :param combination_num : enum combinations
        """

        self.data_dictionary = data_dictionary
        self.data_name = np.array(list(self.data_dictionary.keys()))
        self.data_type = []
        for i in range(len(self.data_name)):
            self.data_type.append(self.data_dictionary[self.data_name[i]]['data_type'])
        self.columnset_dict = {}
        self.combination_num = 0


    def create_combination(self):
        """
        create 2~3 columns combination
        """
        for i in range(len(self.data_name)):
            for j in range(len(self.data_name)):
                if i < j:
                    self.combination_2column(self.combination_num, self.data_name[i], self.data_name[j])

        for i in range(len(self.data_name)):
            for j in range(len(self.data_name)):
                for k in range(len(self.data_name)):
                    if i<j and j<k:
                        self.combination_3column(self.combination_num, self.data_name[i], self.data_name[j], self.data_name[k])
        return self.columnset_dict

    def combination_2column(self, num, column_1, column_2):
        """
        2column combination
        :param num: combination_num
        :param column_1: picked column1
        :param column_2: picked column2
        :return:
        """
        self.columnset_dict["%d" %num] = {}
        self.columnset_dict["%d" %num]["column1"] = column_1
        self.columnset_dict["%d" %num]["column2"] = column_2
        self.columnset_dict["%d" %num]["column_count"] = 2
        self.combination_num += 1

    def combination_3column(self, num, column_1, column_2, column_3):
        """
        3column combination
        :param num: combination num
        :param column_1: picked column1
        :param column_2: picked column2
        :param column_3: picked column3
        :return:
        """
        self.columnset_dict["%d" %num] = {}
        self.columnset_dict["%d" %num]["column1"] = column_1
        self.columnset_dict["%d" %num]["column2"] = column_2
        self.columnset_dict["%d" %num]["column3"] = column_3
        self.columnset_dict["%d" %num]["column_count"] = 3
        self.combination_num += 1
