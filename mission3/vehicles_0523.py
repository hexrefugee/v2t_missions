import carla
import os
from agents.navigation.behavior_agent import BehaviorAgent

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        origin_settings = world.get_settings()

        output_path1 = 'lidar_data_ego'
        output_path2 = 'lidar_data_rsu'


        a_start_point = carla.Location(245.4, -8.4, 5)
        #                                         p，y，r 一般是使用y来控制方向
        v_a = carla.Transform(a_start_point, carla.Rotation(0,-90,0))
        b_start_point = carla.Location(242.4, -25, 5)
        v_b = carla.Transform(b_start_point, carla.Rotation(0,-90,0))
        ego_start_point = carla.Location(245.4, -19, 5)
        v_ego = carla.Transform(ego_start_point, carla.Rotation(0, -90, 0))

        a_end_point = carla.Location(0, -210, 0)
        end_point1 = carla.Transform(a_end_point)

        c_start_point = carla.Location(173, -194, 1)
        v_c = carla.Transform(c_start_point, carla.Rotation(0, 0, 0))
        d_start_point = carla.Location(168, -197, 1)
        v_d = carla.Transform(d_start_point, carla.Rotation(0, 0, 0))

        c_end_point = carla.Location(233.4, -8.4, 0)
        d_end_point = carla.Location(235.4, -8.4, 0)
        end_point2 = carla.Transform(c_end_point)
        end_point3 = carla.Transform(d_end_point)

        # 创建vehicle
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')


        ego_lidar_location = carla.Location(0, 0, 1.5)
        ego_lidar_rotation = carla.Rotation(0, 0, 0)
        va = world.spawn_actor(ego_vehicle_bp, v_a)
        vb = world.spawn_actor(ego_vehicle_bp, v_b)
        vego = world.spawn_actor(ego_vehicle_bp, v_ego)
        vc = world.spawn_actor(ego_vehicle_bp, v_c)
        vd = world.spawn_actor(ego_vehicle_bp, v_d)

        # 创建激光lidar
        lidar_bp_ego = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp_ego.set_attribute('channels', str(32))
        lidar_bp_ego.set_attribute('points_per_second', str(90000))
        lidar_bp_ego.set_attribute('rotation_frequency', str(40))
        lidar_bp_ego.set_attribute('range', str(20))

        lidar_ego_location = carla.Location(0, 0, 1.5)
        lidar_ego_rotation = carla.Rotation(0, 0, 0)
        lidar_ego_trasfrom = carla.Transform(lidar_ego_location, lidar_ego_rotation)
        lidar_ego = world.spawn_actor(lidar_bp_ego, lidar_ego_trasfrom, attach_to=vego)

        lidar_bp_rsu = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp_rsu.set_attribute('channels', str(64))
        lidar_bp_rsu.set_attribute('points_per_second', str(900000))
        lidar_bp_rsu.set_attribute('rotation_frequency', str(40))
        lidar_bp_rsu.set_attribute('range', str(150))
        lidar_rsu_location = carla.Location(240, -185, 3)
        lidar_rsu_rotation = carla.Rotation(0, 0, 0)
        lidar_rsu_trasfrom = carla.Transform(lidar_rsu_location, lidar_rsu_rotation)
        lidar_rsu = world.spawn_actor(lidar_bp_rsu, lidar_rsu_trasfrom)
        
        lidar_ego.listen(
            lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path1, '%06d.ply' % point_cloud.frame)))       
        lidar_rsu.listen(
            lambda point_cloud: point_cloud.save_to_disk(os.path.join(output_path2, '%06d.ply' % point_cloud.frame)))  

        vehicle_list = []

        vehicle_list.append(va)
        vehicle_list.append(vb)
        vehicle_list.append(vego)
        vehicle_list.append(vc)
        vehicle_list.append(vd)

        agent_a = BehaviorAgent(va, behavior='normal')
        agent_b = BehaviorAgent(vb, behavior='normal')
        agent_ego = BehaviorAgent(vego, behavior='normal')
        agent_c = BehaviorAgent(vc, behavior='normal')
        agent_d = BehaviorAgent(vd, behavior='normal')

        agent_a.set_destination(end_point1.location)
        agent_b.set_destination(end_point1.location)
        agent_ego.set_destination(end_point1.location)

        agent_c.set_destination(end_point2.location)
        agent_d.set_destination(end_point3.location)



        while True:
            agent_a._update_information()
            agent_b._update_information()
            agent_ego._update_information()
            agent_c._update_information()
            agent_d._update_information()

            world.tick()
            
            if (len(agent_a._local_planner._waypoints_queue) < 1):
                print('======== Success, Arrivied at Target Point!')
                break
                
            # 设置速度限制
            speed_limit1 = va.get_speed_limit()
            agent_a.get_local_planner().set_speed(speed_limit1)

            control1 = agent_a.run_step(debug=True)
            va.apply_control(control1)

            # speed_limit2 = vb.get_speed_limit()
            agent_b.get_local_planner().set_speed(speed_limit1)

            control2 = agent_b.run_step(debug=True)
            vb.apply_control(control2)

            # speed_limit3 = v_ego.get_speed_limit()
            agent_ego.get_local_planner().set_speed(speed_limit1)

            control3 = agent_ego.run_step(debug=True)
            vego.apply_control(control3)

            # speed_limit4 = v_c.get_speed_limit()
            agent_c.get_local_planner().set_speed(speed_limit1)

            control4 = agent_c.run_step(debug=True)
            vc.apply_control(control4)

            # speed_limit1 = vd.get_speed_limit()
            agent_d.get_local_planner().set_speed(speed_limit1)

            control5 = agent_d.run_step(debug=True)
            vd.apply_control(control5)
 


    finally:
        world.apply_settings(origin_settings)
        # for i in vehicle_list:
        #     i.destroy()
        va.destroy()
        vb.destroy()
        vego.destroy()
        vc.destroy()
        vd.destroy()
        lidar_rsu.destroy()
        lidar_ego.destroy()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
