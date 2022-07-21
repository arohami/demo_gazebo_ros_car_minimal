# Details
## model
### folder structure
modles used for the project are either URDF or SDF. URDF is used by rviz to visualize robot data and SDF is used by ign (gazebo).
models are under <PKG_ROOT>/models directory.
main directory for models is `car` which includes xacro file and it's auto generated urdf and sdf(manualy modified).

there are also basic models in this directory like sun and ground. 

and finally the world descriptor file (sdf) which includes all the other models is placed in this directory.

related config files (rviz, ign) can be found under <PKG_ROOT>/configs


### XACRO
xacro file is the main file which other model descriptors are generated from. <gazebo> tag indicates the parts that are just meant for gazebo (sdf) and are ignored in rviz (urdf)

**note:** xacro file of car_wheel and car_ball_wheel doesn't describe the model itself, instead it describes a macro which generates the model (set's model name so there can be multiple instances of the model in the world). this is why urdf/sdf generated files in car_ball_wheel directory are named sample_models. 

### URDF
urdf files are directly generated from xacro without any further changes.

xacro to urdf conversion command:

```bash
ros2 xacro xacro model.xacro > model.urdf
```

to test urdf files seperately: 

``` bash
ros2 launch urdf_tutorial display.launch.py model:=model.urdf
```

and set fixed frame in rviz to the name of the robot in .urdf file: rviz > global options (right panel) > fixed frame

**note:** we can also write model description in sdf format and then convert it to urdf using pysdf: `ros2 run pysdf sdf2urdf model.sdf model.urdf`. but again, some tags like "joint" that are different in urdf and sdf should be modified manually after the conversion.

**[my forked pysdf repo](https://github.com/arahami/pysdf)**

### SDF
sdf files for each part are initially created from urdf. but since some parts of the files doesn't convert properly to sdf, further modification were needed:
* \<material> tags in urdf (inside \<gazebo> tag) are the color specifications of the model for sdf. but they don't convert properly from urdf to sdf. so material elements are directly inserted in sdf model after conversion.
* since urdf \<joint>s are different from the ones from sdf, "revolute" joints are used in urdf for the simplest representation of "ball" joints in the sdf. since this example is supposed to be as simple as possible, rear wheels of the car are considered to be spherical with ball joint.

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

### docker
simulation and all executors can run within docker too. the command to run docker is already embedded in cmd_setup.bash. this file has basic handy commands ini it including command to run doker (docker-compose)
take notice that .bashrc and entrypoint.bash are already mounted into docker container so we can manipulate docker run and docker exec behaviour. 

also ros_ws is a directory which is mounted into the docker to prevent build and install directory loss after docker container exits. all the whole repo is mounted inside ros_ws/src. so basically there are two ways to mount any extra resources to the container without changing the docker_run.bash volumes:
1. from docker_volumes/ros_ws directory
2. from root directory of this package

<br/>

to run simulator on docker we use docker-compose to launch two separate parts together: 
1. docker container for ros
2. docker container for gazebo

both of these docker containers have the whole project mounted on them but their volumes are different, meaning each container will build isolated from the other and keep the built project in it's own mounted volume. 

since the two main parts of the project (ign gazebo and ros) are seperated, a bridge network is created by docker-compose to make 
docker containers be able to communicate with each other. also because containers are seperated, ign and ros_ign_bridge need IGN_PARTITION environment variable to be able to properly connect.