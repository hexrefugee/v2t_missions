目标：
第一步：使用carla采集车辆运行的一段路线的location，然后将location输出到txt文件中，并按需要排列好。

第二步：处理获取到的location.txt文件，数据格式由Location(x=229.000000, y=115.000000, z=0.946100) >>>  229.000000 115.000000 0.946100。

第三步：通过获得的waypoint点计算两边车道线的坐标

# get_location.py
功能：
    获取车辆从a点到b点的location，并保存为vehicle_location.txt文件。

# handled_data.py
功能：
    处理获得的txt文件，提取x,y,z的坐标，并保存到handled_data中。

# plot_data.py
功能：
    将离散点绘制出来

# calculate_landmark.py
    通过计算车运动方向的向量，加上车道宽，求出两边车道线坐标

"""
# 获取车辆的location使用函数get_location()

get_location(self)
Returns the actor's location the client recieved during last tick. The method does not call the simulator.

    Return: carla.Location - meters
    Setter: carla.Actor.set_location

"""

"""
# 打开一个txt文件，将vehicle的location写入进去
使用str来写入
使用python中的open()函数
具体用法：
xxx = open('x.txt', 'w') //其中w表示写入

获取vehicle的location并写入到x.txt文件中去，一定要加入'\n'
xxx.write(str(vehicle.get_location()) + '\n')

"""

"""
# 误区：
# 将os.path.join的作用和open()函数的作用搞混了
# os.path.join主要作用是针对文件夹的，

举例：
import os

Path1 = 'hhh'
Path2 = 'xxx'
Path3 = 'zzz'

Path10 = Path1 + Path2 + Path3
Path20 = os.path.join(Path1, Path2, Path3)
print('Path10 =', Path10)
print('Path20 =', Path20)

//输出结果：
Path10 = hhhxxxzzz
Path20 = hhh/xxx/zzz

所以可以理解之间需要存储点云数据的时候使用os包了
"""

"""
本来准备使用numpy来处理获得的txt文件，但尝试了一下发现没有好的函数，最后决定使用re，正则表达式来处理

# 使用re.findall(pattern, string)
# 定义正则表达式模式
# pattern = r'(?<=<).*?(?=>)'
# 从(?<=<)到(?=>)之前的字符串
# pattern = r'.*x=(.*?) y=.*'

with open(txt_file, 'r', encoding='utf-8') as f:
    content = f.read()

x_data = re.findall(".*x=(.*), y=.*", content)
y_data = re.findall(".*y=(.*),.*", content)
z_data = re.findall(".*z=(.*)", content)
"""

"""
# 处理后得到了三个list，要把它们的每一行都合并，最后还是使用了numpy来处理

使用np.reshape(len(col1), 1)将每一个list变成n行1列
然后使用np.append(col1, col2, axis=1)函数，将col1和col2按每行拼在一起，axis=0是列，最多只能拼2行
最后使用np.savetxt()函数，将结果保存为txt文件，注意参数要设置成fmt="%s"才能运行。
"""

