import carla
 
def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=50,
                                        persistent_lines=True)
 
def main():
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()

        # 寻找原点和x轴，y轴方向
        origin_point = carla.Location(0, 0, 0)
        x_axis = carla.Location(245, 0, 0)
        y_axis = carla.Location(0, -215, 0)
        show_point(world, x_axis)
        show_point(world, y_axis)


        a_start_point = carla.Location(245.4, -8.4, 0)
        b_start_point = carla.Location(242.4, -25, 0)
        ego_start_point = carla.Location(245.4, -19, 0)

        a_end_point = carla.Location(0, -210, 0)

        c_start_point = carla.Location(173, -194, 0)
        d_start_point = carla.Location(168, -197, 0)

        c_end_point = carla.Location(235.4, -8.4, 0)
        d_end_point = carla.Location(233.4, -8.4, 0)

        start_point_lists = [a_start_point, b_start_point, ego_start_point, a_end_point]
        
        end_point_lists = [c_start_point, d_start_point, c_end_point, d_end_point]

        for i in start_point_lists:
                show_point(world, i)
        
        for i in end_point_lists:
                show_point(world, i)

        lidar_location = carla.Location(240, -185, 3)
        show_point(world, lidar_location)


        # 设置激光雷达的两个点
        lidar_p1 = carla.Location(195, -165, 1)
        lidar_p2 = carla.Location(207, -178, 1)

        # show_point(world, lidar_p1)
        # show_point(world, lidar_p2)

        # 设置4辆车的起点和终点
        vehicle1_start_point = carla.Location(175, -169, 0)
        vehicle1_end_point = carla.Location(230, -169, 0)
        # show_point(world, vehicle1_start_point)
        # show_point(world, vehicle1_end_point)

        vehicle2_start_point = carla.Location(225, -173, 0)
        vehicle2_end_point = carla.Location(160, -173, 0)
        # show_point(world, vehicle2_start_point)
        # show_point(world, vehicle2_end_point)

        # # 生成车辆
        # ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        # ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        # vehicle1 = world.spawn_actor(ego_vehicle_bp, start_point1)
        # vehicle2 = world.spawn_actor(ego_vehicle_bp, start_point2)

 
main()