#!/usr/bin/env python
#coding:utf-8
# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys
import random
import argparse
import time
from datetime import datetime
from matplotlib.pyplot import pause
import numpy as np
from matplotlib import cm
import open3d as o3d

from queue import Queue
from queue import Empty
#import Queue
# try:
#     sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
#         sys.version_info.major,
#         sys.version_info.minor,
#         'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
# except IndexError:
#     pass

import carla
# To import a basic agent
from agents.navigation.basic_agent import BasicAgent
# To import a behavior agent
from agents.navigation.behavior_agent import BehaviorAgent
from agents.navigation.local_planner import RoadOption

geo_ref = carla.GeoLocation(0.0, 0.0, 0.0)


def geo_to_transform(lat, lon, alt, lat_0, lon_0, alt_0):
    """
    Convert WG84 to ENU. The origin of the ENU should pass the geo reference.
    Note this function is a writen by reversing the
    official API transform_to_geo.
    """
    EARTH_RADIUS_EQUA = 6378137.0
    scale = np.cos(np.deg2rad(lat_0))

    mx = lon * np.pi * EARTH_RADIUS_EQUA * scale / 180
    mx_0 = scale * np.deg2rad(lon_0) * EARTH_RADIUS_EQUA
    x = mx - mx_0

    my = np.log(np.tan((lat + 90) * np.pi / 360)) * EARTH_RADIUS_EQUA * scale
    my_0 = scale * EARTH_RADIUS_EQUA * \
        np.log(np.tan((90 + lat_0) * np.pi / 360))
    y = -(my - my_0)
    z = alt - alt_0
    return x, y, z


actor_list = []
#os.remove("gnss_record.txt")
file = open("gnss_record.txt", 'w')


def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    """
    if 'lidar' in sensor_name:
        sensor_data.save_to_disk(os.path.join('../outputs/output_synchronized', '%06d.ply' % sensor_data.frame))
    if 'camera' in sensor_name:
        sensor_data.save_to_disk(os.path.join('../outputs/output_synchronized', '%06d.png' % sensor_data.frame))
    if 'SemanticLidar' in sensor_name:
        sensor_data.save_to_disk('/home/v2t-sim/carlaCache/SemanticLidarMeasurement/%d.ply' % sensor_data.frame)
    """
    #print('\nsensor_name: %s ' %(sensor_name))
    # print('\nsensor_size: ',len(sensor_name))
    # print('\nsensor_type: ',type(sensor_name))
    if 'gnss_1' == sensor_name:
        #print("GNSS measure:\n"+str(gnss)+'\n')
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 1 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_2' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 2 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_3' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 3 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_4' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 4 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_5' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 5 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_6' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 6 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_7' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 7 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_8' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 8 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_9' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 9 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    elif 'gnss_10' == sensor_name:
        x, y, z = geo_to_transform(sensor_data.latitude,
                                   sensor_data.longitude,
                                   sensor_data.altitude,
                                   geo_ref.latitude,
                                   geo_ref.longitude, 0.0)
        file.write("%d 10 %f %f %f %f\n" %
                   (sensor_data.frame, sensor_data.transform.location.x, sensor_data.transform.location.y, x, y))
    sensor_queue.put((sensor_data.frame, sensor_name))


def main():
    # We start creating the client
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    #world = client.load_world('Town10HD_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)   #Town01_Opt
    world = client.get_world()
    #world = client.load_world(args.map)
    sensor_list = []
    try:
        # # We need to save the settings to be able to recover them at the end
        # # of the script to leave the server in the same state that we found it.
        original_settings = world.get_settings()
        settings = world.get_settings()

        # weather = carla.WeatherParameters(cloudiness=10.0,
        #                                   precipitation=10.0,
        #                                   fog_density=10.0)
        # world.set_weather(weather)
        # map_ = world.get_map()
        # map_.save_to_disk('/home/v2t-sim/carlaCache/%s.xodr' % map_.name)
        # # We set CARLA syncronous mode
        settings.fixed_delta_seconds = 0.05    # 0.2
        settings.synchronous_mode = True
        world.apply_settings(settings)
        traffic_manager = client.get_trafficmanager()
        traffic_manager.set_synchronous_mode(True)
        # world.unload_map_layer(carla.MapLayer.Buildings)
        # world.unload_map_layer(carla.MapLayer.StreetLights)
        # world.unload_map_layer(carla.MapLayer.Foliage)
        # NONE
        # No layers selected.
        # Buildings
        # Decals
        # Foliage
        # Ground
        # ParkedVehicles
        # Particles
        # Props
        # StreetLights
        # Walls
        # All
        # # We create the sensor queue in which we keep track of the information
        # # already received. This structure is thread safe and can be
        # # accessed by all the sensors callback concurrently without problem.
        sensor_queue = Queue()
        # sensor_queue = queue.Queue()

        # geo_ref = map_.transform_to_geolocation(carla.Location(x=0, y=0, z=0))
##############################################################
##               生成vehicle
##############################################################
        # vehicle_loc_list = [
        #     carla.Location(10, -65, 2),
        #     carla.Location(18, -65, 2),
        #     carla.Location(30, -65, 2),
        #     carla.Location(39, -65, 2),
        #     carla.Location(47, -65, 2),

        #     carla.Location(10, -68, 2),
        #     carla.Location(20, -68, 2),
        #     carla.Location(28, -68, 2),
        #     carla.Location(38, -68, 2),
        #     carla.Location(45, -68, 2),
        # ]
        vehicle_loc_list = [
            carla.Location(74, 134.4, 2),
            carla.Location(66, 134.4, 2),
            carla.Location(57, 134.4, 2),
            carla.Location(47, 134.4, 2),
            carla.Location(39, 134.4, 2),

            carla.Location(74, 129.8, 2),
            carla.Location(67, 129.8, 2),
            carla.Location(56, 129.8, 2),
            carla.Location(48, 129.8, 2),
            carla.Location(39, 129.8, 2),
        ]
##############################################################
##               生成sensor
##############################################################
        ## Bluepints for the sensors
        blueprint_library = world.get_blueprint_library()
        cam_bp = blueprint_library.find('sensor.camera.rgb')
        cam_bp.set_attribute('image_size_x', str(800))  # width
        cam_bp.set_attribute('image_size_y', str(600))  # height
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('range', str(100.0))
        lidar_bp.set_attribute('points_per_second', str(56000))  # 100000
        # 旋转频率和模拟的 FPS 应该相等，1/0.05=20.0
        lidar_bp.set_attribute('rotation_frequency', str(20.0))
        lidar_bp.set_attribute('upper_fov', str(10.0))
        lidar_bp.set_attribute('lower_fov', str(-30.0))
        #lidar_bp.set_attribute('atmosphere_attenuation_rate', 0.004	)
        #lidar_bp.set_attribute('dropoff_general_rate', 0.45	)   #随机丢弃的点的比例。这是在跟踪之前完成的，这意味着不计算丢弃的点，因此可以提高性能。
        Gnss_bp = blueprint_library.find('sensor.other.gnss')
        Gnss_bp.set_attribute('noise_alt_bias', str(0))
        Gnss_bp.set_attribute('noise_alt_stddev', str(0))
        # 纬度噪声模型中的平均参数。   random.seed(args.seed)
        Gnss_bp.set_attribute('noise_lat_bias', str(0))
        Gnss_bp.set_attribute('noise_lat_stddev', str(10))  # 纬度噪声模型中的标准偏差参数
        Gnss_bp.set_attribute('noise_lon_bias', str(0))
        Gnss_bp.set_attribute('noise_lon_stddev', str(10))
        Gnss_bp.set_attribute('noise_seed', str(0))
        i = 0
        vehicle_list = ['vehicle.tesla.model3', 'vehicle.seat.leon',
                        'vehicle.dodge.charger_2020', 'vehicle.chevrolet.impala']    #
        for vehicle_loc in vehicle_loc_list:
            i = i+1
            #ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
            #ego_bp = random.choice(world.get_blueprint_library().filter('vehicle.*.*'))
            ego_bp = world.get_blueprint_library().find(random.choice(vehicle_list))
            ego_bp.set_attribute('role_name', 'ego_'+str(i))
            #ego_vehicle_bp.set_attribute('color', '0, 0, 0')
            ego_color = random.choice(
                ego_bp.get_attribute('color').recommended_values)
            ego_bp.set_attribute('color', ego_color)
            spawn_waypoint = world.get_map().get_waypoint(
                vehicle_loc, project_to_road=False, lane_type=carla.LaneType.Any)
            print('\n%d wanted_location  :  X: %f, Y: %f' %
                  (i, vehicle_loc.x, vehicle_loc.y))
            print('%d spawn_waypoint  :  X: %f, Y: %f' %
                  (i, spawn_waypoint.transform.location.x, spawn_waypoint.transform.location.y))
            spwawn_location = carla.Location(spawn_waypoint.transform.location.x,
                                             spawn_waypoint.transform.location.y, spawn_waypoint.transform.location.z+5)
            spwawn_rotation = carla.Rotation(0, 180, 0)  # p y r
            spwawn_transform = carla.Transform(
                spwawn_location, spwawn_rotation)
            vehicle_01 = world.spawn_actor(ego_bp, spwawn_transform)
            # control = carla.VehicleControl()
            # control.throttle = 0.0
            # control.brake = 1.0
            # control.hand_brake = True
            # vehicle_01.apply_control(control)
            # physics_control = vehicle_01.get_physics_control()
            # physics_control.use_sweep_wheel_collision = True
            # vehicle_01.apply_physics_control(physics_control)
            # velo_01 = carla.Vector3D(0, 0, 0)
            # vehicle_01.set_target_velocity(velo_01)
            print('ego_%d is spawned' % i)
            #vehicle_01.set_autopilot(True)
            actor_list.append(vehicle_01)
            ## sensor
            spwawn_location = carla.Location(0, 0, 0)
            spwawn_rotation = carla.Rotation(0, 0, 0)
            spwawn_transform = carla.Transform(
                spwawn_location, spwawn_rotation)
            gnss01 = world.spawn_actor(
                Gnss_bp, spwawn_transform, attach_to=vehicle_01)
            if i == 1:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_1"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 2:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_2"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 3:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_3"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 4:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_4"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 5:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_5"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 6:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_6"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 7:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_7"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 8:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_8"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 9:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_9"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            elif i == 10:
                gnss01.listen(lambda data: sensor_callback(
                    data, sensor_queue, "gnss_10"))
                print('gnss_%d is spawned' % i)
                sensor_list.append(gnss01)
            time.sleep(0.1)
        # while True:
        #     pause
        dt0 = datetime.now()
        world.tick()
##############################################################
##               代理
##############################################################
        ## To start a basic agent
        #agent0 = BasicAgent(actor_list[0])
        ## To start a behavior agent with an aggressive profile
        # behavior='aggressive' cautious, normal, and aggressive
        # 下次用class 写会简洁一些 孙220807
        agent0 = BehaviorAgent(actor_list[0], behavior='normal')
        agent1 = BehaviorAgent(actor_list[1], behavior='normal')
        agent2 = BehaviorAgent(actor_list[2], behavior='normal')
        agent3 = BehaviorAgent(actor_list[3], behavior='normal')
        agent4 = BehaviorAgent(actor_list[4], behavior='normal')

        agent5 = BehaviorAgent(actor_list[5], behavior='normal')
        agent6 = BehaviorAgent(actor_list[6], behavior='normal')
        agent7 = BehaviorAgent(actor_list[7], behavior='normal')
        agent8 = BehaviorAgent(actor_list[8], behavior='normal')
        agent9 = BehaviorAgent(actor_list[9], behavior='normal')
        #destination = carla.Location(-55, 140, 0)  # (94.3, 129.4, 0)
        agent0.max_speed = 55
        agent1.max_speed = 55
        agent2.max_speed = 55
        agent3.max_speed = 52
        agent4.max_speed = 50
        agent5.max_speed = 55
        agent6.max_speed = 55
        agent7.max_speed = 55
        agent8.max_speed = 52
        agent9.max_speed = 50
        agent0.min_proximity_threshold = 5
        agent1.min_proximity_threshold = 5
        agent2.min_proximity_threshold = 5
        agent3.min_proximity_threshold = 5
        agent4.min_proximity_threshold = 5
        agent5.min_proximity_threshold = 5
        agent6.min_proximity_threshold = 5
        agent7.min_proximity_threshold = 5
        agent8.min_proximity_threshold = 5
        agent9.min_proximity_threshold = 5

        # spawn_points = world.get_map().get_spawn_points()
        # random.shuffle(spawn_points)
        # destination = random.choice(spawn_points).location
        destination_list_up = [
            carla.Location(-107.6, 80.3, 0),  # 大弯出1
            carla.Location(-106.6, -19.8, 0),  # 小弯in2
            carla.Location(-74.9, -61.2, 0),  # 小弯出2
            carla.Location(-64.8, -61.2, 0),  # 小弯in3
            carla.Location(-64.8, -61.2, 0),  # 小弯in3
            carla.Location(-48.5, -49.6, 0),  # 小弯3出
            carla.Location(-48.5, 113.9, 0),  # 停
        ]
        destination_list_down = [
            carla.Location(-104.0, 70.3, 0),  # 大弯出1   -104.0 , 80.3
            carla.Location(-103.3, -19.8, 0),  # 小弯in2
            # carla.Location(-95.9, -46.1, 0),
            # carla.Location(-92.4, -48.8, 0),
            # carla.Location(-81.9, -55.8, 0),
            carla.Location(-74.9, -57.9, 0),  # 小弯出2
            carla.Location(-64.8, -57.9, 0),  # 小弯in3
            #carla.Location(-52.2, -49.6, 0),  # 小弯3出
            carla.Location(-51.8, 113.9, 0),  # 停
        ]
        agent0.set_destination(destination_list_up[0])
        agent1.set_destination(destination_list_up[0])
        agent2.set_destination(destination_list_up[0])
        agent3.set_destination(destination_list_up[0])
        agent4.set_destination(destination_list_up[0])

        agent5.set_destination(destination_list_down[0])
        agent6.set_destination(destination_list_down[0])
        agent7.set_destination(destination_list_down[0])
        agent8.set_destination(destination_list_down[0])
        agent9.set_destination(destination_list_down[0])

        agent0.ignore_traffic_lights(active=True)
        agent1.ignore_traffic_lights(active=True)
        agent2.ignore_traffic_lights(active=True)
        agent3.ignore_traffic_lights(active=True)
        agent4.ignore_traffic_lights(active=True)
        agent5.ignore_traffic_lights(active=True)
        agent6.ignore_traffic_lights(active=True)
        agent7.ignore_traffic_lights(active=True)
        agent8.ignore_traffic_lights(active=True)
        agent9.ignore_traffic_lights(active=True)

        agent0.follow_speed_limits(value=False)
        agent1.follow_speed_limits(value=False)
        agent2.follow_speed_limits(value=False)
        agent3.follow_speed_limits(value=False)
        agent4.follow_speed_limits(value=False)
        agent5.follow_speed_limits(value=False)
        agent6.follow_speed_limits(value=False)
        agent7.follow_speed_limits(value=False)
        agent8.follow_speed_limits(value=False)
        agent9.follow_speed_limits(value=False)
        # agent0.ignore_vehicles(active=True)
        # agent1.ignore_vehicles(active=True)
        # agent2.ignore_vehicles(active=True)
        # agent3.ignore_vehicles(active=True)
        # agent4.ignore_vehicles(active=True)
        # agent5.ignore_vehicles(active=True)
        # agent6.ignore_vehicles(active=True)
        # agent7.ignore_vehicles(active=True)
        # agent8.ignore_vehicles(active=True)
        # agent9.ignore_vehicles(active=True)
    # VOID = -1
    # LEFT = 1
    # RIGHT = 2
    # STRAIGHT = 3
    # LANEFOLLOW = 4
    # CHANGELANELEFT = 5
    # CHANGELANERIGHT = 6
        # get_waypoint = [
        #     [world.get_map().get_waypoint(carla.Location(-65.2, 133.1, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-107.6, 80.3, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-106.6, -19.8, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-74.9, -61.2, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-64.8, -61.2, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-48.5, -49.6, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        #     [world.get_map().get_waypoint(carla.Location(-48.5, 113.9, 0), project_to_road=False, lane_type=carla.LaneType.Any),RoadOption.LANEFOLLOW],
        # ]
        # agent4.set_global_plan(get_waypoint,stop_waypoint_creation=True, clean_queue=True)   # plan_down
        ## Main loop
        ll = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        while True:
            world.tick()
            w_frame = world.get_snapshot().frame
            #print("\nWorld's frame: %d" % w_frame)
            process_time = datetime.now() - dt0
            if agent0.done():
                if ll[0] == 3:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-60.7, -62.2, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -57.0, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -48.3, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent0.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[0] = ll[0]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[0] = ll[0]+1
                    destination = destination_list_up[ll[0]]
                    agent0.set_destination(destination)
                #break
            if agent1.done():
                if ll[1] == 3:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-60.7, -62.2, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -57.0, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -48.3, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent1.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[1] = ll[1]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[1] = ll[1]+1
                    destination = destination_list_up[ll[1]]
                    agent1.set_destination(destination)
                #break
            if agent2.done():
                if ll[2] == 3:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-60.7, -62.2, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -57.0, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -48.3, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent2.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[2] = ll[2]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[2] = ll[2]+1
                    destination = destination_list_up[ll[2]]
                    agent2.set_destination(destination)
                #break
            if agent3.done():
                if ll[3] == 3:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-60.7, -62.2, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -57.0, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -48.3, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent3.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[3] = ll[3]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[3] = ll[3]+1
                    destination = destination_list_up[ll[3]]
                    agent3.set_destination(destination)
                #break
            if agent4.done():
                if ll[4] == 3:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-60.7, -62.2, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -57.0, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                        [world.get_map().get_waypoint(carla.Location(-50, -48.3, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent4.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[4] = ll[4]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[4] = ll[4]+1
                    destination = destination_list_up[ll[4]]
                    agent4.set_destination(destination)
            if agent5.done():
                if ll[5] == 0:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-103.3, -19.8, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent5.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[5] = ll[5]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[5] = ll[5]+1
                    destination = destination_list_down[ll[5]]
                    agent5.set_destination(destination)
            if agent6.done():
                if ll[6] == 0:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-103.3, -19.8, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent6.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[6] = ll[6]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[6] = ll[6]+1
                    destination = destination_list_down[ll[6]]
                    agent6.set_destination(destination)
            if agent7.done():
                if ll[7] == 0:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-103.3, -19.8, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent7.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[7] = ll[7]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[7] = ll[7]+1
                    destination = destination_list_down[ll[7]]
                    agent7.set_destination(destination)
            if agent8.done():
                if ll[8] == 0:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-103.3, -19.8, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent8.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[8] = ll[8]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[8] = ll[8]+1
                    destination = destination_list_down[ll[8]]
                    agent8.set_destination(destination)
            if agent9.done():
                if ll[9] == 0:
                    get_waypoint = [
                        [world.get_map().get_waypoint(carla.Location(-103.3, -19.8, 0),
                                                      project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    ]
                    agent9.set_global_plan(
                        get_waypoint, stop_waypoint_creation=True, clean_queue=True)   # plan_down
                    ll[9] = ll[9]+1
                else:
                    print("The target has been reached, stopping the simulation")
                    ll[9] = ll[9]+1
                    destination = destination_list_down[ll[9]]
                    agent9.set_destination(destination)
                #break
            # actor_list[0].apply_control(agent0.run_step(debug=True))
            # actor_list[0].apply_control(agent0.run_step())
            dt0 = datetime.now()
            control = agent0.run_step()
            control.manual_gear_shift = False
            actor_list[0].apply_control(control)

            control = agent1.run_step()
            control.manual_gear_shift = False
            actor_list[1].apply_control(control)

            control = agent2.run_step()
            control.manual_gear_shift = False
            actor_list[2].apply_control(control)

            control = agent3.run_step()
            control.manual_gear_shift = False
            actor_list[3].apply_control(control)

            control = agent4.run_step()
            control.manual_gear_shift = False
            actor_list[4].apply_control(control)

            control = agent5.run_step()
            control.manual_gear_shift = False
            actor_list[5].apply_control(control)

            control = agent6.run_step()
            control.manual_gear_shift = False
            actor_list[6].apply_control(control)

            control = agent7.run_step()
            control.manual_gear_shift = False
            actor_list[7].apply_control(control)

            control = agent8.run_step()
            control.manual_gear_shift = False
            actor_list[8].apply_control(control)

            control = agent9.run_step()
            control.manual_gear_shift = False
            actor_list[9].apply_control(control)
            # Now, we wait to the sensors data to be received.
            # As the queue is blocking, we will wait in the queue.get() methods
            # until all the information is processed and we continue with the next frame.
            # We include a timeout of 1.0 s (in the get method) and if some information is
            # not received in this time we continue.
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(True, 1.0)
                    # print("    Frame: %d   Sensor: %s" %
                    #       (s_frame[0], s_frame[1]))

            except Queue.Empty():
                print("    Some of the sensor information is missed")
    finally:
        world.apply_settings(original_settings)
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        for sensor in sensor_list:
            sensor.destroy()
        file.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
