from datetime import datetime


a = [
    {"A": 1, "B": 2},
    {"A": 3, "B": 4},
    {"A": 5, "B": 6},
]


res = list(map(lambda x: x["B"] % 2 == 0, a))

print(res)
