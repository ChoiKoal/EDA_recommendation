import pandas as pd

dict1 = {}
dict2 = {}

dict1['2019 01'] = 1
dict1['2019 02'] = 2

dict2['2019 02'] = 3
dict2['2019 03'] = 4

print(dict1)
print(dict2)

dict1.update(dict2)

print(dict1)

key_list = []
for key in dict1.keys():
    key_list.append((int(key.split(" ")[0]), int(key.split(" ")[1])))

print(key_list)

# key_y, key_m = min(dict1.keys().split(' ')

a = (2015, 3)
b = (2015, 0)

if a > b:
    print("a > b")
else:
    print("a < b")