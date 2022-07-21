#! /bin/bash

source $HOME/.bashrc

# build project
CURRENT_DIR=$(pwd)
cd $HOME/ros_ws
colcon build
source ./install/setup.bash
cd $CURRENT_DIR
ros2 launch demo_gazebo_ros_car_minimal demo_minimal_only_ros.launch.py