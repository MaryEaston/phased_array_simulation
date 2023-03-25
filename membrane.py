import numpy as np
import matplotlib.pyplot as plt

data = "[ \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    [0.1, 0, 0.1, 0, 0, 0, 0.1, 0, 0.1], \
    ]"
std_len = 400 * (10**-3) #(一辺3.2m)

x = np.linspace(0, 8, 9)
y = np.linspace(0, 8, 9)
X, Y = np.meshgrid(x, y)

Z = np.array(eval(data))

def z(x, y, array_distance):
    _x = x*array_distance/std_len
    _y = y*array_distance/std_len
    _x_frac, _x_int = np.modf(_x)
    _y_frac, _y_int = np.modf(_y)
    p1 = Z[int(_y_int)][int(_x_int)]
    p2 = Z[int(_y_int) + 1][int(_x_int) + 1]
    if _y_frac == 0 or _x_frac/_y_frac > 1:
        p3 = Z[int(_y_int)][int(_x_int) + 1]
        dx = (p3-p1)*_x_frac
        dy = (p2-p3)*_y_frac
    else:
        p3 = Z[int(_y_int) + 1][int(_x_int)]
        dx = (p2-p3)*_x_frac
        dy = (p3-p1)*_y_frac
    return (p1 + dx + dy)/array_distance

if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')

    _X = X*std_len
    _Y = Y*std_len
    ax.plot_surface(_X, _Y, Z, alpha=0.7)

    dis = 0.006245666666666667

    x_list = []
    y_list = []
    z_list = []
    for x in range(512):
        print(x)
        for y in range(512):
            x_list.append(x*dis)
            y_list.append(y*dis)
            z_list.append(z(x,y,dis))
    # ax.scatter3D(x_list,y_list,z_list)

    ax.set_title('title')
    ax.set_aspect('equal')

    ax.set_xlabel('X-label')
    ax.set_ylabel('Y-label')
    ax.set_zlabel('Z-label')

    plt.show()
