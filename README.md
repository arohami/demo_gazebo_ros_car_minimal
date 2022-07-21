# demo_gazebo_ros_car_minimal

## Compatibility
this example is written and tested for:
* ros2 humble
* ign gazebo v6.9.0


an example of driving a simple wheeled robot in ign gazebo with rviz visualization

this example includes seperated models for different parts of the robot. each model has a folder which includes main model description in xacro, auto generated urdf(rviz model) from xacro, modified the auto generated sdf(gazebo model) from urdf and a test_world which includes the sdf model

also there are multiple choices about how to launch the project including docker containers.

</br>

# How to use
there are two methods to run this simulation. 
1. modular launch, run each part seperately: 
    - ign gazebo
    - rviz
    - ign gazebo <-- bridge --> ros2
    - robot state calculation (robo_state_publisher --> tf)
    - keyboard driver (teleop keyboard)

2. launch all together using `ros2 launch`
3. launch all together using bash script
4. launch using docker containers (seperate docker containers with docker-compose)

</br>

## modular launch
**note:** before running any command, ros and the cmd_setup.bash in <PKG_ROOT> should be sourced in terminal.

cmd_setup.bash is a simple bash wrapper for commands to run each module and setup environment. for more details checkout `cmd_setup.bash` file in the <PKG_ROOT> directory.

to see what each command do, check cmd_setup.bash.

open terminal in <PKG_ROOT> directory and enter:
```bash
source cmd_setup.bash
```

</br>

### gazebo


open terminal in root project directory, source ros and cmd_setup.bash and enter:

``` bash
run_ign_gazebo
```
 
or you can launch ign gazebo with ros:
``` bash
run_ros_ign_gazebo
```

don't forget to play simulation (play button at the left bottom of the ign gazebo screen)


### ROS BRIDGE
to convert ign gazebo topics to ros2 topics, we use ros_ign_gazebo_bridge package from ros2. 
open terminal in root project directory, source ros and cmd_setup.bash and enter:

```bash
run_ros_ign_bridge
```


### Robot state calculation
position of the robot is published in ros by "ignition-gazebo-diff-drive-system" ign_gazebo plugin (sdf) and state of joints are published in ros by "libignition-gazebo-joint-state-publisher-system.so". for static parts we use "robot_state_publisher" (ros2 package) to calculate position/orientatin of all parts of the robot.

open terminal in root project directory, source ros and cmd_setup.bash and enter:

```bash
run_robot_state_publisher
```


### ROS Visualization
to visualize data of the robot we use rviz, assuming position of the robot is always known. robot description needed (topic)
for proper model visualization in rviz has already taken care of by robot_state_publisher (or we can directly import the urdf file). 

open terminal in root project directory, source ros and cmd_setup.bash and enter:
``` bash
run_rviz
```

#### Drive
to drive the car, we simply use teleop_twist_keyboard package open terminal in root project directory, source ros and cmd_setup.bash and enter:

open a terminal and enter:
``` bash
run_teleop_keyboard
```

### launch all together (using launch file)
another way to run the demo project is to use ros launch file to configure each package and executor and launch them all together as one. 

open a terminal, source ros and the project (or source cmd_setup.bash), enter:
```bash
ros2 launch demo_gazebo_ros_car_minimal demo_gazebo_ros_car_minimal.launch.py
```
this should open ign gazebo with a red vehicle, rviz with the same model at the center of the world and a terminal to read keystrokes and make the car drivable.
**note:** don't forget to start the simulator as it's paused by default. 

</br>

### run all together using bash file
we can run all this together in one terminal using a 
simple bash script. 
open terminal in root project directory, source ros and cmd_setup.bash and enter:
```bash
run_all
```
**note:** don't forget to play simulation. it's paused by default (or you'll get tons of warning from rviz which is not important but is anying)

</br>

## run in docker
it's also possible and a good practice to try to run everything in an isolated environment like docker. 
dockerfile is already availble in other repos. to use docker you need to either build the image from dockerfile or download it from dockerhub:
```
docker pull arahami/ign_gazebo:fortress
docker pull arahami/ros:humble-desktop-upgraded
```

### how to run
to run the proper container from the docker image, it's best to have a docker runner/launcher file. 
here, docker_run.bash is that file.

open terminal in root project directory, source ros and cmd_setup.bash and enter:
```bash
docker_run
```

</br>