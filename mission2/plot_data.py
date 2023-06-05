import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def main():
    file_name = 'handled_data.txt'
    datas = np.loadtxt(file_name, dtype='double', delimiter=' ')
    # x_data = np.loadtxt(file_name, dtype='double', delimiter=' ', usecols=(0))
    # y_data = np.loadtxt(file_name, dtype='double', delimiter=' ', usecols=(1))
    # z_data = np.loadtxt(file_name, dtype='double', delimiter=' ', usecols=(2))
    x_data = datas[:, 0]
    y_data = datas[:, 1]
    z_data = datas[:, 2]

    fig = plt.figure()
    ax3d = Axes3D(fig)
    # ax3d.scatter(x_data, y_data, z_data, c="b",marker="*")
    ax3d.scatter(x_data, y_data, c="b", marker="*")
    plt.show()

main()
