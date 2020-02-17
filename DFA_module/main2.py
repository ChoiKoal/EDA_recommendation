import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
from create_dictionary import CreateDictionary
from column_combination import ColumnCombination
from transformation import Transformation
from scd_score import Special_Case_Detection
from statsmodels.datasets import elec_equip as ds
from Create_SCD_df import CreateDataFrame
import pandas as pd


if __name__ == "__main__":

    f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()
    csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"]

    #Create Column Data Dictionary
    data_dict = CreateDictionary(csv_data, csv_contents_type).initialize_dic()

    #Create Column Combination
    column_combination = ColumnCombination(data_dict).create_combination()

    print ("Column combination Created.")

    scenario_dict = {}
    Transformation(data_dict, column_combination, scenario_dict).transformation()

    # elect
    data_temp = ds.load(as_pandas=True).data
    temp_null = 0
    scd_score = Special_Case_Detection(data_temp, 'Year', temp_null).get_scd_Score()

    print(scd_score)



    for i in scenario_dict.keys():
        if 'year' in scenario_dict[i]['transform']:
            print(i, "th result *************************")

            data = CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict)
            temp_data, binUnit, null_ratio = data.transformation()

            temp_score, temp_score1, least_window = Special_Case_Detection(temp_data, binUnit, null_ratio).get_scd_Score()
            # temp_score, temp_score1 = Special_Case_Detection(data.transformation()).get_scd_Score()


            # temp_score, temp_score1 = Special_Case_Detection(CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict).transformation()).get_scd_Score()

            print(temp_score, temp_score1, least_window)

        elif 'month' in scenario_dict[i]['transform']:
            print(i, "th result *************************")

            data = CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict)
            temp_data, binUnit, null_ratio = data.transformation()

            temp_score, temp_score1, least_window = Special_Case_Detection(temp_data, binUnit,
                                                                           null_ratio).get_scd_Score()
            # temp_score, temp_score1 = Special_Case_Detection(data.transformation()).get_scd_Score()

            # temp_score, temp_score1 = Special_Case_Detection(CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict).transformation()).get_scd_Score()

            print(temp_score, temp_score1, least_window)







