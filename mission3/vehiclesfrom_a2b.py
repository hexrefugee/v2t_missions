import carla
import os
from agents.navigation.behavior_agent import BehaviorAgent

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()
        
        output_path1 = 'lidar_data1'
        output_path2 = 'lidar_data2'
 
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
 
        blueprint_library = world.get_blueprint_library()
 
        # 确定起点和终点
        p1 = carla.Location(175, -169, 1)
        p2 = carla.Location(225, -173, 1)
        # 终点
        p3 = carla.Location(230, -169, 0)
        p4 = carla.Location(160, -173, 0)
        
        s1 = carla.Transform(p1, carla.Rotation(0,0,0))
        s2 = carla.Transform(p2, carla.Rotation(0,180,0))

        e1 = carla.Transform(p3, carla.Rotation(0, 0, 0))
        e2 = carla.Transform(p4, carla.Rotation(0, 0, 0))


        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)
        vehicle2 = world.spawn_actor(ego_vehicle_bp, s2)
 
        world.tick()

        # 创建激光lidar
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(90000))
        lidar_bp.set_attribute('rotation_frequency', str(40))
        lidar_bp.set_attribute('range', str(20))
        # 设置激光雷达的两个点
        lidar1_location = carla.Location(195, -165, 1)
        lidar1_rotation = carla.Rotation(0, 0, 0)
        lidar1_transform = carla.Transform(lidar1_location, lidar1_rotation)

        lidar2_location = carla.Location(207, -178, 1)
        lidar2_rotation = carla.Rotation(0, 0, 0)
        lidar2_transform = carla.Transform(lidar2_location, lidar2_rotation)
        lidar1 = world.spawn_actor(lidar_bp, lidar1_transform)
        lidar2 = world.spawn_actor(lidar_bp, lidar2_transform)
        lidar1.listen(
            lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path1, '%06d.ply' % point_cloud.frame)))       
        lidar2.listen(
            lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path2, '%06d.ply' % point_cloud.frame)))  
 
        # 设置车辆的驾驶模式
        agent1 = BehaviorAgent(vehicle1, behavior='normal')
        agent2 = BehaviorAgent(vehicle2, behavior='normal')

        # 核心函数
        agent1.set_destination(e1.location)
        agent2.set_destination(e2.location)

 
        while True:
            agent1._update_information()
            agent2._update_information()
 
            world.tick()
            
            if (len(agent1._local_planner._waypoints_queue) < 1):
                print('======== Success, Arrivied at Target Point!')
                break
                
            # 设置速度限制
            speed_limit1 = vehicle1.get_speed_limit()
            agent1.get_local_planner().set_speed(speed_limit1)
 
            control1 = agent1.run_step(debug=True)
            vehicle1.apply_control(control1)

            speed_limit2 = vehicle2.get_speed_limit()
            agent2.get_local_planner().set_speed(speed_limit2)
 
            control2 = agent2.run_step(debug=True)
            vehicle2.apply_control(control2)

 
    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()
        vehicle2.destroy()
        # lidar1.destroy()
        # lidar2.destroy()

 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
