import json

def json_length(input_json):
    json_data = json.dumps(input_json)
    item_dict = json.loads(json_data)
    return len(item_dict)


