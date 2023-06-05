import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
import numpy as np
import random
import carla
from agents.navigation.behavior_agent import BehaviorAgent


pub = rospy.Publisher('pointcloud_topic', PointCloud2, queue_size=5)
rospy.init_node('pointcloud_publisher_node', anonymous=True)
# rate = rospy.Rate(1)

# 将carla中的激光lidar转换为ros中的pointcloud2格式发布
def lidar_callback(point_cloud):

    data = np.copy(np.frombuffer(point_cloud.raw_data, dtype=np.dtype('f4')))
    data = np.reshape(data, (int(data.shape[0] / 4), 4))
    print(data.shape)
    points = data[:, :-1]
    print(points.shape)
    msg = PointCloud2()
    msg.header.stamp = rospy.Time().now()
    msg.header.frame_id = "lidar1"

    if len(points.shape) == 3:
        msg.height = points.shape[1]
        msg.width = points.shape[0]
    else:
        msg.height = 1
        msg.width = len(points)

    msg.fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1)]
    msg.is_bigendian = False
    msg.point_step = 12
    msg.row_step = msg.point_step * points.shape[0]
    msg.is_dense = False
    msg.data = np.asarray(points, np.float32).tostring()

    pub.publish(msg)
    print("published...")
            # rate.sleep()


def main():
    actor_list = []
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
        blueprint_library = world.get_blueprint_library()

        p1 = carla.Location(175, -169, 1)
        s1 = carla.Transform(p1, carla.Rotation(0,0,0))
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        # vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)
        # vehicle1.set_autopilot(True)
        # actor_list.append(vehicle1)
        world.tick()
        # agent1 = BehaviorAgent(vehicle1, behavior='normal')

        # spawn_points = world.get_map().get_spawn_points()
        # random.shuffle(spawn_points)

        # if spawn_points[0].location != agent1._vehicle.get_location():
        #     destination = spawn_points[0]
        # else:
        #     destination = spawn_points[1]

        # agent1.set_destination(destination.location)
        # 创建激光lidar
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(300000))
        lidar_bp.set_attribute('rotation_frequency', str(20))
        lidar_bp.set_attribute('range', str(100))
        # 设置激光雷达的点
        lidar_location = carla.Location(195, -165, 2)
        # lidar_location = carla.Location(0, 0, 1.5)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        lidar1 = world.spawn_actor(lidar_bp, lidar_transform)
        actor_list.append(lidar1)
        lidar1.listen(
            lambda data: lidar_callback(data)
        )       

        while True:
            # agent1._update_information()
            world.tick()


    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        print("end...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')