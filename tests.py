import json

a=[1,2,3]
b=[4,5,6]
with open('result.txt', 'a') as file:
    json.dump(a, file)


with open('result.txt', 'a') as file:
    json.dump(b, file)