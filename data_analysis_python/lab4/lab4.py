########################
# ЗАДАНИЕ 1
########################
import scipy.integrate as integrate
from math import sin

def integr(a):
    I1 = integrate.quad(lambda x: 4*sin(x + a) - 3, 0, 5)
    I2 = integrate.dblquad(
        lambda x,y: (x + a)**2 + (y + a)**2,
        0, 1,
        lambda x: 0, lambda x: 1
    )

    return int(I1[0] + I2[0])

########################
# ЗАДАНИЕ 2
########################
import numpy as np
from scipy.integrate import odeint

def ode_solve(a):
    def f(y, x):
        return (x + a) / 3
    
    y0 = 1.0
    k_step = 200

    x_output = np.linspace(0, 2, k_step)
    y_result = odeint(f, y0, x_output)
    result = y_result[-1][0]

    x_output = np.linspace(0, 2, k_step // 100)
    y_result_100 = odeint(f, 1, x_output)

    result_100 = y_result_100[-1][0]

    if abs(result - result_100) <= 0.01:
        return int(result)

print(ode_solve(1))


