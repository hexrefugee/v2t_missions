# 计算车道线坐标

# 1.获取车道宽：1.75m
# 2.获取车道线宽：0.15m
# 3.根据车方向向量和车道宽算出车道线坐标


import numpy as np
import random
from math import sqrt

location = np.loadtxt('handled_data.txt')
s = 1.75

def calculate(x1, y1, x2, y2):
    return (x2 - x1)/(y2 - y1)

def get_point(k, s, x1, y1):
    u1 = s / sqrt(1 + k * k) + x1
    u2 = -(s / sqrt(1 + k * k)) + x1
    v1 = k * (u1 - x1) + y1
    v2 = k * (u2 - x1) + y1
    return u1, v1, u2, v2

def main():
    x_datas = location[:, 0]
    y_datas = location[:, 1]

    x_right = []
    y_right = []
    x_left = []
    y_left = []

    for i in range(len(x_datas)):
        if i == 0:
            x1 = x_datas[0]
            y1 = y_datas[0]
            x2 = x_datas[1]
            y2 = y_datas[1]
        else:
            x1 = x2.copy()
            y1 = y2.copy()
            if i + 1 == len(x_datas):
                break
            x2 = x_datas[i + 1]
            y2 = y_datas[i + 1]
        k = -1 * calculate(x1, y1, x2, y2)
        u1, v1, u2, v2 = get_point(k, s, x1, y1)
        x_right.append(u1)
        y_right.append(v1)
        x_left.append(u2)
        y_left.append(v2)
    
    right_x_point = np.array(x_right)
    right_y_point = np.array(y_right)
    right_x_point = np.reshape(right_x_point, (len(right_x_point), 1))
    right_y_point = np.reshape(right_y_point, (len(right_y_point), 1))
    result_right = np.append(right_x_point, right_y_point, axis=1)
    
    left_x_point = np.array(x_left)
    left_y_point = np.array(y_left)
    left_x_point = np.reshape(left_x_point, (len(left_x_point), 1))
    left_y_point = np.reshape(left_y_point, (len(left_y_point), 1))
    result_left = np.append(left_x_point, left_y_point, axis=1)

    np.savetxt('left_landmark.txt', result_right, fmt='%s', delimiter=' ')
    np.savetxt('right_landmark.txt', result_left, fmt='%s', delimiter=' ')


main()

