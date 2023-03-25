import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from math import log10

t_latent = np.linspace(-40, 120, 161)

def temp2phase(temp):
    phase = [-5.29E+01,-6.99E+01,-7.20E+01,-1.04E+02,-1.33E+02]
    temp_list = [-40,0,40,80,120]

    fitted_curve = interpolate.interp1d(temp_list, phase, kind="quadratic")

    return np.pi * fitted_curve(temp)/180

def temp2power(temp):
    power = [1.14E+01,1.64E+01,1.85E+01,1.85E+01,1.70E+01]
    temp_list = [-40,0,40,80,120]

    fitted_curve = interpolate.interp1d(temp_list, power, kind="quadratic")

    return 10**(fitted_curve(temp)/10)

phase = [-5.29E+01,-6.99E+01,-7.20E+01,-1.04E+02,-1.33E+02]
temp_list = [-40,0,40,80,120]

fitted_curve = interpolate.interp1d(temp_list, phase, kind="quadratic")

plt.scatter(temp_list, phase)
plt.plot(t_latent, fitted_curve(t_latent), c="red")

plt.savefig("phase.png")

plt.clf()

power = [1.14E+01,1.64E+01,1.85E+01,1.85E+01,1.70E+01]
temp_list = [-40,0,40,80,120]

fitted_curve = interpolate.interp1d(temp_list, power, kind="quadratic")

plt.scatter(temp_list, power)
plt.plot(t_latent, fitted_curve(t_latent), c="red")

plt.savefig("power.png")
