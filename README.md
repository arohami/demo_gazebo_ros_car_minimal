# demo_gazebo_ros_car_minimal

## Compatibility
this example is written and tested for:
* ros2 humble
* ign gazebo v6.9.0


an example of driving a simple 4 wheel car in ign gazebo with rviz visualization

this example includes seperated models for different parts of the robot. each model has a folder which includes main model description in xacro, auto generated urdf(rviz model) from xacro, modified the auto generated sdf(gazebo model) from urdf and a test_world which includes the sdf model

## Explaination
---

the parent folder(named "car") which includes xacro file and it's auto generated urdf and sdf(manualy modified). there is also the world descriptor file (sdf) rviz2 config file and ign gazebo config file in the root directory of the project.

the xacro model in the car folder includes models(xacro files) of other parts, connects them together (joint description) and imports/implements plugins.

### XACRO
xacro file is the main file which other model descriptors are generated from. <gazebo> tag indicates the parts that are just meant for gazebo (sdf) and are ignored in rviz (urdf)

**note:** xacro file of car_wheel and car_ball_wheel doesn't describe the model itself, instead it describes a macro which generates the model (set's model name so there can be multiple instances of the model in the world). this is why urdf/sdf generated files are named sample_models. 

### URDF
urdf files are directly generated from xacro without any further changes.

xacro to urdf conversion command:

```bash
ros2 xacro xacro model.xacro > model.urdf
```

to test urdf files seperately: 

``` bash
ros2 launch urdf_tutorial display.launch.py
```

**note:** we can also write model description in sdf format and then convert it to urdf using pysdf: `ros2 run pysdf sdf2urdf model.sdf model.urdf`. but again, some tags like "joint" that are different in urdf and sdf should be modified manually after the conversion.

**[my forked pysdf repo](https://github.com/arahami/pysdf)**

### SDF
sdf files for each part are initially created from urdf. but since some parts of the files doesn't convert properly to sdf, further modification are needed:
* \<material> tags in urdf (inside \<gazebo> tag) are the color specifications of the model for sdf. but they don't convert properly from urdf to sdf. so material elements are directly inserted in sdf model after conversion.
* since urdf \<joint>s are different from the ones from sdf, "revolute" joints are used in urdf for the simplest representation of "ball" joints in the sdf. since this example is supposed to be as simple as possible, rear wheels of the car are considered to be spherical with ball joints.

urdf to sdf conversion command:

```bash
gz sdf -p model.urdf > model.sdf
```

to test sdf files seperately: 
```bash
ign gazebo test_world.sdf
```

**note:** to use test_world.sdf in car_wheel and car_ball_wheel you need to **change model.config**:

uncomment this line: `<sdf version="1.7">sample_model.sdf</sdf>`
comment this line: `<sdf version="1.7">model.sdf</sdf>`

**note:** common sdf models (sun & ground plane) are placed in root directory of the project and are used by world/test_world sfd files.

## How to use
----
there are two methods to run this simulation. 
1. launch each part seperately: 
    - ign gazebo
    - rviz
    - ign gazebo <--bridge--> ros2
    - keyboard driver (teleop keyboard)

2. launch using ros2 launcher

### modular launch

#### gazebo

open terminal in root project directory, source ros and enter:
``` bash
 export SDF_PATH=$SDF_PATH:$(pwd)
```
**note**: since files of different parts are relatively included in the main model file, it's important to set this environment variable correctly (so for example $SDF_PATH/car/car_body should exist)

after setting environment variable, you can launch world.sdf in ign gazebo directly: 
``` bash
 ign gazebo car/world.sdf --gui-config ign_gazebo_gui.config
 ```
 
or you can launch ign gazebo using ros command:
``` bash
ros2 launch ros_ign_gazebo ign_gazebo.launch.py ign_args:="car/world.sdf --gui-config ign_gazebo_gui.config"
```

don't forget to play simulation (play button at the left bottom of the ign gazebo screen)


### ROS BRIDGE
to convert ign gazebo topics to ros2 topics, we use ros_ign_gazebo_bridge package from ros2:

```bash
ros2 run ros_ign_bridge parameter_bridge /model/two_wheel_drive_car/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist /camera@sensor_msgs/msg/Image@ignition.msgs.Image /model/two_wheel_drive_car/odometry@nav_msgs/msg/Odometry@ignition.msgs.Odometry /camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo /world/default/model/two_wheel_drive_car/joint_state@sensor_msgs/msg/JointState@ignition.msgs.Model /model/two_wheel_drive_car/tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V 
```

### ROS Visualization
to visualize data of the robot we use rviz assuming position of the robot is always known. but other parts position should be calculated (tf)
position of the robot is published in ros using "two_wheeled_robot_diff_drive" plugin. for tf of static parts we use "robot_state_publisher" and tf of dynamic parts are published using "joint_state_publisher". however since rviz, robot_state_publisher and joint_state_publisher are already packed nicely and launched in urdf_tutorial_example, we use this package.

###################### add jointstate and robot state publisher and rviz setting ###################
open another terminal:

``` bash
ros2 launch urdf_tutorial display.launch.py rvizconfig:=rviz2_config.rviz model:=car/model.urdf
```


### Drive
to drive the car, we simply use teleop_twist_keyboard package:

open another terminal:
``` bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```