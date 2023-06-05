#!/usr/bin/env python3
# coding:utf-8

import carla
import rospy
from test_pkg.msg import CarInfo  # 自定义消息格式

# 全局变量，记录当前路点
current_waypoint = None

# def has_passed_road(vehicle, road_id):
#     global current_waypoint

#     # 如果当前路点为 None，则获取车辆当前所在的路点
#     if current_waypoint is None:
#         current_location = vehicle.get_location()
#         current_waypoint = map_data.get_waypoint(current_location)

#     # 如果当前路点不在指定道路上，则更新当前路点为指定道路上的第一个路点
#     # if current_waypoint.road_id != road_id:
#     #     for waypoint in waypoints:
#     #         if waypoint.road_id == road_id:
#     #             current_waypoint = waypoint
#     #             break

#     # 检查车辆是否在当前路点可行驶区域内，如果在，则继续检查下一个路点；否则说明车辆已经离开当前道路
#     if current_waypoint.is_junction:
#         current_location = vehicle.get_location()
#         current_waypoint = map_data.get_waypoint(current_location)
#         print("current_waypoint: {}".format(current_waypoint))
#         return False
#     else:
#         location = vehicle.get_location()
#         distance = current_waypoint.transform.location.distance(location)
#         if distance <= 2.0:
#             current_waypoint = current_waypoint.next(2.0)[0]
#         print("current_waypoint: {}".format(current_waypoint))
#         return True

def has_passed_road(vehicle, road_id):
    current_waypoint = None

    # 如果当前路点为 None，则获取车辆当前所在的路点
    if current_waypoint is None:
        current_location = vehicle.get_location()
        current_waypoint = map_data.get_waypoint(current_location)
    if current_waypoint.road_id != road_id:
        # print("vechile current_waypoint: {}".format(current_waypoint))
        return False
    else:
        print(111111)
        # print("vehicle current_waypoint: {}".format(current_waypoint))
        return True


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    # Carla地图数据
    global map_data
    map_data = world.get_map()
    waypoints = map_data.generate_waypoints(2.0)

    # 车流量统计变量初始化
    vehicle_counter = 0

    try:
        # ROS节点初始化
        rospy.init_node('carla_vehicle_info_publisher', anonymous=True)
        car_info_pub = rospy.Publisher('car_info', CarInfo, queue_size=10)

        road_id = 67

        while True:
            # 获取所有车辆的位置信息
            vehicles_location = {}
            for actor in world.get_actors().filter('vehicle.*'):
                vehicle_id = actor.id
                vehicle_location = actor.get_location()
                vehicles_location[vehicle_id] = vehicle_location

                # 检查该车辆是否通过了指定道路，如果通过了，就发送出去
                if has_passed_road(actor, road_id):
                    vehicle_counter += 1
                    # 发布车辆ID和位置信息到ROS话题中
                    car_info_msg = CarInfo()
                    car_info_msg.vehicle_id = vehicle_id
                    car_info_msg.location = [vehicle_location.x, vehicle_location.y, vehicle_location.z]
                    print("The Vehicle ID: {} is on the road,The Location is: [{}, {}, {}]".format(vehicle_id, vehicle_location.x, vehicle_location.y, vehicle_location.z))
                    car_info_pub.publish(car_info_msg)
    
    finally:
        pass




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')