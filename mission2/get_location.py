import carla
import sys
import os

from agents.navigation.behavior_agent import BehaviorAgent

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.1
        world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()

        # output_path = 'location_file'
        location_file = open('vehicle_location.txt', 'w')

        p1 = carla.Location(229, 115, 1)
        p2 = carla.Location(0, 194, 1)

        start_point = carla.Transform(p1, carla.Rotation(0, 90, 0))
        end_point = carla.Transform(p2, carla.Rotation(0, 90, 0))

        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, start_point)

        world.tick()

        agent = BehaviorAgent(vehicle1, behavior='normal')

        agent.set_destination(end_point.location)

        while True:
            agent._update_information()

            world.tick()

            if len(agent._local_planner._waypoints_queue) < 1:
                print('======== Success, Arrivied at Target Point!')
                break
            location = vehicle1.get_location()
            waypoint = world.get_map().get_waypoint(location)
            location_file.write(str(waypoint) + '\n')

            speed_limit1 = vehicle1.get_speed_limit()
            agent.get_local_planner().set_speed(speed_limit1)

            control = agent.run_step(debug=True)
            control.throttle=0.5
            vehicle1.apply_control(control)

    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exitd by user!')
