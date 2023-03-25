import csv
import itertools
import math
import numpy as np
# import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sin, cos, sqrt
import pickle
import sys
import interplate
import re
import random
import membrane
import multiprocessing
import loss

args = sys.argv

Giga = 10**9
c = 2.99792*10**8 #(m/s)

pi = np.pi

class config:
    def __init__(self,
                 frequency:float,
                 array_distance:float,
                 sim_theta:int,
                 sim_phi:int,
                 temp_func,
                 phase_func,
                 power_func,
                 x_func,
                 y_func,
                 z_func,
                 regular:bool,
                 array_num:int):
        # ターゲット周波数
        self.frequency = frequency
        # 波長
        self.lamb = c/frequency
        # アンテナ素子間隔
        self.array_distance = array_distance
        # シミュレーション解像度
        self.sim_theta = sim_theta
        self.sim_phi = sim_phi
        # 温度に対する関数
        self.temp_func = temp_func
        self.phase_func = phase_func
        self.power_func = power_func
        # 変形に係る関数
        self.x_func = x_func
        self.y_func = y_func
        self.z_func = z_func
        # 正規化を行うかどうか
        self.regular = regular
        # 一辺のアンテナ素子数
        self.array_num = array_num

        # アンテナの情報を作成
        self.arrays = self.generate_arrays()



    def generate_arrays(self):
        """アンテナ

        Returns:
            _type_: _description_
        """
        arrays = []
        power_sum = 0

        for i, _x in enumerate(range(self.array_num)):
            # progress bar
            ratio = i/self.array_num
            length = 30
            progress = math.ceil(ratio * length)
            bar = f'generate array [{"■" * progress}{"□" * (length - progress)}]'
            percentage = math.ceil(ratio * 100)
            sys.stdout.write("\033[2K\033[G")
            sys.stdout.write(f'{bar} {percentage}%')
            sys.stdout.flush()
            # progress bar end

            for _y in range(self.array_num):
                power = interplate.temp2power(self.temp_func(_x,_y))/interplate.temp2power(0) * self.power_func(self,_x,_y)
                phase = interplate.temp2phase(self.temp_func(_x,_y)) + self.phase_func(_x,_y)
                power_sum = power_sum + power
                arrays.append(array(
                    x = self.x_func(_x,_y) * self.array_distance,
                    y = self.y_func(_x,_y) * self.array_distance,
                    z = self.z_func(_x,_y,self.array_distance) * self.array_distance,
                    phase = phase,
                    power = power,
                ))
        print()
        if self.regular == 1:
            power_ave = power_sum/len(arrays)
            for _array in arrays:
                _array.power = _array.power / power_ave

        return arrays

    # def generate_array_multi(self):
    #     with multiprocessing.Pool() as pool:
    #         args = [(sim_config, _x) for sim_config in [self]*self.array_num for _x in range(self.array_num)]
    #         _arrays = pool.map(generate_array_element, args)
    #     arrays = list(itertools.chain.from_iterable(_arrays))

    #     if self.regular == 1:
    #         power_sum = 0
    #         for _array in arrays:
    #             power_sum = power_sum + _array.power
    #         power_ave = power_sum / len(arrays)
    #         for _array in arrays:
    #             _array.power = _array.power / power_ave

    #     return arrays

class array:
    """アンテナ素子情報クラス
    アンテナ素子の情報をまとめたクラス
    """
    def __init__(self, x:float, y:float, z:float, phase:float, power:float):
        """アンテナ素子情報の初期化

        Args:
            x (float): 素子のx座標
            y (float): 素子のy座標
            z (float): 素子のz座標
            phase (float): 設定位相
            power (float): 設定利得
        """
        self.x = x
        self.y = y
        self.z = z
        # self.power_direction = lambda theta, phi: 1
        self.phase = phase
        self.power = power

    def distance(self, theta_flat:float, phi_flat:float):
        """仮想的な平面からアンテナ素子までの距離を算出

        Args:
            theta_flat (float): 仮想的な平面の法線ベクトル
            phi_flat (float): 仮想的な平面の法線ベクトル

        Returns:
            float: 距離
        """
        flat_x = np.sin(theta_flat) * np.cos(phi_flat)
        flat_y = np.sin(theta_flat) * np.sin(phi_flat)
        flat_z = np.cos(theta_flat)

        return flat_x*self.x + flat_y*self.y + flat_z*self.z

    def phase_distance(self, sim_config:config):
        """位相を距離に換算

        Args:
            sim_config (config): シミュレーション設定

        Returns:
            float: 距離
        """
        return sim_config.lamb*self.phase/(2*np.pi)

# def generate_array_element(args):
#     sim_config, _x = args
#     arrays = []

#     for _y in range(sim_config.array_num):
#         power = interplate.temp2power(sim_config.temp_func(_x,_y))/interplate.temp2power(0) * sim_config.power_func(_x,_y)
#         phase = interplate.temp2phase(sim_config.temp_func(_x,_y)) + sim_config.phase_func(_x,_y)
#         power_sum = power_sum + power
#         arrays.append(array(
#             sim_config.x_func(_x,_y) * sim_config.array_distance,
#             sim_config.y_func(_x,_y) * sim_config.array_distance,
#             sim_config.z_func(_x,_y,sim_config.array_distance) * sim_config.array_distance,
#             phase,
#             power,
#         ))

#     return arrays

def power(theta_m:float, phi_m:float, sim_config:config):
    """ 無限遠での振幅の和を計算する

    Args:
        theta_m (float): 計測を行う極角
        phi_m (float): 計測を行う方位角

    Returns:
        float: 出力
    """
    ep = 0
    em = 0
    for i, array in enumerate(sim_config.arrays):
        # progress bar
        ratio = i/len(sim_config.arrays)
        length = 30
        progress = math.ceil(ratio * length)
        bar = f'simulation [{"■" * progress}{"□" * (length - progress)}]'
        percentage = math.ceil(ratio * 100)
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.write(f'{bar} {percentage}%')
        sys.stdout.flush()
        # progress bar end

        distance = array.distance(theta_m, phi_m) - array.phase_distance(sim_config)
        ep = ep + array.power*np.exp(1j*2*np.pi*distance/sim_config.lamb)
        em = em + array.power*np.exp(-1j*2*np.pi*distance/sim_config.lamb)
    print()
    return (ep*em/len(sim_config.arrays)**2).real

def save(data,file_name:str):
    """あるデータをファイルとして保存

    Args:
        data (_type_): 保存するデータ
        file_name (str): 保存するファイル名
    """
    file = open(file_name, "wb")
    pickle.dump(data, file)

def antenna(sim_config:config):
    antenna = [[],[],[]]
    for x in range(sim_config.array_num):
        for y in range(sim_config.array_num):
            array_x = (x - 1/2*sim_config.array_num)/sim_config.array_num
            array_y = (y - 1/2*sim_config.array_num)/sim_config.array_num
            array_temp = sim_config.temp_func(x,y)

            antenna[0].append(array_x)
            antenna[1].append(array_y)
            antenna[2].append(array_temp)
    return antenna

def rand(x:float,y:float):
    """ランダムな値を生成

    Args:
        x (float): シード値 1
        y (float): シード値 2

    Returns:
        _type_: _description_
    """
    random.seed(x*10000 + y*10000)
    return random.random()

if __name__ == "__main__":
    with open('config.csv') as f:
        config_file = csv.reader(f)
        for row in config_file:
            _row = list(map(lambda row: row.strip(),row))
            if _row[0] == "sim_theta" or "#" in _row[0]:
                continue
            print(f"{_row[10]} : ")
            exec("def _temp(x,y): return " + _row[2])
            exec("def _phase(x,y): return " + _row[3])
            exec("def _power(self,x,y): return " + _row[4])
            exec("def _x(x,y): return " + _row[5])
            exec("def _y(x,y): return " + _row[6])
            exec("def _z(x,y,dis): return " + _row[7])
            sim_config = config(24*Giga,\
                                c/(24*Giga)/2,\
                                int(_row[0]),\
                                int(_row[1]),\
                                temp_func = _temp,
                                phase_func = _phase,
                                power_func = _power,
                                x_func = _x,
                                y_func = _y,
                                z_func = _z,
                                regular = int(_row[9]),
                                array_num = int(_row[8]),
                                )
            theta = np.linspace(-1/3*np.pi, 1/3*np.pi, sim_config.sim_theta)
            # theta = np.linspace(-1/11.25*np.pi, 1/11.25*np.pi, sim_config.sim_theta)
            phi = np.linspace(0, np.pi, sim_config.sim_phi, endpoint=False)

            Theta, Phi = np.meshgrid(theta, phi)
            Loss = 1/loss.loss(loss.distance(loss.gen_theta(loss.horizon_theta(), Theta, (30/180 * np.pi)/sim_config.array_num, 128 * 10**-3)), sim_config)
            # Power = power(Theta, Phi, sim_config) * Loss
            Power = power(Theta, Phi, sim_config)
            print(sim_config.lamb)

            # save((Loss, Theta, Phi), f"result/simulation/{_row[10]}_Loss")
            save((Power, Theta, Phi), f"result/simulation/{_row[10]}")
            save(antenna(sim_config), f"result/antenna/{_row[10]}")
