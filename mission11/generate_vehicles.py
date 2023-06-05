#!/usr/bin/env python
# 目标：把生成10车辆并设置成自动驾驶


import carla
from numpy import random
import logging


def main():

    vehicles_list = []
    all_id = []
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    synchronous_master = False

    vehicles_nums = 10

    try:
        world = client.get_world()

        traffic_manager = client.get_trafficmanager(8000)
        traffic_manager.set_global_distance_to_leading_vehicle(2.5)
        
        settings = world.get_settings()
        
        traffic_manager.set_synchronous_mode(True)

        if not settings.synchronous_mode:
            synchronous_master = True
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
        else:
            synchronous_master = False
        
        blueprints = world.get_blueprint_library().filter('vehicle.*')

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)


        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor

        # --------------
        # Spawn vehicles
        # --------------
        batch = []

        for n, transform in enumerate(spawn_points):
            if n >= vehicles_nums:
                break
            blueprint = random.choice(blueprints)
            if blueprint.has_attribute('color'):
                color = random.choice(blueprint.get_attribute('color').recommended_values)
                blueprint.set_attribute('color', color)
            if blueprint.has_attribute('driver_id'):
                driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                blueprint.set_attribute('driver_id', driver_id)

            # spawn the cars and set their autopilot and light state all together
            batch.append(SpawnActor(blueprint, transform)
                .then(SetAutopilot(FutureActor, True, traffic_manager.get_port())))


        for response in client.apply_batch_sync(batch, synchronous_master):
            if response.error:
                logging.error(response.error)
            else:
                vehicles_list.append(response.actor_id)
        print('spawned %d vehicles, press Ctrl+C to exit.' % (len(vehicles_list)))

        traffic_manager.global_percentage_speed_difference(30.0)   

        while True:
            if synchronous_master:
                world.tick()
            else:
                world.wait_for_tick()     

    finally:
        if not synchronous_master:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.no_rendering_mode = False
            settings.fixed_delta_seconds = None
            world.apply_settings(settings)

        print('\ndestroying %d vehicles' % len(vehicles_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')





