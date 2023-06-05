import carla
import cv2
import logging
import time
import numpy as np
from numpy import random
from queue import Queue
from queue import Empty

def sensor_callback(sensor_data, sensor_queue):
    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
    # image is rgba format
    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))
    array = array[:, :, :3]
    sensor_queue.put((sensor_data.frame, array))

def main():

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        world = client.get_world()

        origin_settings = world.get_settings()

        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
        # 229, 115, 1
        spawn_point = carla.Transform(carla.Location(x=229, y=115, z=1), carla.Rotation(yaw=90))
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)

        # 创建相机并将其附加到车辆上
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=0, z=1))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        sensor_queue = Queue(maxsize=10)  
        camera.listen(lambda image: sensor_callback(image, sensor_queue))
        # 将相机设置为驾驶员视角
        # camera_settings = carla.CameraSettings('Driver View', 1920, 1080, 90)
        # camera.set_camera_settings(camera_settings)

        while True:
            world.tick()
            try:
                s_frame = sensor_queue.get(True, 1.0)
                print("Camera Frame: %d" % (s_frame[0]))

                # show image in a poping window
                cv2.imshow('camera', s_frame[1])
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Empty:
                print("Some of the sensor information is missed")

    finally:
        world.apply_settings(origin_settings)

        # client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_id_list])
        # camera.destroy()
        cv2.destroyAllWindows()

        time.sleep(0.5)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')