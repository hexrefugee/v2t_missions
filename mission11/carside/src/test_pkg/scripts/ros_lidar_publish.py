import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField

import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import random
import carla
from agents.navigation.behavior_agent import BehaviorAgent

import time

import sys                                                                  
import signal
 
def quit(signum, frame):
    print('')
    print('stop')
    sys.exit()



pub_lidar = rospy.Publisher('pointcloud_topic', PointCloud2, queue_size=5)
rospy.init_node('pointcloud_publisher_node', anonymous=True)
# rate = rospy.Rate(1)

pub_img = rospy.Publisher('/camera2/rgb/image_raw', Image, queue_size = 10)
pub_img_segment = rospy.Publisher('/camera2/rgb/seg_raw', Image, queue_size = 10)

# 将carla中的激光lidar转换为ros中的pointcloud2格式发布
def lidar_callback(point_cloud):

    data = np.copy(np.frombuffer(point_cloud.raw_data, dtype=np.dtype('f4')))
    data = np.reshape(data, (int(data.shape[0] / 4), 4))
    print(data.shape)
    points = data[:, :-1]
    points[:,0] = -points[:, 0]
    print(points.shape)
    msg = PointCloud2()
    msg.header.stamp = rospy.Time().now()
    msg.header.frame_id = "car_lidar"

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


    pub_lidar.publish(msg)
    # print("published...")
    # rate.sleep()

def camera_at1_callback(img_msg):
    # img_msg.save_to_disk('_out/%08d' % img_msg.frame)
    im_array = np.copy(np.frombuffer(img_msg.raw_data, dtype=np.dtype("uint8")))
    im_array = np.reshape(im_array, (img_msg.height, img_msg.width, 4))
    im_array = im_array[:, :, :3][:, :, ::-1]

    # cv_bridge.core.CvBridgeError: encoding specified as bgr8, but image has incompatible type 8UC4

    # rate = rospy.Rate(10)
    bridge = CvBridge()

    # while not rospy.is_shutdown():
    # image = cv2.resize(image,(1920,1200))
    pub_img.publish(bridge.cv2_to_imgmsg(im_array,"8UC3"))      #   bgr8
    # cv2.imshow("lala",im_array)
    # cv2.waitKey(1)
    # rate.sleep()

def camera_semantic_callback(sensor_data):
    sensor_data.convert(carla.ColorConverter.CityScapesPalette)
    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
    # image is rgba format
    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))
    array = array[:, :, :3][:, :, ::-1]
    bridge = CvBridge()
    pub_img_segment.publish(bridge.cv2_to_imgmsg(array,"8UC3"))      #   bgr8


    


def main():
    actor_list = []
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        original_settings = world.get_settings()

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()
        camera_bp = blueprint_library.filter("sensor.camera.rgb")[0]
        # Configure the blueprints
        camera_bp.set_attribute("image_size_x", str(1280))
        camera_bp.set_attribute("image_size_y", str(720))

        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        # p1 = carla.Location(100,190,5)
        # s1 = carla.Transform(p1, carla.Rotation(0,0,0))

        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')

        vehicle1 = world.spawn_actor(ego_vehicle_bp, spawn_points[0])
        # vehicle1.set_autopilot(True)
        actor_list.append(vehicle1)
        world.tick()

       
        camera_at1 = world.spawn_actor(camera_bp,carla.Transform(carla.Location(1,0,2)), attach_to=vehicle1)
        actor_list.append(camera_at1)
        camera_at1.listen(lambda data: camera_at1_callback(data))

        # 创建 Semantic segmentation 
        camera_transform = carla.Transform(carla.Location(1,0,2))
        camera_Seg = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        camera_seg = world.spawn_actor(camera_Seg, camera_transform, attach_to=vehicle1)
        camera_seg.listen(lambda image: camera_semantic_callback(image))

        agent1 = BehaviorAgent(vehicle1, behavior='normal')

        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        if spawn_points[0].location != agent1._vehicle.get_location():
            destination = spawn_points[0]
        else:
            destination = spawn_points[1]

        agent1.set_destination(destination.location)
        # 创建激光lidar
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(300000))
        lidar_bp.set_attribute('rotation_frequency', str(20))
        lidar_bp.set_attribute('range', str(100))
        # 设置激光雷达的点
        lidar_location = carla.Location(0,0,1.8)
        # lidar_location = carla.Location(0, 0, 1.5)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        lidar1 = world.spawn_actor(lidar_bp, lidar_transform, attach_to=vehicle1)
        actor_list.append(lidar1)
        lidar1.listen(
            lambda data: lidar_callback(data)
        )       
        signal.signal(signal.SIGINT, quit)                                
        signal.signal(signal.SIGTERM, quit)

        
        while True:
            try:
                agent1._update_information()
                world.tick()
                if (len(agent1._local_planner._waypoints_queue) < 1):
                    random.shuffle(spawn_points)
                    if spawn_points[0].location != agent1._vehicle.get_location():
                        destination = spawn_points[0]
                    else:
                        destination = spawn_points[1]
                    agent1.set_destination(destination.location)

                # top view
                spectator = world.get_spectator()
                transform = vehicle1.get_transform()
                spectator.set_transform(carla.Transform(transform.location + carla.Location(z=40),
                                                    carla.Rotation(pitch=-70)))
                control = agent1.run_step()
                vehicle1.apply_control(control)
            except:
                print("end...")
                break


    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        for x in actor_list:
            x.destroy()
        # time.sleep(1)
        print("DestroyActor end")
        if original_settings:
            world.apply_settings(original_settings)
        print(' - Exited by user.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')