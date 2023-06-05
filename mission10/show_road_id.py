# 可视化的显示所有道路的id信息
# 道路id是67

import carla

# Connect to the Carla simulation environment
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# Get map data and all waypoints
map_data = world.get_map()
waypoints = map_data.generate_waypoints(5.0)

# Get the topology of the map
topology = map_data.get_topology()

# Create a list to store all road IDs
road_ids = []

# Extract the road IDs from the topology and add them to the list
for segment in topology:
    road_id = segment[0].road_id
    if road_id not in road_ids:
        road_ids.append(road_id)

# Print out all road IDs
print("All road IDs:")
for road_id in road_ids:
    print(road_id)

# Visualize all road IDs in the simulation environment
for waypoint in waypoints:
    if waypoint.road_id in road_ids:
        world.debug.draw_string(waypoint.transform.location, str(waypoint.road_id),
                                draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=100.0,
                                persistent_lines=True)
