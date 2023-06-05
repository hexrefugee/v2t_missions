#!/usr/bin/env python
# coding:utf-8

import cv2
import rospy
from test_pkg.msg import CarInfo  # 自定义消息格式
import time
import numpy as np


def car_info_callback(car_info_msg):
    """
    当收到名为 `car_info` 的消息时，执行此回调函数。
    """
    # 解析车辆 ID 和位置坐标，并添加到 `vehicles` 列表中。
    vehicle_id = car_info_msg.vehicle_id
    location_x, location_y, _ = car_info_msg.location
    location_x = location_x * 5
    location_y = location_y * 3
    vehicles[vehicle_id] = (int(location_x), int(location_y)), time.time()
    # vehicles.append((vehicle_id, (int(location_x), int(location_y))))

vehicles = {}   # 存储车辆位置信息和更新时间的字典

def main():

    try:
        # 初始化 ROS 节点和 OpenCV 窗口
        rospy.init_node('carla_vehicle_info_subscriber', anonymous=True)
        # cv2.namedWindow('carla_local_dynamic_map', cv2.WINDOW_NORMAL)

        # 创建 ROS 订阅者
        rospy.Subscriber('car_info', CarInfo, car_info_callback)


        while True:
            # 循环读取 `vehicles` 列表中的所有车辆位置，并将它们画在图像上。
            # img = cv2.imread('path/to/map/image')  # 读取地图图片
            img = np.zeros((1000, 2000, 3), dtype=np.uint8)
            img.fill(255)
            current_time = time.time()  # 当前时间戳
            to_remove = []  # 需要删除的车辆 ID 列表
            for vehicle_id, (location, update_time) in vehicles.items():
                if current_time - update_time > 1.0:  # 如果车辆信息已经过时
                    to_remove.append(vehicle_id)
                else:
                    cv2.circle(img, location, 5, (0, 0, 255), -1)  # 绘制红色圆形

            # 从 `vehicles` 中删除已经过时的车辆
            for vehicle_id in to_remove:
                del vehicles[vehicle_id]

            # 在窗口中显示绘制好的图像，直到用户按下 ESC 键退出程序。
            cv2.imshow('carla_local_dynamic_map', img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 如果用户按下 ESC 键
                break
    finally:
        print('\ndone.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')