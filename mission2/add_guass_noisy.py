import numpy as np
import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 读取txt文件
locations = np.loadtxt('handled_data.txt')

x = locations[:, 0]
y = locations[:, 1]

# 添加高斯噪声
def add_gauss_nosiy(datas):
    mu = 0
    sigma = 1
    data = datas.copy()
    for i in range(len(data)):
        data[i] += random.gauss(mu, sigma)
    return data

def drawPic(data):
    plt.figure(figsize=(13, 8))
    color = ['black','red']
    label = ["ground_truth", 'add_nosiy']
    linestyle = ['--', '-.']
    marker = ['', '.']
    linewidth = [2, 2]
    for j in range(len(data)):
        x = []
        y = []
        for p in data[j]:
            x.append(p[0])
            y.append(p[1])
        # plt.plot(x,y,label=label[j], marker=marker[j], linewidth=linewidth[j], color=color[j])
        plt.plot(x,y,label=label[j], marker=marker[j], color=color[j])
    
    plt.legend(prop={'size':15})
    plt.xlabel('x axis/m')
    plt.ylabel('y axis/m')
    # plt.axis('off')
    plt.show()

x_add_guass = []
x_add_guass = add_gauss_nosiy(x)
y_add_guass = add_gauss_nosiy(y)

gt_data = [x, y]
add_nosiy_data = [x_add_guass, y_add_guass]
plt.plot(x, y)
plt.plot(x_add_guass, y_add_guass, linestyle='', marker='.')
plt.xlabel('x axis/m')
plt.ylabel('y axis/m')
plt.show()
datas = [gt_data, add_nosiy_data]
# drawPic(datas)
fig = plt.figure()



