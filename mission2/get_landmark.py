import numpy as np

d = 1.75

handled_data = np.loadtxt('handled_data.txt')
center_point = handled_data[:, [0, 1]]

right_landmark = []

for i in range(len(center_point)):
    if i == 0:
        v = center_point[i + 1] - center_point[i]
    elif i == len(center_point) - 1:
        v = center_point[i] - center_point[i - 1]
    else:
        v = center_point[i + 1] - center_point[i - 1]

    u = v / np.linalg.norm(v)
    right_landmark = center_point[i] + d*u

right_landmark = np.array(right_landmark)

np.savetxt('right_landmark.txt', right_landmark, fmt='%s', delimiter=' ')
