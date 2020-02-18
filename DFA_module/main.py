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
from rank import Rank
import time

if __name__ == "__main__":

    # f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    f = open("./tmax_raw_data.csv", 'r', encoding='utf-8')
    # f = open("./carcrash.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()
    # csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"] #tmaxday
    csv_contents_type = ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "tem", "tem", "num", "cat", "num", "num", "num", "cat"]  #tmax_raw_data_set
    # csv_contents_type = ["cat", "cat", "cat", "cat", "num", "num", "num", "num", "num", "num"] #carcrash

    startTime = time.time()
    #Create Column Data Dictionary
    data_dict = CreateDictionary(csv_data, csv_contents_type).initialize_dic()
    runtime = time.time()

    del csv_data
    print ("Runtime : %.4f" % (runtime-startTime))

    #Create Column Combination
    column_combination = ColumnCombination(data_dict).create_combination()

    print ("Column combination Created.")
    runtime2 = time.time()
    print("Runtime : %.4f" % (runtime2 - runtime))


    scenario_dict = Transformation(data_dict, column_combination).transformation()

    print ("Scenario dictionary created")
    runtime3 = time.time()
    print("Runtime : %.4f" % (runtime3 - runtime2))

    Rank(scenario_dict).rank()



    endTime = time.time() - startTime

    print ("Program Runtime : %.4f" % endTime)




