import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
from create_dictionary import CreateDictionary
from column_combination import ColumnCombination

if __name__ == "__main__":

    f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()
    csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"]

    data_dict = CreateDictionary(csv_data, csv_contents_type).initialize_dic()
    column_combination = ColumnCombination(data_dict).create_combination()




    # csv_data = np.loadtxt("./TmaxDay_data.csv", delimiter=".", dtype=str)
    # print (csv_data)
