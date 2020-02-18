import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
import pandas as pd
from collections import Counter, defaultdict

class Rank():
    def __init__(self, scenario_dict):
        self.scenario_dict = scenario_dict
        self.score1 = []
        self.score2 = []

    def rank(self):
        for key in self.scenario_dict:
            scenario_score1 = (0.5 * self.scenario_dict[key]['transform_score'] + self.scenario_dict[key]['m_score'])
            scenario_score2 = (0.5 * self.scenario_dict[key]['transform_score'] + self.scenario_dict[key]['m_score']) * (self.scenario_dict[key]['scd_score'] + 0.5)
            self.score1.append(scenario_score1)
            self.score2.append(scenario_score2)

        top_10_1 = np.array(self.score1).argsort()[-10:]
        top_10_2 = np.array(self.score2).argsort()[-10:]
        print("Top 10 Scenario1")

        for item in top_10_1:
            picked_scenario_X = self.scenario_dict["%d" %item]['X']
            picked_scenario_Y = self.scenario_dict["%d" %item]['Y']
            picked_scenario_agg_X = self.scenario_dict["%d" %item]['Agg_func_X']
            picked_scenario_agg_Y = self.scenario_dict["%d" % item]['Agg_func_Y']
            picked_scenario_chart_type = self.scenario_dict["%d" % item]['Chart_Type']

            print ("Scenario %d : Dimension: %s %s , Measure: %s %s , Chart Type: %s , Scenario_score: %.4f" %(item, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_Y, picked_scenario_Y, picked_scenario_chart_type, self.score1[item]))

        print("Top 10 Scenario2")
        for item in top_10_2:
            picked_scenario_X = self.scenario_dict["%d" % item]['X']
            picked_scenario_Y = self.scenario_dict["%d" % item]['Y']
            picked_scenario_agg_X = self.scenario_dict["%d" % item]['Agg_func_X']
            picked_scenario_agg_Y = self.scenario_dict["%d" % item]['Agg_func_Y']
            picked_scenario_chart_type = self.scenario_dict["%d" % item]['Chart_Type']

            if item in top_10_1:
                print ("[", end=' ')

                print("Scenario %d : Dimension: %s %s , Measure: %s %s , Chart Type: %s , Scenario_score: %.4f" % (
                item, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_Y, picked_scenario_Y,
                picked_scenario_chart_type, self.score2[item]),  end =' ')
            else:
                print("Scenario %d : Dimension: %s %s , Measure: %s %s , Chart Type: %s , Scenario_score: %.4f" % (
                    item, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_Y, picked_scenario_Y,
                    picked_scenario_chart_type, self.score2[item]))

            if item in top_10_1:
                print ("]")