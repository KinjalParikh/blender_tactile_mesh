import numpy as np
import matplotlib.pyplot as plt
import json

'''
data format = 70 trials
{"trial": [1, 4], "response": 0}
{"trial": [4, 7], "response": 1}
{"trial": [2, 4], "response": 0}
{"trial": [4, 4], "response": 1}
{"trial": [4, 4], "response": 0}
{"trial": [6, 4], "response": 1}
'''

filename = 'results/' + 'responses_20240322144334' + '.csv'

data_array = [[] for i in range(7)]

with open(filename, 'r') as file:
    for line in file:
        data = json.loads(line)
        if data['trial'][0] == 4:
            data_array[data['trial'][1]-1].append(data['response'])
        else:
            data_array[data['trial'][0]-1].append(1-data['response'])

data_array = [np.mean(data) for data in data_array]

plt.plot(data_array)
plt.show()