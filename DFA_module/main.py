import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
from create_dictionary import CreateDictionary

if __name__ == "__main__":

    f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()
    csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"]

    createDic = CreateDictionary(csv_data, csv_contents_type)

    csv_data_table = createDic.initialize_dic()


    # csv_data = np.loadtxt("./TmaxDay_data.csv", delimiter=".", dtype=str)
    # print (csv_data)
