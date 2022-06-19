from setuptools import setup
from glob import glob


package_name = 'demo_gazebo_ros_car_minimal'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ("share/" + package_name + "/launch/", ["launch/demo_gazebo_ros_car_minimal.launch.py"]),
        ("share/" + package_name + "/models/car/car_wheel/", glob("models/car/car_wheel/*")),
        ("share/" + package_name + "/models/car/car_body/", glob("models/car/car_body/*")),
        ("share/" + package_name + "/models/car/car_camera/", glob("models/car/car_camera/*")),
        ("share/" + package_name + "/models/car/car_ball_wheel/", glob("models/car/car_ball_wheel/*")),
        ("share/" + package_name + "/models/car/", glob("models/car/model.sdf*")),
        ("share/" + package_name + "/models/car/", glob("models/car/model.urdf*")),
        ("share/" + package_name + "/models/car/", glob("models/car/model.xacro*")),
        ("share/" + package_name + "/models/car/", glob("models/car/model.config*")),
        ("share/" + package_name + "/models/", glob("models/world.sdf*")),
        ("share/" + package_name + "/models/ground_plane/", glob("models/ground_plane/*")),
        ("share/" + package_name + "/models/sun/", glob("models/sun/*")),
        ("share/" + package_name, ["rviz2_config.rviz"]),
        ("share/" + package_name, ["ign_gazebo_gui.config"]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arahami',
    maintainer_email='a.rahami88@gmail.com',
    description='gazebo example with ros',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
