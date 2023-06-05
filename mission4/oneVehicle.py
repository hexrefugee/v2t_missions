import carla
from cv2 import cv2 as cv
from carla_birdeye_view import BirdViewProducer, BirdViewCropType, PixelDimensions
from agents.navigation.behavior_agent import BehaviorAgent

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
 
        world = client.get_world()
 
        origin_settings = world.get_settings()
 
        birdview_producer = BirdViewProducer(
            client,  # carla.Client
            target_size=PixelDimensions(width=150, height=336),
            pixels_per_meter=4,
            crop_type=BirdViewCropType.FRONT_AND_REAR_AREA,
            render_lanes_on_junctions=False,
        )
        
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
 
        blueprint_library = world.get_blueprint_library()
 
        # 确定起点和终点
        p1 = carla.Location(229, 115, 1)
        p2 = carla.Location(229, 110, 1)
        p3 = carla.Location(229, 105, 1)
        p4 = carla.Location(229, 100, 1)
        p5 = carla.Location(229, 95, 1)
        p6 = carla.Location(0, 194, 1)
        
        s1 = carla.Transform(p1, carla.Rotation(0,90,0))
        s2 = carla.Transform(p2, carla.Rotation(0,90,0))
        s3 = carla.Transform(p3, carla.Rotation(0,90,0))
        s4 = carla.Transform(p4, carla.Rotation(0,90,0))
        s5 = carla.Transform(p5, carla.Rotation(0,90,0))
        end_point = carla.Transform(p6, carla.Rotation(0, 0, 0))


        # 创建车辆
        ego_vehicle_bp = blueprint_library.find('vehicle.audi.a2')
        ego_vehicle_bp.set_attribute('color', '0, 0, 0')
        vehicle1 = world.spawn_actor(ego_vehicle_bp, s1)
        vehicle2 = world.spawn_actor(ego_vehicle_bp, s2)
        vehicle3 = world.spawn_actor(ego_vehicle_bp, s3)
        vehicle4 = world.spawn_actor(ego_vehicle_bp, s4)
        vehicle5 = world.spawn_actor(ego_vehicle_bp, s5)
 
        world.tick()
 
        # 设置车辆的驾驶模式
        agent1 = BehaviorAgent(vehicle1, behavior='normal')
        agent2 = BehaviorAgent(vehicle2, behavior='normal')
        agent3 = BehaviorAgent(vehicle3, behavior='normal')
        agent4 = BehaviorAgent(vehicle4, behavior='normal')
        agent5 = BehaviorAgent(vehicle5, behavior='normal')
        # 核心函数
        agent1.set_destination(end_point.location)
        agent2.set_destination(end_point.location)
        agent3.set_destination(end_point.location)
        agent4.set_destination(end_point.location)
        agent5.set_destination(end_point.location)
 

        while True:
            agent1._update_information()
            agent2._update_information()
            agent3._update_information()
            agent4._update_information()
            agent5._update_information()
 
            # birdview = birdview_producer.produce(
            #     agent_vehicle=agent1  # carla.Actor (spawned vehicle)
            # )
            # rgb = BirdViewProducer.as_rgb(birdview)
            # cv.imshow("BirdView RGB", rgb)

            birdview: BirdView = birdview_producer.produce(agent_vehicle=agent1)
            bgr = cv.cvtColor(BirdViewProducer.as_rgb(birdview), cv.COLOR_BGR2RGB)
            # NOTE imshow requires BGR color model
            cv.imshow("BirdView RGB", bgr)
            world.tick()
            
            if (len(agent4._local_planner._waypoints_queue) < 1):
                vehicle5.destroy()
                print('======== Success, Arrivied at Target Point!')
                break
                
            # 设置速度限制
            # speed_limit1 = vehicle1.get_speed_limit()
            # agent1.get_local_planner().set_speed(speed_limit1)
 
            # control1 = agent1.run_step(debug=True)
            # vehicle1.apply_control(control1)

            # speed_limit2 = vehicle2.get_speed_limit()
            # agent2.get_local_planner().set_speed(speed_limit2)
 
            # control2 = agent2.run_step(debug=True)
            # vehicle2.apply_control(control2)

            # speed_limit3 = vehicle3.get_speed_limit()
            # agent3.get_local_planner().set_speed(speed_limit3)
 
            # control3 = agent3.run_step(debug=True)
            # vehicle3.apply_control(control3)

            # speed_limit4 = vehicle4.get_speed_limit()
            # agent4.get_local_planner().set_speed(speed_limit4)
 
            # control4 = agent4.run_step(debug=True)
            # vehicle4.apply_control(control4)

            # speed_limit5 = vehicle5.get_speed_limit()
            # agent5.get_local_planner().set_speed(speed_limit5)
 
            # control5 = agent5.run_step(debug=True)
            # vehicle5.apply_control(control5)
 
    finally:
        world.apply_settings(origin_settings)
        vehicle1.destroy()
        vehicle2.destroy()
        vehicle3.destroy()
        vehicle4.destroy()
        vehicle5.destroy()
        cv.destroyAllWindows()
 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')