# Drone Advanced Robotics Project

## Murad Murad, 324994219

## Jwana Abuleil, 318696317

This project works best on ubuntu 22.04

[Screencast from 11-01-25 13:05:59.webm](https://github.com/user-attachments/assets/4ccd1ff0-bf4d-4771-ab53-d35726e026a2)


## Step 1: Setting Up ROS2

Set locale

Make sure you have a locale which supports UTF-8. If you are in a minimal environment (such as a docker container), the locale may be something minimal like POSIX. We test with the following settings. However, it should be fine if you’re using a different UTF-8 supported locale.

`locale  # check for UTF-8`

`sudo apt update && sudo apt install locales`

`sudo locale-gen en_US en_US.UTF-8`

`sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8`

`export LANG=en_US.UTF-8`

`locale  # verify settings`

Setup Sources

You will need to add the ROS 2 apt repository to your system.

First ensure that the Ubuntu Universe repository is enabled.

`sudo apt install software-properties-common`

`sudo add-apt-repository universe`

Now add the ROS 2 GPG key with apt.

`sudo apt update && sudo apt install curl -y`

`sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg`

Then add the repository to your sources list.

`echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null`

Install ROS 2 packages

Update your apt repository caches after setting up the repositories.

`sudo apt update`

ROS 2 packages are built on frequently updated Ubuntu systems. It is always recommended that you ensure your system is up to date before installing new packages.

`sudo apt upgrade`


Desktop Install (Recommended): ROS, RViz, demos, tutorials.

`sudo apt install ros-humble-desktop`

Environment setup

Sourcing the setup script

Set up your environment by sourcing the following file.

Replace ".bash" with your shell if you're not using bash

Possible values are: setup.bash, setup.sh, setup.zsh

`source /opt/ros/humble/setup.bash`

Try some examples

Talker-listener

If you installed ros-humble-desktop above you can try some examples.

In one terminal, source the setup file and then run a C++ talker:

`source /opt/ros/humble/setup.bash`

`ros2 run demo_nodes_cpp talker`

In another terminal source the setup file and then run a Python listener:

`source /opt/ros/humble/setup.bash`

`ros2 run demo_nodes_py listener`

# Install MAVROS for ROS2

MAVROS bridges ROS2 and ArduPilot.

Install MAVROS dependencies:

`sudo apt update`

`sudo apt install -y ros-humble-mavros ros-humble-mavros-extras`

# Step 2: Clone the Advanced Robotics Project Repository

`cd ~`

`git clone https://github.com/MuradMu/advanced_robotics_project.git`

`cd ~/advanced_robotics_project`

# Step 3: Install and Configure Gazebo

Install Gazebo (compatible version):

`sudo apt install -y ros-humble-gazebo-ros-pkgs`

`echo 'source /usr/share/gazebo/setup.sh' >> ~/.bashrc`

`source ~/.bashrc`


# Step 4: Install and Configure ArduPilot

Clone ArduPilot:

`cd ~/advanced_robotics_project`

`git clone https://github.com/ArduPilot/ardupilot.git`

`cd ardupilot`

`git submodule update --init --recursive`

Install prerequisites:

`./Tools/environment_install/install-prereqs-ubuntu.sh -y`

`. ~/.profile`

Build SITL (Software In The Loop):

`./waf configure --board sitl`

`./waf build`

Test SITL:

`./build/sitl/bin/arducopter --model quad`

sim_vehicle.py might not be in your PATH. If you’ve installed ArduPilot in the ~/advanced_robotics_project/ardupilot directory, you need to ensure the Tools/autotest directory is included in your PATH.

Add the following line to your ~/.bashrc file:

`export PATH=$PATH:~/advanced_robotics_project/ardupilot/Tools/autotest`

Then reload your shell with:

`source ~/.bashrc`

install mavproxy:

`sudo pip3 install MAVProxy`

# Step 5: Install YOLOv7

Clone YOLOv7 repository:

`cd ~/advanced_robotics_project`

`git clone https://github.com/WongKinYiu/yolov7.git`

`cd yolov7`

Install YOLOv7 dependencies:

`pip install -r requirements.txt`

# Install Gazebo plugin for APM (ArduPilot Master) :

`cd ~/advanced_robotics_project`

`git clone https://github.com/khancyr/ardupilot_gazebo.git`

`cd ardupilot_gazebo`

build and install plugin

`mkdir build`

`cd build`

`cmake ..`

`make -j4`

`sudo make install`

`echo 'source /usr/share/gazebo/setup.sh' >> ~/.bashrc`

Set paths for models:

`echo 'export GAZEBO_MODEL_PATH=~/advanced_robotics_project/ardupilot_gazebo/models' >> ~/.bashrc`

`. ~/.bashrc`

Run Simulator

NOTE the iris_arducopter_runway is not currently working in gazebo11. The iq_sim worlds DO work

In one Terminal (Terminal 1), run Gazebo:

`gazebo --verbose ~/advanced_robotics_project/ardupilot_gazebo/worlds/iris_arducopter_runway.world`

In another Terminal (Terminal 2), run SITL:

`cd ~/advanced_robotics_project/ardupilot/ArduCopter`

`sim_vehicle.py -v ArduCopter -f gazebo-iris --console`


# Testing After Setup

Verify Gazebo launch:

`gazebo`

Verify ArduPilot SITL:

`cd ~/advanced_robotics_project/ardupilot/ArduCopter`

`sim_vehicle.py -v ArduCopter -f gazebo-iris --console --map`


Test YOLOv7 with a sample image:

`cd ~/advanced_robotics_project/yolov7`

`python detect.py --source inference/images/horses.jpg --weights yolov7.pt`

# change file paths in all files to current user

`find ~/advanced_robotics_project -type f -exec sed -i "s/murad/$(whoami)/g" {} +`

# building the project

`echo 'export GAZEBO_MODEL_PATH=~/advanced_robotics_project/iris/src/iris_drone/models' >> ~/.bashrc`

`echo 'export GAZEBO_RESOURCE_PATH=~/advanced_robotics_project/iris/src/iris_drone/worlds:${GAZEBO_RESOURCE_PATH}' >> ~/.bashrc`

`echo 'source $HOME/advanced_robotics_project/ardupilot/Tools/completion/completion.bash' >> ~/.bashrc`

`echo 'export PATH=$PATH:$HOME/advanced_robotics_project/ardupilot/Tools/autotest' >> ~/.bashrc`

`echo 'export PATH=/usr/lib/ccache:$PATH' >> ~/.bashrc`




`cd ~/advanced_robotics_project/iris`

`sudo apt update`

`sudo apt install python3-rosdep2`

`rosdep update`

`rosdep install -y --from-paths src --ignore-src -r`

`sudo apt install python3-colcon-common-extensions -y`

`export PATH=$PATH:~/.local/bin`

`source ~/.bashrc`

`colcon build`

`source ~/advanced_robotics_project/iris/install/setup.sh`

`source ~/.bashrc`


## copy the opject detection code to the yolov7 directory:

`cp ~/advanced_robotics_project/ros2_yolo.py ~/advanced_robotics_project/yolov7/`


## running the project:

### in termenal 1:

`cd ~/advanced_robotics_project/iris`

`colcon build`

`source ~/advanced_robotics_project/iris/install/setup.sh`

`ros2 launch iris_drone iris.launch.py`

### in termenal 2:

`cd ~/advanced_robotics_project/yolov7`

`python3 ros2_yolo.py`

or if you want to change the target object use:

`python3 ros2_yolo.py [target object]`

example:

`python3 ros2_yolo.py chair`

### in termenal 3:

`cd ~/advanced_robotics_project/iris`

`colcon build`

`source ~/advanced_robotics_project/iris/install/setup.sh`

`ros2 run iris_drone mission`

or if you want to run the real time node:

`ros2 run iris_drone real_time_node`

Adding Search Points: To add search points in the mission code, use the following command structure:

`self.GotoLocation(-35.3630969, 149.1651725, alt)`

`self.GotoLocation(-35.3630969, 149.1651725, alt)`

`self.GotoLocation(-35.3630969, 149.1651725, alt)`

`self.GotoLocation(-35.3630969, 149.1651725, alt)`

For real-time point sending, open a new terminal and execute:

`ros2 topic pub /destination_coordinates geometry_msgs/Point "{x: -35.363244, y: 149.1652153, z: 5.0}"`

`ros2 topic pub /destination_coordinates geometry_msgs/Point "{x: -35.3630969, y: 149.1651725, z: 5.0}"`
