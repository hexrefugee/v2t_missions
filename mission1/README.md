author：HHH
repo：实现多辆车搭载lidar在地图里面运行，并采集数据

functions:

all_vehicle.py:
    获取carla中所有的vehicle模型，并写入all_vehicle.txt文件中去。

show_point.py
    在地图上显示设定的点。

vehiclefrom_a2b.py:
    不添加tm的情况下，最多只能使用2辆车。

vehicles_lidar.py:
    不使用tm的情况下，两辆车搭载lidar测试。
    测试通过，两辆搭载了lidar的车辆正常运行。
    再次测试，3辆车可以正常搭载ldar运行，
    发现一个小trick，在函数：
        agent3 = BehaviorAgent(vehicle3, behavior='normal')
    中BehaviorAgent函数的第一个参数可以用来跟随，
    设置成vehicle2就可以完全和vehicle2一样的操作

TM_test.py:
    尝试使用tm来管理车辆。

vehiclesfrom_a2b.py:
    添加了5辆车，可以正常运行 。

vehicle_rotation.py
    一辆车循环运行