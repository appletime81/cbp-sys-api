a = {
    "endCreateDate": "3",
    "endDueDate": "4",
    "startCreateDate": "1",
    "startDueDate": "2",
}


newDict = {}

for key, value in a.items():
    if key.startswith("start"):
        newKey = key.replace("start", "range")
        if newKey not in newDict:
            newDict[newKey] = {}
        newDict[newKey]["gte"] = value
    elif key.startswith("end"):
        newKey = key.replace("end", "range")
        if newKey not in newDict:
            newDict[newKey] = {}
        newDict[newKey]["lte"] = value
    else:
        newDict[key] = value

print(newDict)
