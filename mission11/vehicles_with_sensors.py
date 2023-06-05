import carla

def main():

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        settings = world.get_settings()
        settings.synchronous_mode = True
        synchronous_master = True

        # traffic_manager
        tm_normal = client.get_trafficmanager(8000)
        tm_normal.set_global_distance_to_leading_vehicle(2.0)
        tm_normal.set_random_device_seed(0)
        tm_normal.set_synchronous_mode(True)

        tm_sensor = client.get_trafficmanager(4000)
        tm_sensor.set_global_distance_to_leading_vehicle(2.0)
        tm_sensor.set_random_device_seed(0)
        tm_sensor.set_synchronous_mode(True)

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

        # spawn lidar
        spawn_point1 = spawn_points[-1]
        sensor_vehicle = world.spawn_actor(vehicle_bp, spawn_point1)
        sensor_vehicle.set_autopilot(True, tm_sensor.get_port())
        sensor_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=-0.2))

        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(300000))
        lidar_bp.set_attribute('rotation_frequency', str(20))
        lidar_bp.set_attribute('range', str(100))

        lidar_location = carla.Location(0,0,1.8)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        lidar1 = world.spawn_actor(lidar_bp, lidar_transform, attach_to=sensor_vehicle)


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
