#!/bin/bash

xhost +

SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PKG_PATH="$(dirname $SCRIPT_PATH)"

USER=user
DOCKER_USER_HOME=/home/$USER

docker run --rm -it  \
    --privileged \
    --network=my-bridge-network \
    --user $USER \
    --name IGN_demo_gazebo_ros_car_minimal \
    -e DISPLAY=$DISPLAY  \
    -e QT_X11_NO_MITSHM=1 \
    -e IGN_PARTITION \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$XAUTH:$XAUTH" \
    -v "/etc/localtime:/etc/localtime:ro" \
    -v "/dev/input:/dev/input" \
    -v /dev:/dev \
    -v $PKG_PATH/docker_volumes/ign_gazebo_home/entrypoint.bash:$DOCKER_USER_HOME/entrypoint.bash \
    -v $PKG_PATH/docker_volumes/ign_gazebo_home/.bashrc:$DOCKER_USER_HOME/.bashrc \
    -v $PKG_PATH/docker_volumes/ros_ws:$DOCKER_USER_HOME/ros_ws \
    -v $PKG_PATH:$DOCKER_USER_HOME/ros_ws/src/demo_gazebo_ros_car_minimal \
    --security-opt seccomp=unconfined \
    arahami/ign_gazebo:fortress