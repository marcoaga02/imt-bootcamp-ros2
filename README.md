This repository contains several files useful to interact with the Turtlebot4 Lite. In particular, the `turtlebot4-cli.py` file, launches a CLI that is very useful to control the robot and to perform additional actions, like launching Rviz2 and slam.
# turtlebot4-cly.py
This file, that can be executed using the commmand `python3 turtlebot4-cly.py`, launches the Command Line Interface for controlling the robot.
# teleop.py
This file launches a ROS2 node, which intercepts the keyboard arrows, and map them to Twist messages that are sent to the ROS2 topic that commands the movement of the robot. Can be executed through the CLI launching the `arrows` command.
