import numpy as np
import math

class Rank():
    def __init__(self, scenario_dict):
        """
        :param scenario_dict: created scenario dictionary
        """
        self.scenario_dict = scenario_dict
        self.score = []

    def rank(self):
        """
        calculate scenario ranking and pick top N scenario
        :return: picked scenario
        """
        index = list(self.scenario_dict.keys())
        for key in self.scenario_dict:
            scenario_score = 0.01 * self.scenario_dict[key]['transform_score'] + self.scenario_dict[key]['m_score']
            self.score.append(scenario_score)

        top_10 = np.array(self.score).argsort()[-10:]
        top_10 = top_10[::-1]
        print("Top 100 Scenario")

        picked_scenario = {}
        i = 0
        for item in top_10:
            i += 1
            item_index = index[item]
            picked_scenario["%d" %i] = self.scenario_dict[item_index]
            picked_scenario_X = self.scenario_dict[item_index]['X']
            picked_scenario_Y = self.scenario_dict[item_index]['Y']
            picked_scenario_agg_X = self.scenario_dict[item_index]['Agg_func_X']
            picked_scenario_agg_Y = self.scenario_dict[item_index]['Agg_func_Y']
            picked_scenario_chart_type = self.scenario_dict[item_index]['Chart_Type']
            if self.scenario_dict[item_index]['3column'] == False:
                print ("Scenario %s : Dimension: %s %s , Measure: %s %s , \n Chart Type: %s , Scenario_score: %.4f \n"
                       %(item_index, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_Y, picked_scenario_Y, picked_scenario_chart_type, self.score[item]))

            else:
                picked_scenario_X2 = self.scenario_dict[item_index]['X2']
                picked_scenario_agg_X2 = self.scenario_dict[item_index]['Agg_func_X2']
                print ("Scenario %s : Dimension: %s %s %s %s , Measure: %s %s , \n Chart Type: %s , Scenario_score: %.4f \n"
                       %(item_index, picked_scenario_agg_X, picked_scenario_X, picked_scenario_agg_X2, picked_scenario_X2, picked_scenario_agg_Y, picked_scenario_Y, picked_scenario_chart_type, self.score[item]))
        return picked_scenario