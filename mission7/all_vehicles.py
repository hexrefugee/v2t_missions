import carla
import random

# 连接CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# 获取世界对象和蓝图工厂对象
world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 获取所有车辆蓝图
vehicle_blueprints = blueprint_library.filter('vehicle.*')

# 获取指定的路段
map = world.get_map()
waypoint_list = map.generate_waypoints(distance=10.0)  # 生成离当前Actor最近的路点列表
waypoint = random.choice(waypoint_list)  # 随机选择一个路点作为起始点

# 生成10辆车
for i in range(10):
    # 随机选择车辆蓝图
    blueprint = random.choice(vehicle_blueprints)

    # 设置生成车辆的属性
    blueprint.set_attribute('role_name', 'autopilot')
    blueprint.set_attribute('color', '255,0,0')

    # 获取路点方向并设置车辆朝向
    transform = waypoint.transform
    transform.rotation.yaw += 180.0

    # 在路点位置生成车辆
    vehicle = world.spawn_actor(blueprint, transform)
    
    # 沿着路段移动车辆
    for j in range(10):
        # 获取下一个路点
        waypoint = random.choice(waypoint.next(2.0))

        # # 设置车辆速度
        # vehicle.set_target_velocity(carla.Vector3D(x=30.0, y=0.0, z=0.0))

        # # 设置车辆目标路点
        # vehicle.set_autopilot(True, waypoint)