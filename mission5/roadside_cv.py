import argparse
import carla
import cv2
import logging
import time
import numpy as np
from numpy import random
from queue import Queue
from queue import Empty
import os

# try... except的主要作用是获取的carla的egg包，然后指向这个包，多机相连接的时候要确定正确的egg包的位置
# 
# try:
#     sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
#         sys.version_info.major,
#         sys.version_info.minor,
#         'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
# except IndexError:
#     pass

# output_path = '../output_basic_api'

def sensor_callback(sensor_data, sensor_queue):
    sensor_data.convert(carla.ColorConverter.CityScapesPalette)
    # sensor_data.save_to_disk(os.path.join(output_path, '%06d.png' % sensor_data.frame))
    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
    # image is rgba format
    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))
    array = array[:, :, :3]
    sensor_queue.put((sensor_data.frame, array))

def main():
    try:
        # 修改这个localhost部分，改称连接主机的IP
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()
 
 
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
 
        blueprint_library = world.get_blueprint_library()

        # 创建sensor queue
        # sensor_queue1 = Queue(maxsize=10)
        sensor_queue2 = Queue(maxsize=10)
        # sensor_queue3 = Queue(maxsize=10)
        # sensor_queue4 = Queue(maxsize=10)

        # 创建 RGB_camera
        # camera_RGB = world.get_blueprint_library().find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(100,190,10))
        # camera_rgb = world.spawn_actor(camera_RGB, camera_transform)
        # 设置回调函数
        # camera_rgb.listen(lambda image: sensor_callback(image, sensor_queue1))

        # 创建 Semantic segmentation
        camera_Seg = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        camera_seg = world.spawn_actor(camera_Seg, camera_transform)
        camera_seg.listen(lambda image: sensor_callback(image, sensor_queue2))

        # 创建 Instance segmentation camera
        # camera_Ins = world.get_blueprint_library().find('sensor.camera.instance_segmentation')
        # camera_ins = world.spawn_actor(camera_Ins, camera_transform)
        # camera_ins.listen(lambda image: sensor_callback(image, sensor_queue3))

        # 创建 Depth camera
        # camera_Dep = world.get_blueprint_library().find('sensor.camera.depth')
        # camera_dep = world.spawn_actor(camera_Dep, camera_transform)
        # camera_dep.listen(lambda image: sensor_callback(image, sensor_queue3))

        while True:
            world.tick()
            # s_frame1 = sensor_queue1.get(True, 1.0)
            s_frame2 = sensor_queue2.get(True, 1.0)
            # s_frame3 = sensor_queue3.get(True, 1.0)
            # s_frame4 = sensor_queue4.get(True, 1.0)
            # cv2.imshow('camera_rgb', s_frame1[1])
            cv2.imshow('camera_seg', s_frame2[1])

            # cv2.imshow('camera_ins', s_frame3[1])
            # cv2.imshow('camera_dep', s_frame4[1])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



    finally:
        world.apply_settings(origin_settings)
        # camera_rgb.destroy()
        camera_seg.destroy()
        cv2.destroyAllWindows()
        time.sleep(0.5)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')