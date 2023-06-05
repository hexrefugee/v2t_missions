import carla



# 连接CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# 获取世界对象和蓝图工厂对象
world = client.get_world()
blueprint_library = world.get_blueprint_library()

point_a = carla.Location(0,0,5)
point_b = carla.Location(10,10,5)



world.debug.draw_arrow(point_a, point_b, life_time=50)

