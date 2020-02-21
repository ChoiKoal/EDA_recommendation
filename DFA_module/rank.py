import numpy as np

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
        for key in self.scenario_dict:
            scenario_score = 0.1 * self.scenario_dict[key]['transform_score'] + self.scenario_dict[key]['m_score']
            self.score.append(scenario_score)

        top_10 = np.array(self.score).argsort()[-10:]
        top_10 = top_10[::-1]
        print("Top 100 Scenario")

        picked_scenario = {}
        i = 0
        for item in top_10:
            i += 1
            picked_scenario["%d" %i] = self.scenario_dict["%d" %item]
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
        return picked_scenario