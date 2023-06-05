# 路侧部分的展示demo
# 设计使用o3d来展示激光lidar，使用cv2来展示视觉

# carlaViz使用指南

# 1. launch carla simulator
cd CARLA_SIMULATOR_PATH
./CarlaUE4.sh

# 2. pull and launch the docker image
#    if you run this command in a remote machine, replace CARLAVIZ_BACKEND_HOST 
#    with the ip address of the machine where you run this command, 
#    otherwise, keep it as localhost
docker pull mjxu96/carlaviz:0.9.13 # based on your carla version


# 使用下面这个命令
# if you are using docker on Linux and Carla server is running on localhost:2000
docker run -it --network="host" -e CARLAVIZ_BACKEND_HOST=localhost -e CARLA_SERVER_HOST=localhost -e CARLA_SERVER_PORT=2000 mjxu96/carlaviz:0.9.13 # based on your carla version

# if you are using docker on Windows/MacOS and Carla server is running on localhost:2000
# NOTE: you can only run CarlaViz with version 0.9.12 or later on Windows
docker run -it -e CARLAVIZ_BACKEND_HOST=localhost -e CARLA_SERVER_HOST=host.docker.internal -e CARLA_SERVER_PORT=2000 -p 8080-8081:8080-8081 -p 8089:8089 mjxu96/carlaviz:0.9.13 # based on your carla version

# 3. run this script
python3 example.py

# 4. open your browser and go to localhost:8080 or CARLAVIZ_BACKEND_HOST:8080

