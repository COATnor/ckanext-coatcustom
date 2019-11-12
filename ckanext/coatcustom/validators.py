import json

def str_to_bool(value):
    return str(value).lower() == "true"

def multiple_to_json(iterable):
    if not iterable:  # Missing object
        iterable = []
    return json.dumps(iterable)
