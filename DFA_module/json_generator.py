import json


class JsonGenerator:
    def __init__(self, picked_scenario):
        self.picked_scenario = picked_scenario
        self.data = []
        self.chart_type = ""
        self.measure = []
        self.dimension = []


    def generate_json(self):
        for key in self.picked_scenario.keys():
            scenario = self.picked_scenario[key]
            json_scenario = {}
            json_scenario["vtID"] = None
            json_scenario["type"] = scenario['Chart_Type']
            json_scenario["dimension"] = []
            dimension_01 = {}
            dimension_02 = {}
            if scenario["3column"] == True:
                dimension_01["groupId"] = "0"
                if len(scenario['X'].split(",")) == 1:
                    dimension_01["name"] = scenario['X']
                    dimension_01["grpFunc"] = None
                elif len(scenario['X'].split(",")) == 2:
                    dimension_01["name"] = scenario['X'].split(",")[0]
                    dimension_01["grpFunc"] = scenario['X'].split(",")[1]
                json_scenario["dimension"].append(dimension_01)

                dimension_02["groupId"] = "1"
                if len(scenario['X2'].split(",")) == 1:
                    dimension_02["name"] = scenario['X2']
                    dimension_02["grpFunc"] = None
                elif len(scenario['X2'].split(",")) == 2:
                    dimension_02["name"] = scenario['X2'].split(",")[0]
                    dimension_02["grpFunc"] = scenario['X2'].split(",")[1]
                json_scenario["dimension"].append(dimension_02)

            elif scenario["3column"] == False:
                dimension_01["groupId"] = "0"
                if len(scenario['X'].split(",")) == 1:
                    dimension_01["name"] = scenario['X']
                    dimension_01["grpFunc"] = None
                elif len(scenario['X'].split(",")) == 2:
                    dimension_01["name"] = scenario['X'].split(",")[0]
                    dimension_01["grpFunc"] = scenario['X'].split(",")[1]
                json_scenario["dimension"].append(dimension_01)

            json_scenario["measure"] = []
            measure_01 = {}
            measure_01["name"] = scenario['Y']
            measure_01["aggFunc"] = scenario['Agg_func_Y']
            json_scenario["measure"].append(measure_01)

            self.data.append(json_scenario)
        return json.dumps(self.data)


