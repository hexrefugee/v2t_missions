import carla
 
def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=50,
                                        persistent_lines=True)
 
def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
        # test_point = carla.Location(-11,-72,2)
        start_point = carla.Location(229, 116, 2)
        origin_point = carla.Location(0, 0, 0)
        show_point(world, origin_point)
        end_point = carla.Location(20,194,2)
        # show_point(world, start_point)
        # show_point(world, test_point)
        show_point(world, end_point)
        p1 = carla.Location(229, 116, 2)
        p2 = carla.Location(20,194,2)
        p3 = carla.Location(20,198,2)
        p4 = carla.Location(20,199,2)
        p5 = carla.Location(20,200,2)
        p6 = carla.Location(20,201,2)
        p7 = carla.Location(20,202,2)
        p8 = carla.Location(20, 205, 1)
        p9 = carla.Location(240, 116, 1)

        # p = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
        p = [p1, p2, p3, p8, p9]
        # p = [p1, p2, p3, p4]
        # for i in p:
        #     show_point(world, i)

        # show_point(world, carla.Location(152, 193, 2))
 
main()