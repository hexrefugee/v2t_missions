"""
实现车辆不断循环运行
"""

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
        p1 = carla.Location(30, 7, 2)
        s1 = carla.Transform(p1, carla.Rotation(0,0,0))
        end_point = [
            carla.Location(30, 7, 2),
            carla.Location(100, 7, 2),
            carla.Location(200, 7, 2),
            carla.Location(220, 7, 2),
            carla.Location(228, 15, 2),
            carla.Location(235, 25, 2),
            carla.Location(234, 38, 2),
            carla.Location(234, 50, 2),
            carla.Location(234, 60, 2),
            carla.Location(234, 70, 2),
            carla.Location(233, 80, 2),
            carla.Location(233, 90, 2),
            carla.Location(10, 194, 1),
            carla.Location(6, 160, 1),
            carla.Location(6, 140, 1),
            carla.Location(6, 130, 1),
            carla.Location(6, 60, 1),
            carla.Location(6, 30, 1),
        ]

        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)

        world.tick()

        agent1 = BehaviorAgent(vehicle1, behavior='normal')

        agent1.set_destination(end_point[1])
        k = 1
        while True:
            agent1._update_information()
 
            world.tick()
            
            if (len(agent1._local_planner._waypoints_queue) < 1):
                print('======== Success, Arrivied at %d Point!', k)
                k = k + 1
                if k == 17:
                    k = 0
                print('======== Find a new %d Point!', k)
                agent1.set_destination(end_point[k])

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



        



