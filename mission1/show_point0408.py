import carla
 
def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=50,
                                        persistent_lines=True)
 
def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()

        # show_point(world, end_point)
        # p1 = carla.Location(0, 0, 2)
        p2  = carla.Location(30, 7, 2)
        p3  = carla.Location(100, 7, 2)
        p4  = carla.Location(200, 7, 2)
        p5  = carla.Location(220, 7, 2)
        p6  = carla.Location(228, 15, 2)
        p7  = carla.Location(235, 25, 2)
        p8  = carla.Location(234, 38, 2)
        p9  = carla.Location(234, 50, 2)
        p10 = carla.Location(234, 60, 2)
        p11 = carla.Location(234, 70, 2)
        p12 = carla.Location(233, 80, 2)
        p13 = carla.Location(233, 90, 2)
        p14 = carla.Location(10, 194, 1)
        p15 = carla.Location(6, 160, 1)
        p16 = carla.Location(6, 140, 1)
        p17 = carla.Location(6, 130, 1)
        p18 = carla.Location(6, 60, 1)
        p19 = carla.Location(6, 30, 1)

        p = [p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19]
        for i in p:
            show_point(world, i)
 
main()