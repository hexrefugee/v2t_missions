import carla
 
def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=500,
                                        persistent_lines=True)
 
def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
        p1 = carla.Location(0, 0, 0)
        p2 = carla.Location(400, 0, 0)
        p3 = carla.Location(-500, 0, 0)
        p4 = carla.Location(0, 400, 0)
        p5 = carla.Location(0, -400, 0)
        show_point(world, p1)
        show_point(world, p2)
        show_point(world, p3)
        show_point(world, p4)
        show_point(world, p5)

 
main()