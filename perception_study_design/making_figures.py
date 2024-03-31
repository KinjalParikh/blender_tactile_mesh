import numpy as np
import matplotlib.pyplot as plt
import json
from bayesian_adaptive import bayesian_adaptive_controller


'''
data format = 70 trials
{"trial": [1, 4], "response": 0}
{"trial": [4, 7], "response": 1}
{"trial": [2, 4], "response": 0}
{"trial": [4, 4], "response": 1}
{"trial": [4, 4], "response": 0}
{"trial": [6, 4], "response": 1}
'''

result_files_dots = [
    'responses_20240325152547_Brenna',
    'responses_20240325155339_Sue',
    'responses_20240325172148_Bogdan',
    'responses_20240325181052_Karran',
    'responses_20240325192824_Chenxi'
]

result_files_lines = [
    'responses_20240325154545_Yixin',
    'responses_20240325161309_Qihan',
    'responses_20240325215106_Warren',
    'responses_20240328095845_Blaine',
    'responses_20240328104853_Zhecheng',
    'responses_20240329122126_Victor',
    'responses_20240329180546_Selena'
]

thresholds = []
slopes = []
lapse_rates = []
sigmas = []
data_array_means = []
stimuli_array = [-3, -2, -1, 0, 1, 2, 3]

for result_file in result_files_lines:
    filename = 'results/' + result_file + '.csv'
    print('loading ' + filename)

    data_array = [[] for _ in range(7)]

    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            if data['trial'][0] == 4:
                data_array[data['trial'][1]-1].append(data['response'])
            else:
                data_array[data['trial'][0]-1].append(1-data['response'])

    data_array_mean = [np.mean(data) for data in data_array]
    data_array_means.append(data_array_mean)

    test_controller = bayesian_adaptive_controller(stimuli_array)
    for i in range(7):
        for j in range(len(data_array[i])):
            design = {'stimulus': stimuli_array[i]} 
            response = data_array[i][j]
            test_controller.update_params(design, response)

    test_controller.print_posterior_estimation()
    thresholds.append(test_controller.engine.post_mean['threshold'])
    slopes.append(test_controller.engine.post_mean['slope'])
    lapse_rates.append(test_controller.engine.post_mean['lapse_rate'])
    sigmas.append(1 / test_controller.engine.post_mean['slope'])

# save all the data arrays to a local json file
data = {
    'thresholds': thresholds,
    'slopes': slopes,
    'lapse_rates': lapse_rates,
    'sigmas': sigmas,
    'data_array_means': data_array_means
}
with open('results/results_stats_lines.json', 'w') as file:
    json.dump(data, file)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.figure(figsize=(8, 6))

# get tab10 colormap for plotting
cmap = plt.get_cmap('tab10')
colors = cmap.colors[:len(thresholds)]
labels = ['P'+str(i+1) for i in range(len(thresholds))]

for i in range(len(thresholds)):
    threshold = thresholds[i]
    slope = slopes[i]
    lapse_rate = lapse_rates[i]
    sigma = sigmas[i]

    x = np.linspace(-3, 3, 1000)
    cdf = norm.cdf(x, loc=threshold, scale=sigma)
    adjusted_cdf = (1 - 2*lapse_rate) * cdf + lapse_rate

    plt.plot(stimuli_array, data_array_means[i], 'o', color=colors[i], label=labels[i])
    plt.plot(x, adjusted_cdf, color=colors[i])

plt.title('User Responses and Approximated Psychometric Functions (Lines)')
plt.xlabel('Compare Density Levels')
plt.ylabel('Percentage of "more dense" responses')
plt.legend()
plt.grid(True)
plt.show()
