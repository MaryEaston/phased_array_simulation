import matplotlib.pyplot as plt
import numpy as np
# import simulation
from cmath import log10

height = 500 * 10**3 #(m)
earth_r = 6378.14 * 10**3 #(m)
orbit_r = earth_r + height
gme = 3.986 * 10**14 #(m^3 s^-2) 地心重力定数

step_time = 10**-3

lamb = 12.491 * 10**-3

def loss(d,sim_config):
    return (4*np.pi*d/sim_config.lamb)**2

def loss_t(d):
    return (4*np.pi*d/lamb)**2

def distance(theta):
    return np.sqrt(earth_r**2 - 2*orbit_r*earth_r*np.sin(theta) + orbit_r**2)

def gen_theta_main(start_theta, index, step_time):
    # 角速度
    omega = (gme / orbit_r**3)**(1/2)
    return omega*index*step_time + start_theta

def gen_theta(start_theta, Theta, step_arg,step_time):
    omega = (gme / orbit_r**3)**(1/2)
    Index = (Theta - np.min(Theta)) / step_arg
    return Index * step_time * omega + start_theta

def horizon_theta():
    return np.arcsin(earth_r/orbit_r)

def top_theta():
    return np.pi/2

# print(np.arange(10)*1.2*0.8 + 1.2)
if __name__ == "__main__":
    _x = []
    _y = []
    max = (0,0)
    lo_old = 10*-30
    lo = 10*-30
    for x in range(346632*2):
        _x.append(x)
        lo = 1/loss_t(distance(gen_theta_main(horizon_theta(), x, 10**-3)))
        d = np.real(10*log10(lo) - 10*log10(lo_old))
        if d > max[0] and x != 0:
            max = (d, x)
        _y.append(lo)
        lo_old = lo
        # _y.append(distance(gen_theta_main(horizon_theta(), x, 10**-3)))

    fig, ax = plt.subplots()
    __x = list(map(lambda x: x/1000,_x))
    __y = list(map(lambda y: np.real(10*log10(y)),_y))

    print(max[0], max[1])
    # __y = _y


    # max = np.argmax(__y)
    ax.text(0.05, 0.95,
                f"max {round(max[0],7) * 1000}dB/s ({max[1] / 1000})",
                verticalalignment='top',
                transform=ax.transAxes
                )

    ax.plot(__x, __y)
    ax.set_xticks([0, 347, 693], ["0(Horizon)", "347(Zenith)", "693(Horizon)"])

    ax.set_xlabel("time(position) [s]")
    ax.set_ylabel("Free Space Pass Loss [dB]")

    plt.savefig("loss.eps")
