# demo_gazebo_ros_car_minimal

## Compatibility
this example is written and tested for:
* ros2 foxy
* gazebo v11.11.0


an example of simple 4 wheel car in gazebo and rviz visualization plus explaination

this example includes seperated models for gazebo (sdf) and rviz (urdf) files so editting models would be a little bit easier. final robot model includes models, connects them together (joints) and imports plugins.

## URDF
urdf files are written using xacro. then they are converted to urdf files using `ros2 xacro xacro model.xacro > model.urdf` command.

## SDF
sdf files for each part are initially created using `gz sdf -p model.urdf > model.sdf`. since some parts of the files doesn't convert properly to sdf, further modification are needed:
* \<material> tags in urdf (inside \<gazebo> tag) are the color specifications of the model for sdf. but they don't convert properly from urdf to sdf. so material elements are directly inserted in sdf model after conversion.
* since urdf \<joint>s are different from the ones from sdf, "revolute" joints are used in urdf for the simplest representation of "ball" joints in the sdf. since this example is supposed to be as simple as possible, rear wheels of the car are considered to be spherical with ball joints.


## How to use
open terminal in root project directory, source ros and enter:
``` bash
 export GAZEBO_MDOEL_PATH=$GAZEBO_MODEL_PATH:$(pwd)
```
**note**: since files of different parts are relatively included in the main model file, it's important to set this environment variable correctly (so for example $GAZEBO_MODEL_PATH/car/car_body should exist)

after setting environment variable, you can launch world.sdf in gazebo directly: 
``` bash
 gazebo car/world.sdf --verbose 
 ```

this should open up gazebo with a red car in the center


### sdf 2 urdf conversion and vice versa

**note:** we can also run gazebo using `ros2 launch gazebo_ros gazebo.launch.py` and then spawn model using `ros2 run gazebo_ros spawn_entity.py -file car/model.urdf -entity "my_robot"`
however since gazebo doens't properly convert some tags from urdf to sdf, model will spawn in gray color! (and so this method is not used)

**note:** we can also write model description in sdf format and then convert it to urdf using pysdf: `ros2 run pysdf sdf2urdf model.sdf model.urdf`. but again, some tags like "joint" that are different in urdf and sdf should be modified manually after the conversion.

**[my forked pysdf repo](https://github.com/arahami/pysdf)**


### ROS Visualization
to visualize data of the robot we use rviz assuming position of the robot is always known. but other parts position should be calculated (tf)
position of the robot is published in ros using "two_wheeled_robot_diff_drive" plugin. for tf of static parts we use "robot_state_publisher" and tf of dynamic parts are published using "joint_state_publisher". however since rviz, robot_state_publisher and joint_state_publisher are already packed nicely and launched in urdf_tutorial_example, we use this package.

open another terminal:

``` bash
ros2 launch urdf_tutorial display.launch.py rvizconfig:=car/rviz2_config.rviz model:=car/model.urdf
```


### Drive
to drive the car, we simply use teleop_twist_keyboard package:

open another terminal:
``` bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```