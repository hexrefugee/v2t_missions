# 制定ID为64的道路，当车辆经过这个道路时，会发送位置信息
# 完成了函数has_pass_road的编写

import carla
from agents.navigation.behavior_agent import BehaviorAgent

# 连接到 Carla 仿真环境
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

blueprint_library = world.get_blueprint_library()

# 获取地图数据
map_data = world.get_map()

# 找到指定道路并获取该道路上的路点
waypoint_list = []
waypoints = map_data.generate_waypoints(2)

road_id = 67

for waypoint in waypoints:

    if waypoint.road_id == road_id:  
        waypoint_list.append(waypoint)

print("id为67的waypoint数量:")
print(len(waypoint_list))

for waypoint in waypoint_list:
    world.debug.draw_string(waypoint.transform.location, 'O',
                                draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=100.0,
                                persistent_lines=True)

# current_waypoint = None

# 创建一个函数以检查车辆是否通过了指定的道路
def has_passed_road(vehicle, road_id):
    current_waypoint = None

    # 如果当前路点为 None，则获取车辆当前所在的路点
    if current_waypoint is None:
        current_location = vehicle.get_location()
        current_waypoint = map_data.get_waypoint(current_location)

    if current_waypoint.road_id != road_id:
        print("vechile current_waypoint: {}".format(current_waypoint))
        return False
    else:
        print("vehicle current_waypoint: {}".format(current_waypoint))
        return True


    # 如果当前路点不在指定道路上，则更新当前路点为指定道路上的第一个路点
    # if current_waypoint.road_id != road_id:
    #     for waypoint in waypoints:
    #         if waypoint.road_id == road_id:
    #             current_waypoint = waypoint
    #             break
    

    # 检查车辆是否在当前路点可行驶区域内，如果在，则继续检查下一个路点；否则说明车辆已经离开当前道路
    # if current_waypoint.is_junction:
    #     current_location = vehicle.get_location()
    #     current_waypoint = map_data.get_waypoint(current_location)
    #     print("current_waypoint: {}".format(current_waypoint))
    #     return False
    # else:
    #     location = vehicle.get_location()
    #     distance = current_waypoint.transform.location.distance(location)
    #     if distance <= 2.0:
    #         current_waypoint = current_waypoint.next(2.0)[0]
    #     print("current_waypoint: {}".format(current_waypoint))
    #     return True

p1 = carla.Location(229, 115, 1)
s1 = carla.Transform(p1, carla.Rotation(0,90,0))
p6 = carla.Location(173, -194, 1)
end_point = carla.Transform(p6, carla.Rotation(0, 0, 0))

ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
ego_vehicle_bp.set_attribute('color', '0, 0, 0')
vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)

world.tick()

agent1 = BehaviorAgent(vehicle1, behavior='normal')

agent1.set_destination(end_point.location)
print(len(agent1._local_planner._waypoints_queue))

while True:
    agent1._update_information()

    world.tick()

    if has_passed_road(vehicle1, road_id):
        print("Vehicle is still on road {}".format(road_id))
    else:
        print("Vehicle has left road {}".format(road_id))
    
    if (len(agent1._local_planner._waypoints_queue) < 1):
        print('======== Success, Arrivied at Target Point!')
        break
        
    # 设置速度限制
    # speed_limit1 = vehicle1.get_speed_limit()
    # agent1.get_local_planner().set_speed(speed_limit1)

    control1 = agent1.run_step(debug=True)
    
    control1.throttle=0.7
    vehicle1.apply_control(control1)
    

vehicle1.destroy()
