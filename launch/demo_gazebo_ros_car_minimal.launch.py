from sys import prefix
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_source import LaunchDescriptionSource
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch.substitutions import EnvironmentVariable
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # package info
    package_name = "demo_gazebo_ros_car_minimal"
    package_path = FindPackageShare(package_name)
    models_path = PathJoinSubstitution([package_path, "models"])
    urdf_model_path = PathJoinSubstitution([models_path, "car/model.urdf"])
    rviz_config_path = PathJoinSubstitution([package_path, "rviz2_config.rviz"])
    ign_gazebo_config_path = PathJoinSubstitution([package_path, "ign_gazebo_gui.config"])
    world_sdf_path = PathJoinSubstitution([models_path, 'world.sdf'])

    # ign gazebo
    ign_gazebo_cmd = ExecuteProcess(
        cmd=[["ign gazebo ", world_sdf_path, " --gui-config ", ign_gazebo_config_path]],
        shell=True,
        output="screen",
    )

    ros_ign_gazebo_package_launch_path = os.path.join(
        get_package_share_directory('ros_ign_gazebo'), 'launch/ign_gazebo.launch.py')
    ros_ign_gazebo_launch_arguments = {"ign_args": [world_sdf_path, " --gui-config ", ign_gazebo_config_path]}.items()
    launch_description_source = PythonLaunchDescriptionSource(ros_ign_gazebo_package_launch_path)
    ros_ign_gazebo_launch_include = IncludeLaunchDescription(launch_description_source,
                                                             launch_arguments=ros_ign_gazebo_launch_arguments)

    # ros ign bridge
    ros_ign_bridge_topics = [
        "/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
        "/camera@sensor_msgs/msg/Image@ignition.msgs.Image",
        "/odometry@nav_msgs/msg/Odometry@ignition.msgs.Odometry",
        "/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo",
        "/joint_states@sensor_msgs/msg/JointState@ignition.msgs.Model",
        "/tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V"
    ]

    ros_ign_gazebo_bridge_cmd = ExecuteProcess(
        cmd=["ros2 run ros_ign_bridge parameter_bridge ", [item+" " for item in ros_ign_bridge_topics]],
        shell=True,
        output="screen",
    )

    ros_ign_bridge_node = Node(package="ros_ign_bridge", executable="parameter_bridge",
                               arguments=ros_ign_bridge_topics, name="ros_ign_bridge")

    # state_publisher

    state_publisher_cmd = ExecuteProcess(
        cmd=["ros2 run robot_state_publisher robot_state_publisher", urdf_model_path],
        shell=True,
        output="screen",
    )

    state_publisher_node = Node(package="robot_state_publisher", executable="robot_state_publisher",
                                arguments=[urdf_model_path])

    # rviz
    rviz_cmd = ExecuteProcess(
        cmd=["ros2 run rviz2 rviz2 -d", rviz_config_path],
        shell=False,
        output="screen"
    )

    rviz_node = Node(package="rviz2", executable="rviz2", arguments=["-d", rviz_config_path])

    # teleop keyboard
    teleop_cmd = ExecuteProcess(
        cmd=["bash -c", "'source /opt/ros/humble/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard'"],
        shell=True,
        output="screen",
        prefix="gnome-terminal --"
    )

    teleop_node = Node(package="teleop_twist_keyboard", executable="teleop_twist_keyboard",
                       emulate_tty=True, prefix="gnome-terminal --")

    return LaunchDescription(
        [
            SetEnvironmentVariable(name="SDF_PATH", value=models_path),
            # # ign_gazebo_cmd,                     # this
            ros_ign_gazebo_launch_include,       # or this

            # # ros_ign_gazebo_bridge_cmd,    # this
            ros_ign_bridge_node,           # or this

            # # state_publisher_cmd,    # this
            state_publisher_node,   # or this

            # # rviz_cmd,       # this
            rviz_node,      # or this

            # teleop_cmd,                     # this
            teleop_node,                    # or this
        ]
    )
