import csv
from create_dictionary import CreateDictionary
from column_combination import ColumnCombination
from transformation import Transformation
from rank import Rank
import time

if __name__ == "__main__":

    """
    Mock-up Ver.
    Dataset 1: TmaxDay_data
    Dataset 2: tmax_raw_data (from ERP)
    Dataset 3: Carcrash data
    """

    # read CSV file format (may change)
    # f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    f = open("./tmax_raw_data.csv", 'r', encoding='utf-8')
    # f = open("./carcrash.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    csv_data = []
    for line in rdr:
        csv_data.append(line)

    f.close()

    # get data_type (from meta in future)

    # csv_contents_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"] #tmaxday
    csv_contents_type = ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "tem", "tem", "num", "cat", "num", "num", "num", "cat"]  #tmax_raw_data_set
    # csv_contents_type = ["cat", "cat", "cat", "cat", "num", "num", "num", "num", "num", "num"] #carcrash

    # Time check
    startTime = time.time()

    # Create Column Data Dictionary
    data_dict = CreateDictionary(csv_data, csv_contents_type).initialize_dic()
    runtime = time.time()

    # Pop the csv object to reduce memory usage
    del csv_data
    print ("Runtime : %.4f" % (runtime-startTime))

    # Create Column Combination
    column_combination = ColumnCombination(data_dict).create_combination()

    print ("Column combination Created.")
    runtime2 = time.time()
    print("Runtime : %.4f" % (runtime2 - runtime))

    # Create Scenario Dictionary - Transformation + Guessing Scenario value
    scenario_dict = Transformation(data_dict, column_combination).transformation()

    print ("Scenario dictionary created")
    runtime3 = time.time()
    print("Runtime : %.4f" % (runtime3 - runtime2))

    # Calculate Scenario score and Rank. Top 20 will be printed
    Rank(scenario_dict).rank()

    # Final Time Check
    endTime = time.time() - startTime
    print ("Program Runtime : %.4f" % endTime)




