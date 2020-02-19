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
# <<<<<<< HEAD
from scd_score import Special_Case_Detection
from statsmodels.datasets import elec_equip as ds
from Create_SCD_df import CreateDataFrame
import pandas as pd

# =======
from rank import Rank
import time
# >>>>>>> 5693a6a3d1709a7b4c8004b0ebab9fbf890fd26f

if __name__ == "__main__":


    # f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    f = open("./tmax_raw_data.csv", 'r', encoding='utf-8')
    # f = open("./carcrash.csv", 'r', encoding='utf-8')
    # f = open("./traffic_accident.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()

    # csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"] #tmaxday
    csv_contents_type = ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "tem", "tem", "num", "cat", "num", "num", "num", "cat"]  #tmax_raw_data_set
    # csv_contents_type = ["cat", "cat", "cat", "cat", "num", "num", "num", "num", "num", "num"] #carcrash
    # csv_contents_type = ["cat", "tem", "cat", "cat", "cat", "cat", "num", "num", "num", "num", "num", "num", "num", "num"]


    startTime = time.time()
    #Create Column Data Dictionary
    data_dict = CreateDictionary(csv_data, csv_contents_type).initialize_dic()
    runtime = time.time()
    print ("Runtime : %.4f" % (runtime-startTime))

    #Create Column Combination
    column_combination = ColumnCombination(data_dict).create_combination()

    print ("Column combination Created.")
    runtime2 = time.time()
    print("Runtime : %.4f" % (runtime2 - runtime))


# <<<<<<< HEAD
#     # elect
#     data_temp = ds.load(as_pandas=True).data
#     temp_null = 0
#     scd_score = Special_Case_Detection(data_temp, 'Year', temp_null).get_scd_Score()
#
#     print(scd_score)
#
#
#
#     for i in scenario_dict.keys():
#         if 'year' in scenario_dict[i]['transform']:
#             print(i, "th result *************************")
#
#             data = CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict)
#             temp_data, binUnit, null_ratio = data.transformation()
#
#             temp_score, temp_score1, least_window = Special_Case_Detection(temp_data, binUnit, null_ratio).get_scd_Score()
#             # temp_score, temp_score1 = Special_Case_Detection(data.transformation()).get_scd_Score()
#
#
#             # temp_score, temp_score1 = Special_Case_Detection(CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict).transformation()).get_scd_Score()
#
#             print(temp_score, temp_score1, least_window)
#
#         elif 'month' in scenario_dict[i]['transform']:
#             print(i, "th result *************************")
#
#             data = CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict)
#             temp_data, binUnit, null_ratio = data.transformation()
#
#             temp_score, temp_score1, least_window = Special_Case_Detection(temp_data, binUnit,
#                                                                            null_ratio).get_scd_Score()
#             # temp_score, temp_score1 = Special_Case_Detection(data.transformation()).get_scd_Score()
#
#             # temp_score, temp_score1 = Special_Case_Detection(CreateDataFrame("./TmaxDay_data.csv", scenario_dict[i], data_dict).transformation()).get_scd_Score()
#
#             print(temp_score, temp_score1, least_window)
#
#
#
# =======
    scenario_dict = Transformation(data_dict, column_combination).transformation()

    print ("Scenario dictionary created")
    runtime3 = time.time()
    print("Runtime : %.4f" % (runtime3 - runtime2))

    Special_Case_Detection(data_dict, scenario_dict).get_scd_Score()



    '''
    for i in scenario_dict.keys():
        # if i == '1':

            if 'year' in scenario_dict[i]['X']:
                # print(i, "th result *************************")
                # print(scenario_dict[i])
                X_name = scenario_dict[i]['X']
                X_unit = 'Year'
                X_name_sub = X_name.replace('year', 'month')
                Y_name = scenario_dict[i]['Y']
                agg_func = scenario_dict[i]['Agg_func_Y']

                # print(X_unit, X_name, Y_name, agg_func)
                wrapped = pd.DataFrame({'%s' %(X_name) : data_dict[X_name]['data'], '%s' %(X_name_sub) : data_dict[X_name_sub]['data'], '%s' %(Y_name): data_dict[Y_name]['data']})
                # print("wraaped : ")
                # print(wrapped)

                if 'COUNT' in agg_func:
                    Y = wrapped.groupby(by = [X_name, X_name_sub]).count()
                if 'SUM' in agg_func:
                    Y = wrapped.groupby(by=[X_name, X_name_sub]).sum()
                if 'AVG' in agg_func:
                    Y = wrapped.groupby(by=[X_name, X_name_sub]).mean()

                # print("Y : ")


                # scd_score, score, least_window = Special_Case_Detection(Y, 'Year', 0).get_scd_Score()
                scd_score = Special_Case_Detection(Y, X_unit, 0).get_scd_Score()
                if scd_score > 0:

                    count = 0
                    for values in Y[Y_name].values:
                        if values == 0:
                            count += 1
                    zero_ratio = count / Y.shape[0]

                    if zero_ratio < 0.2:
                        print(i, "th result *************************")
                        print(scenario_dict[i])
                        print(scd_score)
                        print(Y)

            if 'month' in scenario_dict[i]['X']:
                # print(i, "th result *************************")
                # print(scenario_dict[i])
                X_name = scenario_dict[i]['X']
                X_unit = 'Month'
                X_name_sub = X_name.replace('month', 'day')
                Y_name = scenario_dict[i]['Y']
                agg_func = scenario_dict[i]['Agg_func_Y']

                # print(X_unit, X_name, Y_name, agg_func)
                wrapped = pd.DataFrame({'%s' %(X_name) : data_dict[X_name]['data'], '%s' %(X_name_sub) : data_dict[X_name_sub]['data'], '%s' %(Y_name): data_dict[Y_name]['data']})
                # print("wraaped : ")
                # print(wrapped)

                if 'COUNT' in agg_func:
                    Y = wrapped.groupby(by = [X_name, X_name_sub]).count()
                if 'SUM' in agg_func:
                    Y = wrapped.groupby(by=[X_name, X_name_sub]).sum()
                if 'AVG' in agg_func:
                    Y = wrapped.groupby(by=[X_name, X_name_sub]).mean()

                # print("Y : ")



                # scd_score, score, least_window = Special_Case_Detection(Y, 'Year', 0).get_scd_Score()
                scd_score = Special_Case_Detection(Y, X_unit, 0).get_scd_Score()
                if scd_score > 0:
                    # print(i, "th result *************************")
                    # print(scenario_dict[i])
                    # print(scd_score)
                    # print(Y)
                    # print(Y[Y_name])
                    # print(Y[Y_name][1,1])
                    # print(Y.shape[0])

                    count = 0
                    for values in Y[Y_name].values:
                        if values == 0:
                            count += 1
                    zero_ratio = count/Y.shape[0]

                    if zero_ratio < 0.2:
                        print(i, "th result *************************")
                        print(scenario_dict[i])
                        print(scd_score)
                        print(Y)
    '''



    Rank(scenario_dict).rank()



    endTime = time.time() - startTime


    print ("Program Runtime : %.4f" % endTime)




