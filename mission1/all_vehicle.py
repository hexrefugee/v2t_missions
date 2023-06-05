import carla


def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()

        blueprint_library = world.get_blueprint_library()

        bp_vehicle = blueprint_library.filter('vehicle*')

        all_vehicle = open('all_vehicle.txt', mode='w')
        for i in bp_vehicle:
            all_vehicle.write(str(i) + '\n')

main()
      