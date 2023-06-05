import carla

def main():

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        synchronous_master = True
        # traffic_manager
        tm_normal = client.get_trafficmanager(8050)
        tm_normal.set_global_distance_to_leading_vehicle(2.0)
        tm_normal.set_random_device_seed(0)
        tm_normal.set_synchronous_mode(True)


        # spawn vehicles
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('model3')[0]
        spawn_points = world.get_map().get_spawn_points()
        for i in range(20):
            spawn_point = spawn_points[i]
            vehicle = world.spawn_actor(vehicle_bp, spawn_point)
            print("spawn_point: ", str(spawn_point))
            vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=-0.2))
            vehicle.set_autopilot(True, tm_normal.get_port())



        # add vehicles to tm
        actor_list = world.get_actors().filter('vehicle*')
        print(len(actor_list))
        # for actor in actor_list:
        #     actor.set_autopilot(True, tm.get_port())

        while True:
            if  synchronous_master:
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

        print('\ndestroying %d vehicles' % len(actor_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list]) 


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
