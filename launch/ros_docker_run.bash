#!/bin/bash

xhost +

SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PKG_PATH="$(dirname $SCRIPT_PATH)"

USER=user
DOCKER_USER_HOME=/home/$USER

docker network create --driver=bridge ign_ros_network || true

set -x  # debug mode
docker run --rm -it  \
    --privileged \
    --network=ign_ros_network \
    --user $USER \
    --name ROS_demo_gazebo_ros_car_minimal \
    -e DISPLAY=$DISPLAY  \
    -e QT_X11_NO_MITSHM=1 \
    -e IGN_PARTITION \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$XAUTH:$XAUTH" \
    -v "/etc/localtime:/etc/localtime:ro" \
    -v "/dev/input:/dev/input" \
    -v /dev:/dev \
    -v $PKG_PATH/docker_volumes/ros_home/entrypoint.bash:$DOCKER_USER_HOME/entrypoint.bash \
    -v $PKG_PATH/docker_volumes/ros_home/.bashrc:$DOCKER_USER_HOME/.bashrc \
    -v $PKG_PATH/docker_volumes/ros_ws:$DOCKER_USER_HOME/ros_ws \
    -v $PKG_PATH:$DOCKER_USER_HOME/ros_ws/src/demo_gazebo_ros_car_minimal \
    --security-opt seccomp=unconfined \
    arahami/ros:humble-desktop-upgraded