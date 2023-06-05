# 对于交通流、车端、路侧同步效果进行测试

# test1 全部设置为异步模式
交通流 设置 异步 50辆车 单独可以运行，运行几十秒后就乱撞

车端  设置  异步

路侧  设置   异步

结果：交通流使用异步只能运行几十秒

# test2 交通流同步模式
交通流 设置 同步 50辆车 可以运行， 但一卡一卡的

车端  设置 同步  

# test3 使用Carla-lidar-data-generator包里面的代码
初步设置系统： server_setup.py 开的同步模式 tm也是同步模式

交通流：异步 generate_traffic.py 但tm使用的是异步，比较奇怪，需要在研究研究 应该是被覆盖了

车端： carside 使用的是同步模式 

路侧： catkin_ws 使用的是异步模式

结果： 比较流畅的运行了近两分钟

注意：交通流和车端、路侧的settings.fixed_delta_seconds不同
