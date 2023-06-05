import numpy as np
import random

locations = np.loadtxt('handled_data.txt')

x = locations[:, 0]
y = locations[:, 1]

def add_gauss_nosiy(datas, mu, sigma):
    mu_ = mu
    sigma_ = sigma
    data = datas.copy()
    for i in range(len(data)):
        data[i] += random.gauss(mu_, sigma_)
    return data


def main():
    gps_x = add_gauss_nosiy(x, 0, 2)
    gps_y = add_gauss_nosiy(y, 0, 2)

    gps_data = [gps_x, gps_y]

    rsu_x = add_gauss_nosiy(x, 0, 0.5)
    rsu_y = add_gauss_nosiy(y, 0, 0.5)

    rsu_data = [rsu_x, rsu_y]
    
    x_fuse = 0.1 * gps_data[0] + 0.9 * rsu_data[0]
    y_fuse = 0.1 * gps_data[1] + 0.9 * rsu_data[1]

    x_fuse = np.reshape(x_fuse, (len(x_fuse), 1))
    y_fuse = np.reshape(y_fuse, (len(y_fuse), 1))

    fuse_data = np.append(x_fuse, y_fuse, axis=1)

    np.savetxt('fuse_datas.txt', fuse_data, fmt='%s', delimiter=' ')

main()

