import carla
 
def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=50,
                                        persistent_lines=True)
 
def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
 
        # start_point = carla.Location(229, 116, 2)
        end_point = carla.Location(30,5,2)
        # show_point(world, start_point)
        show_point(world, end_point)
        p1 = carla.Location(50, 5.5, 1)
        p2 = carla.Location(80, 6, 1)
        p3 = carla.Location(110, 6.5, 1)
        p4 = carla.Location(140, 7, 1)
        p5 = carla.Location(170, 7.5, 1)
        p = [p1, p2, p3, p4, p5]
        for i in p:
            show_point(world, i)
 
main()
