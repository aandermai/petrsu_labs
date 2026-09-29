#####################
# ЗАДАНИЕ 1
#####################
import numpy as np

def function(int_list):
    n_list = np.array(int_list)

    n_list[n_list < 0] = 0
    n_list[n_list > 0] *= 4
    n_list.sort()
    n_list = n_list[::-1]

    return n_list[0] + n_list[1]

#####################
# ЗАДАНИЕ 2
#####################
def function(temperature1, temperature2):
    pass