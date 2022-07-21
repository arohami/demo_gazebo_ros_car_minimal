SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source /opt/ros/humble/setup.bash
source $SCRIPT_PATH/../install/setup.bash    # source ws assuming pkg directory is: ws/src/pkg
export SDF_PATH=$SDF_PATH:$SCRIPT_PATH/models
export PKG_PATH=$SCRIPT_PATH
pid_list=()

run_ign_gazebo(){
    ign gazebo $PKG_PATH/models/world.sdf --gui-config $PKG_PATH/configs/ign_gazebo_gui.config
}
export -f run_ign_gazebo

run_ros_ign_gazebo(){
    ros2 launch ros_ign_gazebo ign_gazebo.launch.py ign_args:="$PKG_PATH/models/world.sdf --gui-config $PKG_PATH/configs/ign_gazebo_gui.config"
}
export -f run_ros_ign_gazebo

run_ros_ign_bridge(){
    ros2 run ros_ign_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist /camera@sensor_msgs/msg/Image@ignition.msgs.Image /odometry@nav_msgs/msg/Odometry@ignition.msgs.Odometry /camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo /joint_states@sensor_msgs/msg/JointState@ignition.msgs.Model /tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V
}
export -f run_ros_ign_bridge

run_robot_state_publisher(){
    ros2 run robot_state_publisher robot_state_publisher models/car/model.urdf
}
export -f run_robot_state_publisher

run_rviz(){
    ros2 run rviz2 rviz2 -d $PKG_PATH/configs/rviz2_config.rviz --ros-args --log-level fatal
}
export -f run_rviz

run_teleop_keyboard(){
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
}
export -f run_teleop_keyboard

kill_all(){
    list_descendants ()
    {
        local children=$(ps -o pid= --ppid "$1")

        for pid in $children
        do
            list_descendants "$pid"
        done

        echo "$children"
    }

    kill $(list_descendants $$)
}
export -f kill_all

run_all(){
    run_ign_gazebo &
    pid_list+=($!)

    run_ros_ign_bridge &
    pid_list+=($!)

    run_robot_state_publisher &
    pid_list+=($!)

    sleep 3
    run_rviz &
    pid_list+=($!)

    run_teleop_keyboard
    
    kill_all
}
export -f run_all

docker_run(){
    docker-compose -f $PKG_PATH/launch/docker-compose.yaml up
    docker-compose -f $PKG_PATH/launch/docker-compose.yaml down
}
export -f docker_run