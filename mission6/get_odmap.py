import carla

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

        map_ = world.get_map()
        map_.save_to_disk('/home/v2t-smi/carla-code/HHH/mission6/%s.xodr' %map_.name)

    finally:
        world.apply_settings(origin_settings)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')