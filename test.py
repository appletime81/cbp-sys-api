from pprint import pprint

a = [
    {"A": 1, "B": 2, "C": 3},
    {"A": 4, "B": 5, "C": 6},
    {"A": 7, "B": 8, "C": 9},
    {"A": 10, "B": 11, "C": 12},
    {"A": 13, "B": 14, "C": 15},
]


filter_values = list(filter(lambda x: x["A"] > 1 and x["A"] < 10, a))
pprint(filter_values)
