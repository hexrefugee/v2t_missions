import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a = np.reshape(a, (3, 1))
b = np.reshape(b, (3, 1))
c = np.append(a, b, axis=1)
print(c)