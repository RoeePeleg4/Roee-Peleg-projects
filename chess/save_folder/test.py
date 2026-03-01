dict1 = {}
dict1.update({"a" : [3]})
if ("a" in list(dict1.keys())):
    dict1["a"].append(6)
else:
    dict1.update({"a" : 6})
dict1.update({"a" : 6})
print(dict1)