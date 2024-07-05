import json

with open("./data/R41BN247000T0K-WorkBench.json") as json_file:
    data = json.load(json_file)

mydict = {'Part': data['uniquePn']}
for dt in data['parameterValues']:
    mydict[dt['parameterName']] =  dt['value']

for k,v in mydict.items():
    print(k, ' ', v)
with open('./data/R41B247.json', 'w') as outfile:
    json.dump(mydict, outfile)