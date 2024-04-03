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

filename = 'results/' + 'responses_20240401165655' + '.csv'

data_array = [[] for i in range(7)]

with open(filename, 'r') as file:
    for line in file:
        data = json.loads(line)
        if data['trial'][0] == 4:
            data_array[data['trial'][1]-1].append(data['response'])
        else:
            data_array[data['trial'][0]-1].append(1-data['response'])

data_array_mean = [np.mean(data) for data in data_array]
data_array_mean[3] = 0.5

stimuli_array = [-3, -2, -1, 0, 1, 2, 3]
test_controller = bayesian_adaptive_controller(stimuli_array)

for i in range(7):
    for j in range(len(data_array[i])):
        design = {'stimulus': stimuli_array[i]} 
        response = data_array[i][j]
        test_controller.update_params(design, response)

test_controller.print_posterior_estimation()


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Given parameters
threshold = test_controller.engine.post_mean['threshold']
slope = test_controller.engine.post_mean['slope']
lapse_rate = test_controller.engine.post_mean['lapse_rate']

# Convert the slope to standard deviation (σ). This conversion depends on the specific relation you're using;
# here we'll assume a direct relationship for illustration.
sigma = 1 / slope

# Define the range of x values for which we want to compute the CDF
x = np.linspace(-4, 4, 1000)

# Compute the Gaussian CDF
cdf = norm.cdf(x, loc=threshold, scale=sigma)

# Adjust the CDF for the lapse rate
adjusted_cdf = (1 - 2*lapse_rate) * cdf + lapse_rate

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(stimuli_array, data_array_mean, 'o', label='Data')
plt.plot(x, adjusted_cdf, label='Gaussian CDF')
plt.title('Gaussian CDF with Lapse Rate')
plt.xlabel('Compare Density Levels')
plt.ylabel('Percentage of "more dense" responses')
plt.legend()
plt.grid(True)
plt.show()
