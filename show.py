from cmath import log10
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import sys
# import simulation
import os
import glob

args = sys.argv

# def load3d(filename):
#     points = [[],[],[]]
#     with open(filename, 'rb') as f:
#         load = pickle.load(f)
#         for data in load:

#             if data[0] <= 0:
#                 data[0] = 0.00000000001
#             dB = 1+1/4*log10(data[0]).real
#             if dB > 0:
#                 coord = simulation.polar(dB,data[1],data[2])
#             else:
#                 coord = simulation.polar(0, 0, 0)

#             points[0].append(coord.x)
#             points[1].append(coord.y)
#             points[2].append(coord.z)
#     return points

def load3d_antenna(filename):
    with open(f'result/antenna/{filename}', 'rb') as f:
        load = pickle.load(f)
    return load

def load2d(file_dir):
    points = [[],[],[]]
    with open(file_dir, 'rb') as f:
        load = pickle.load(f)

    return load

def show3d1(data,data_a):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(data[0], data[1], data[2])
    ax.scatter(data_a[0], data_a[1], -0.2,c = data_a[2] , cmap='rainbow')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.show()

def show3d2(data,data2):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(data[0], data[1], data[2])
    ax.scatter(data2[0], data2[1], data2[2],c="r")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.show()

def getNearestValue(list, num):
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx

def save2_x(data, out_dir, *filenames):
    colors = ['k', 'r', 'y', 'g', 'b']
    fig_name = ""
    fig, ax = plt.subplots()
    for index, filename, color in zip(range(5),filenames, colors):
        x = []
        y = []
        for _power, _theta, _phi in zip(data[0], data[1], data[2]):
            for power, theta, phi in zip(_power, _theta, _phi):
                if phi == 0:
                    x.append(theta)
                    y.append(power)
        # for d in data:
        #     if d[2] == 0:
        #         x.append(d[1])
        #         y.append(d[0])
        _x = list(map(lambda x: x/np.pi*180,x))
        _y = list(map(lambda y: np.real(10*log10(y)),y))

        fig_name = fig_name + filename
        ax.plot(_x, _y, color=color)

        max = np.argmax(_y)
        dB1 = getNearestValue(_y, -1)
        dB2 = getNearestValue(_y, -2)
        dB3 = getNearestValue(_y, -3)
        # ax.text(0.05, 0.95 - index/20,
        #         f"{round(_x[max],3)}° ({round(_y[max].real,3)} dB)\n\
        #         {round(_x[dB1],5)}° ({round(_y[dB1].real,3)} dB)\n\
        #         {round(_x[dB2],5)}° ({round(_y[dB2].real,3)} dB)\n\
        #         {round(_x[dB3],5)}° ({round(_y[dB3].real,3)} dB)",
        #         color=color,
        #         verticalalignment='top',
        #         transform=ax.transAxes
        #         )
        print(f"{filename},{round(_y[1].real,3)},")

    ax.set_xticks([-60,-30,0,30,60])
    plt.xlim([-60,60])
    ax.set_xlabel("$θ_y$ [deg]", fontsize=35)

    # ax.set_yticks([-20,-10,0,10,20,30,40])
    # plt.ylim([-20,40])
    # ax.set_ylabel("$G_r$ [dBi]", fontsize=35)
    ax.set_yticks([-50,-40,-30,-20,-10,0])
    plt.ylim([-50,-0])
    ax.set_ylabel("$G_r$ [dB]", fontsize=35)

    ax.grid()
    # ax.set_yticks([-5,-4,-3,-2,-1,0,1])
    # plt.ylim([-5,1])
    ax.tick_params(labelsize=28)

    plt.tight_layout()
    plt.savefig(f'{out_dir}{os.path.basename(fig_name)}.png')
    plt.close()

def save2_y(data, out_dir, *filenames):
    colors = ['k', 'r', 'y', 'g', 'b']
    fig_name = ""
    fig, ax = plt.subplots()
    for index, filename, color in zip(range(5),filenames, colors):
        x = []
        y = []
        for _power, _theta, _phi in zip(data[0], data[1], data[2]):
            for power, theta, phi in zip(_power, _theta, _phi):
                if phi == np.pi/2:
                    x.append(theta)
                    y.append(power)
        # for d in data:
        #     if d[2] == np.pi/2:
        #         x.append(d[1])
        #         y.append(d[0])
        _x = list(map(lambda x: x/np.pi*180,x))
        _y = list(map(lambda y: 10*log10(y.real) if y != 0 else -100000000 ,y))

        fig_name = fig_name + filename
        ax.plot(_x, _y, color=color)

        max_index = np.argmax(_y)
        ax.text(0.05, 0.95 - index/20, f"{_x[max_index]}° ({_y[max_index].real} dB)",
                color=color,
                verticalalignment='top',
                transform=ax.transAxes
                )

    # ax.set_xticks([-90,-60,-30,0,30,60,90])
    ax.set_yticks([-40,-30,-20,-10,0,10])
    plt.ylim([-40,10])
    plt.savefig(f'{out_dir}{os.path.basename(fig_name)}')
    plt.close()


if len(sys.argv) == 1:
    files = glob.glob("result/simulation/*")
    # files = glob.glob("archive/simulation/*")
    for file in files:
        save2_x(load2d(f"result/simulation/{os.path.basename(file)}"), "result/graph/x/", file)
        # save2_y(load2d(f"result/simulation/{os.path.basename(file)}"), "result/graph/y/", file)

        # save2_x(load2d(f"archive/simulation/{os.path.basename(file)}"), "archive/graph/x/", file)
        # save2_y(load2d(f"archive/simulation/{os.path.basename(file)}"), "archive/graph/y/", file)

if len(sys.argv) > 1:
    datas = sys.argv
    datas.pop(0)
    save2_x(*datas)

# if len(sys.argv) == 2:
#     # show3d1(load3d(args[1]),load3d_antenna(args[1]))
#     save2_x(load2d(args[1]),args[1])
#     save2_y(load2d(args[1]),args[1])

# if len(sys.argv) == 3:
#     show3d2(load3d(args[1]),load3d(args[2]))

# fig, ax = plt.subplots()

# data = load2d('result/simulation/t:(40)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y)

################################################################

# data = load2d('result/simulation/t:x(-40,0)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y, color='b')

################################################################

# data = load2d('result/simulation/t:x(0,40)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y, color='g')

################################################################

# data = load2d('result/simulation/t:x(40,80)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y,color='y')

################################################################

# data = load2d('result/simulation/t:x(40,80)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y,color='r')

# ax.set_xticks([-90,-60,-30,0,30,60,90])
# plt.yscale('log')
# plt.ylim([0.0001,10])
# pig_path = f'r'
# plt.savefig(f'result/graph/x/{os.path.basename("(40)(40,80)")}')
# plt.close()

# fig, ax = plt.subplots()

# data = load2d('result/simulation/t:(40)')

# x = []
# y = []
# for d in data:
#     if d[2] == 0:
#         x.append(d[1])
#         y.append(d[0])
# _x = list(map(lambda x: x/np.pi*180,x))

# ax.plot(_x, y)

# if len(sys.argv) == 3:
