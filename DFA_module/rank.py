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
        self.score = []

    def rank(self):
        for key in self.scenario_dict:
            scenario_score = 0.5 * self.scenario_dict[key]['transform_score'] + self.scenario_dict[key]['m_score']
            self.score.append(scenario_score)

        top_10 = np.array(self.score).argsort()[-20:]
        top_10 = top_10[::-1]
        print("Top 100 Scenario")

        for item in top_10:
            picked_scenario_X = self.scenario_dict["%d" %item]['X']
            picked_scenario_Y = self.scenario_dict["%d" %item]['Y']
            picked_scenario_agg_X = self.scenario_dict["%d" %item]['Agg_func_X']
            picked_scenario_agg_Y = self.scenario_dict["%d" % item]['Agg_func_Y']
            picked_scenario_chart_type = self.scenario_dict["%d" % item]['Chart_Type']
            if self.scenario_dict["%d" % item]['3column'] == False:
                print ("Scenario %d : Dimension: %s %s , Measure: %s %s , \n Chart Type: %s , Scenario_score: %.4f \n"
                       %(item, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_Y, picked_scenario_Y, picked_scenario_chart_type, self.score[item]))

            else:
                picked_scenario_X2 = self.scenario_dict["%d" %item]['X2']
                picked_scenario_agg_X2 = self.scenario_dict["%d" %item]['Agg_func_X2']
                print ("Scenario %d : Dimension: %s %s %s %s , Measure: %s %s , \n Chart Type: %s , Scenario_score: %.4f \n"
                       %(item, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_X2, picked_scenario_X2, picked_scenario_agg_Y, picked_scenario_Y, picked_scenario_chart_type, self.score[item]))