# -*- coding: utf-8 -*-
 
 
import os
import random
import sys
 
import carla
 
from agents.navigation.behavior_agent import BehaviorAgent
 
 
def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()
 
 
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
 
        blueprint_library = world.get_blueprint_library()
 
        # 确定起点和终点
        p11 = carla.Location(50, 5.5, 1)
        p12 = carla.Location(80, 6, 1)
        p21 = carla.Location(180, 6.5, 1)
        p22 = carla.Location(140, 7, 1)
        start_point1 = carla.Transform(p11, carla.Rotation(0,0,0))
        start_point2 = carla.Transform(p12, carla.Rotation(0,0,0))
        end_point1 = carla.Transform(p21, carla.Rotation(0, 0, 0))
        end_point2 = carla.Transform(p21, carla.Rotation(0, 0, 0))
        
        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, start_point1)
        vehicle2 = world.spawn_actor(ego_vehicle_bp, start_point2)
 
        world.tick()
 
        # 设置车辆的驾驶模式
        agent1 = BehaviorAgent(vehicle1, behavior='normal')
        agent2 = BehaviorAgent(vehicle2, behavior='normal')
        # 核心函数
        # agent.set_destination(agent.vehicle.get_location(), end_point.location, clean=True)
        agent1.set_destination(end_point1.location)
        agent2.set_destination(end_point2.location)
 
        while True:
            agent1._update_information()
            agent2._update_information()
 
            world.tick()
            
            if len(agent1._local_planner._waypoints_queue) < 1 and len(agent2._local_planner._waypoints_queue) < 1:
                print('======== Success, Arrivied at Target Point!')
                break
                
            # 设置速度限制
            speed_limit1 = vehicle1.get_speed_limit()
            agent1.get_local_planner().set_speed(speed_limit1)
 
            control1 = agent1.run_step(debug=True)
            vehicle1.apply_control(control1)

            speed_limit2 = vehicle2.get_speed_limit()
            agent2.get_local_planner().set_speed(speed_limit1)
 
            control2 = agent2.run_step(debug=True)
            vehicle2.apply_control(control2)
 
    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()
        vehicle2.destroy()
 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')