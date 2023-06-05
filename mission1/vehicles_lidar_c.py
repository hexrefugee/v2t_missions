import sys
import glob
import os

try:
    sys.path.append(glob.glob('../carla/dist/new/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
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

        # output_path1 = 'lidar_data1'
        # output_path2 = 'lidar_data2'
        # output_path3 = 'lidar_data3'
        output_path = 'lidar_data'
        # 确定起点和终点
        p1 = carla.Location(5.8, -36, 1)
        p2 = carla.Location(5.8, -45, 1)
        # p3 = carla.Location(7, -60, 1)
        p6 = carla.Location(7, -130, 1)
        
        s1 = carla.Transform(p1, carla.Rotation(0,90,0))
        s2 = carla.Transform(p2, carla.Rotation(0,90,0))
        # s3 = carla.Transform(p3, carla.Rotation(0,90,0))
        end_point = carla.Transform(p6, carla.Rotation(0, 0, 0))


        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)
        vehicle2 = world.spawn_actor(ego_vehicle_bp, s2)
        # vehicle3 = world.spawn_actor(ego_vehicle_bp, s3)

        #创建lidar
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(128))
        lidar_bp.set_attribute('points_per_second', str(46080000))
        lidar_bp.set_attribute('rotation_frequency', str(20))
        lidar_bp.set_attribute('range', str(200))
        lidar_bp.set_attribute('upper_fov', str(25))
        lidar_bp.set_attribute('lower_fov', str(-15))

        # 设置lidar架设的点
        lidar_location = carla.Location(-11,-72,2)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)        
        # 生成lidar并采集数据
        lidar = world.spawn_actor(lidar_bp, lidar_transform)
        # lidar1 = world.spawn_actor(lidar_bp, lidar_transform)
        # lidar2 = world.spawn_actor(lidar_bp, lidar_transform)
        # lidar3 = world.spawn_actor(lidar_bp, lidar_transform)
        # lidar1.listen(
        #     lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path1, '%06d.ply' % point_cloud.frame)))       
        # lidar2.listen(
        #     lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path2, '%06d.ply' % point_cloud.frame)))  
        # lidar3.listen(
        #     lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path3, '%06d.ply' % point_cloud.frame)))  
        lidar.listen(
            lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path, '%06d.ply' % point_cloud.frame))) 
 
        world.tick()
 
        # 设置车辆的驾驶模式
        agent1 = BehaviorAgent(vehicle1, behavior='normal')
        agent2 = BehaviorAgent(vehicle2, behavior='normal')
        

        agent1.set_destination(end_point.location)
        agent2.set_destination(end_point.location)
        # agent3.set_destination(end_point.location)

 
        while True:
            agent1._update_information()
            agent2._update_information()
            # agent3._update_information()
            

 
            world.tick()
            
            if len(agent1._local_planner._waypoints_queue) < 1 | len(agent2._local_planner._waypoints_queue) < 1:
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

            # speed_limit3 = vehicle3.get_speed_limit()
            # agent3.get_local_planner().set_speed(speed_limit3)
 
            # control3 = agent3.run_step(debug=True)
            # vehicle3.apply_control(control3)
            


    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()
        vehicle2.destroy()
        lidar.destroy()

 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
