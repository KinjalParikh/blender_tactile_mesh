from cgi import test
from turtle import update
from adopy.tasks.psi import ModelProbit, EnginePsi
import numpy as np
from scipy.stats import bernoulli
import math
import matplotlib.pyplot as plt

'''
a bayesian adaptive processing class that generate next stimulus and update posterious prediction values

how to use:
test_controller = bayesian_adaptive_controller()
design = test_controller.get_next_design()
response = test_controller.compute_simulation(design)
test_controller.update_params(design, response)
'''

class bayesian_adaptive_controller:
    
    def __init__(self, stimuli_array):
        self.model = ModelProbit()
        self.grid_designs = {
            'stimulus': stimuli_array
        }
        self.grid_params = {
            # 'guess_rate': np.linspace(0.01, 0.05, num=5),
            # 'guess_rate': [0],
            'lapse_rate': np.linspace(0, 0.05, num=11),
            'threshold': np.linspace(-2, 2, num=101),
            'slope': np.linspace(0, 2, num=101)
        }
        self.engine = EnginePsi(self.model, self.grid_designs, self.grid_params)
        self.trial_number = 0
        #done
    
    def get_next_design(self, optimal=True):
        if optimal:
            return self.engine.get_design('optimal')
        else:
            return self.engine.get_design('random')
    
    def update_params(self, design, response):
        self.engine.update(design, response)
        self.trial_number += 1

    def print_posterior_estimation(self):
        print('Trial', self.trial_number)
        # arg = np.argmax(self.engine.post)
        # print(arg)
        # print(self.engine.grid_param.iloc[arg])
        print(self.engine.post_mean)
        print(self.engine.post_sd)

if __name__ == "__main__":
    stimuli_array = [-3, -2, -1, 0, 1, 2, 3]
    test_controller = bayesian_adaptive_controller(stimuli_array)
    design = test_controller.get_next_design()
    print(type(design))
    print(design)
    response = 1
    print(design['stimulus'], response)
    test_controller.update_params(design, response)
    print(test_controller.engine.post_mean)
    print(test_controller.engine.post_sd)