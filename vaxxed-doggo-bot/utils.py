import json

from . import config


def get_data():
    with open(config.data_file, "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    assert isinstance(data, dict), "data must be dict"
    with open(config.data_file, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)
