import carla

def show_point(world, point_location):
    world.debug.draw_string(point_location, 'X', draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=50,
                                        persistent_lines=True)

# 连接CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# 获取世界对象和蓝图工厂对象
world = client.get_world()
blueprint_library = world.get_blueprint_library()


map = world.get_map()

crosswalks = map.get_crosswalks()

for i in crosswalks:
    show_point(world, i)