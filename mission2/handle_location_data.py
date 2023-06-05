import numpy as np


file_name = 'vehicle_location.txt'
data = np.loadtxt(file_name, dtype='str', delimiter=',', usecols=(1))
print(data)







# with open('handle_date.txt', 'a') as file:
#     write_str = '%f %f %f\n' %(float_data1, float_data2, float_data3)
#     file.write(write_str)








