import carla

from agents.navigation.behavior_agent import BehaviorAgent
from agents.navigation.local_planner import RoadOption


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

        # 设置旋转一圈的四个点
        p1 = carla.Location(229, 116, 2)
        p2 = carla.Location(20,194,2)
        p3 = carla.Location(20,198,2)
        p4 = carla.Location(20,199,2)
        p5 = carla.Location(20,200,2)
        p6 = carla.Location(20,201,2)
        p7 = carla.Location(20,202,2)
        p8 = carla.Location(20, 205, 1)
        p9 = carla.Location(240, 116, 1)

        s1 = carla.Transform(p1, carla.Rotation(0,90,0))
        s2 = carla.Transform(p2, carla.Rotation(0,90,0))
        s3 = carla.Transform(p3, carla.Rotation(0,90,0))
        s4 = carla.Transform(p4, carla.Rotation(0,90,0))


        # s5 = carla.Transform(p5, carla.Rotation(0,90,0))
        # s6 = carla.Transform(p6, carla.Rotation(0,90,0))
        # s7 = carla.Transform(p7, carla.Rotation(0,90,0))
        s8 = carla.Transform(p8, carla.Rotation(0,90,0))
        s9 = carla.Transform(p9, carla.Rotation(0,90,0))

        ll = 0

        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)
        
        destination_list = [
            p3, p4, p8, p9
        ]

        # points = [s2, s3, s4, s5, s6, s7, s8, s9]

        world.tick()


        # 设置车辆的驾驶模式
        agent1 = BehaviorAgent(vehicle1, behavior='normal')
        agent1.max_speed = 50
        agent1.set_destination(p2)
        agent1.ignore_traffic_lights(active=True)

    
        while True:
            world.tick()

            if agent1.done():
                if ll == 2:
                    # constraint_points = [
                    #     [world.get_map().get_waypoint(p5,
                    #                         project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    #     [world.get_map().get_waypoint(p6,
                    #                         project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    #     [world.get_map().get_waypoint(p7,
                    #                         project_to_road=False, lane_type=carla.LaneType.Any), RoadOption.LANEFOLLOW],
                    # ]
                    constraint_points = [
                        [p7, RoadOption.LANEFOLLOW],
                    ]

                    agent1.set_global_plan(
                        constraint_points, stop_waypoint_creation=True, clean_queue=True) 
                    print("12312312312312312")
                    print(ll)
                    ll = ll + 1
                else:
                    destination = destination_list[ll]
                    print(ll)
                    ll = ll + 1
                    agent1.set_destination(destination)

            # 设置速度限制
            speed_limit1 = vehicle1.get_speed_limit()
            agent1.get_local_planner().set_speed(speed_limit1)

            control1 = agent1.run_step(debug=True)
            vehicle1.apply_control(control1)
    
    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')






