import carla
import os
import random

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.get_world()

        origin_settings = world.get_settings()


        settings = world.get_settings()
        synchronous_master = False
        settings.synchronous_mode = True
        # 20FPS
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)    

        # tm管理器
        traffic_manager = client.get_trafficmanager(8000)
        # every vehicle keeps a distance of 3.0 meter
        traffic_manager.set_global_distance_to_leading_vehicle(3.0)
        # Set physical mode only for cars around ego vehicle to save computation
        # traffic_manager.set_hybrid_physics_mode(True)
        # default speed is 30
        traffic_manager.global_percentage_speed_difference(80)
        traffic_manager.set_synchronous_mode(True)

        # 获取车辆蓝图
        blueprints_vehicle = world.get_blueprint_library().filter("vehicle.*")
        # sort the vehicle list by id
        blueprints_vehicle = sorted(blueprints_vehicle, key=lambda bp: bp.id)

        # 设置起点和终点
        p1 = carla.Location(229, 115, 1)
        p2 = carla.Location(229, 105, 1)
        p3 = carla.Location(229, 95, 1)
        p4 = carla.Location(229, 85, 1)
        p5 = carla.Location(229, 75, 1)        
        p6 = carla.Location(20, 194, 1)

        s1 = carla.Transform(p1, carla.Rotation(0,90,0))
        s2 = carla.Transform(p2, carla.Rotation(0,90,0))
        s3 = carla.Transform(p3, carla.Rotation(0,0,0))
        s4 = carla.Transform(p4, carla.Rotation(0,0,0))
        s5 = carla.Transform(p5, carla.Rotation(0,0,0))
        end_point = carla.Transform(p6, carla.Rotation(0, 0, 0))     

        

    finally:
        