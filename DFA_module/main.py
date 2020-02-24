import csv
from create_dictionary import CreateDictionary
from column_combination import ColumnCombination
from transformation import Transformation
from rank import Rank
from json_generator import JsonGenerator
import time

if __name__ == "__main__":

    """
    Mock-up Ver.
    Dataset 1: TmaxDay_data
    Dataset 2: tmax_raw_data (from ERP)
    Dataset 3: Carcrash data
    """

    # read CSV file format (may change)
    f = open("./jeju_wood.csv", 'r', encoding='utf-8')
    # f = open("./TmaxDay_data.csv", 'r', encoding='utf-8')
    # f = open("./tmax_raw_data.csv", 'r', encoding='utf-8')
    # f = open("./carcrash.csv", 'r', encoding='utf-8')
    rdr = csv.reader(f)
    data_table = []
    for line in rdr:
        data_table.append(line)

    f.close()

    # get data_type (from meta in future)

    data_type = ["cat", "cat", "cat", "cat", "tem", "cat", "cat", "cat", "num", "num", "num", "num", "cat", "cat", "cat", "num", "num"]
    # data_type = ["tem", "cat", "cat", "num", "cat", "num", "num", "num", "num"] #tmaxday
    # data_type = ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "tem", "tem", "num", "cat", "num", "num", "num", "cat"]  #tmax_raw_data_set
    # data_type = ["cat", "cat", "cat", "cat", "num", "num", "num", "num", "num", "num"] #carcrash


    # data_table = []
    # data_type = []
    # data_name = []
    #
    # for i in range(len(input_data['meta'])):
    #     data_name.append(input_data['meta'][i]['name'])
    #     data_type.append(input_data['meta'][i]['type'])
    # data_table.append(data_name)
    # for i in range(len(input_data['data'])):
    #     data_table.append(input_data['data'][i])

    # Time check
    startTime = time.time()
    # Create Column Data Dictionary
    data_dict = CreateDictionary(data_table, data_type).initialize_dic()
    runtime = time.time()

    # Pop the csv object to reduce memory usage
    del data_table
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
    picked_scenario = Rank(scenario_dict).rank()

    # Final Time Check
    endTime = time.time() - startTime

    json = JsonGenerator(picked_scenario).generate_json()
    print ("Program Runtime : %.4f" % endTime)

    print (json)




