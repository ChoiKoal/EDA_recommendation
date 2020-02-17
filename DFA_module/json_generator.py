import json


class JsonGenerator:
    def __init__(self, table_id):
        self.table_id = table_id
        self.chart_type = ""
        self.measure = []
        self.dimension = []

    def add_dimension(self, name, group_func):
        # name : column name
        # group_func : group function - None, "년", "월", "일"
        info = dict()
        info['groupId'] = len(self.dimension)
        info['name'] = name
        # info['type'] = type

        # grpFunc - 년 월 일 (임시)
        info['grpFunc'] = group_func
        # info['grpLogc'] = group_logc
        self.dimension.append(info)

    def add_measure(self, name, aggr_func):
        # name : column name
        # aggr_func : aggregation function - "COUNT", "SUM", "MAX", "MIN", "AVG"
        info = dict()
        info['name'] = name
        # info['type'] = type
        info['aggFunc'] = aggr_func
        self.measure.append(info)

    def set_chart_type(self, chart_type):
        # bar1, line1, pie1, scatter1
        self.chart_type = chart_type

    def generate_json(self):
        data = dict()
        data['tableId'] = self.table_id
        data['type'] = self.chart_type
        data['dimension'] = self.dimension
        data['measure'] = self.measure
        return json.dumps(data)


