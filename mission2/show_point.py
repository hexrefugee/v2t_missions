import carla
import numpy as np

def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=500,
                                        persistent_lines=True)
 
handled_data = np.loadtxt('handled_data.txt')
right_landmark = np.loadtxt('right_landmark.txt')
left_landmark = np.loadtxt('left_landmark.txt')

def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
 

        location = handled_data[:, [0, 1]]
        for i in range(len(location[:,0])):
                center_point = carla.Location(location[i, 0], location[i, 1], 0)
                right_point = carla.Location(right_landmark[i, 0], right_landmark[i, 1], 0)
                left_point = carla.Location(left_landmark[i, 0], left_landmark[i, 1], 0)
                show_point(world, center_point)
                # show_point(world, right_point)
                show_point(world, left_point)

 
main()