# For when I need to convert things, this might help
# https://pint.readthedocs.io/en/stable/getting/tutorial.html

us_units = {
    "weight": {
        "lb": {"name": "pound"},
        "oz": {"name": "ounce"},
    },
    "volume": {
        "gal": {"name": "gallon"},
        "qt": {"name": "quart"},
        "pt": {"name": "pint"},
        "c": {"name": "cup"},
        "floz": {"name": "fluid ounce"},
        "tbsp": {"name": "tablespoon"},
        "tsp": {"name": "teaspoon"},
    }
}

metric_units = {
    "weight": {
        "g": {"name": "gram"},
        "kg": {"name": "kilogram"},
    },
    "volume": {},
}

count_units = {
    "ct": {"name": "count"},
    "dz": {"name": "dozen"},
}

count_list = [(k, v["name"]) for k, v in count_units.items()]

us_weight_list = [(k, v["name"]) for k, v in us_units["weight"].items()]
us_volume_list = [(k, v["name"]) for k, v in us_units["volume"].items()]
us_choice_list = us_weight_list + us_volume_list + count_list

metric_weight_list = [(k, v["name"]) for k, v in metric_units["weight"].items()]
metric_volume_list = [(k, v["name"]) for k, v in metric_units["volume"].items()]
metric_choice_list = metric_weight_list + metric_volume_list + count_list
