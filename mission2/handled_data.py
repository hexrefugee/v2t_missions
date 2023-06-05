import re
import numpy as np
txt_file = r'vehicle_location.txt'


def readTXT():
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    x_data = re.findall(".*x=(.*), y=.*", content)
    y_data = re.findall(".*y=(.*), z=.*", content)
    z_data = re.findall(".*z=(.*)\), R.*", content)

    arr1 = np.array(x_data)
    arr2 = np.array(y_data)
    arr3 = np.array(z_data)

    arr1 = np.reshape(arr1, (len(arr1), 1))
    arr2 = np.reshape(arr2, (len(arr2), 1))
    arr3 = np.reshape(arr3, (len(arr3), 1))
    result = np.append(arr1, arr2, axis=1)
    result = np.append(result, arr3, axis=1)
    # print(result)

    # np.savetxt('handled_data.txt', result, fmt='%s', delimiter=' ', newline='\n')
    np.savetxt('handled_data.txt', result, fmt='%s', delimiter=' ')

readTXT()


