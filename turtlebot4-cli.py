#!/usr/bin/env python3
import subprocess
import os
from teleop import main as arrows

env = os.environ.copy()

def byeByePrinter():
    print("\nBye Bye!")

def execInAnotherTerminal(cmd: str):
    subprocess.Popen(
        f"gnome-terminal -- bash -c '{cmd}; exec bash'",
        shell=True,
        executable='/bin/bash',
        env=env
    )


commands = {
    "dock": "ros2 action send_goal /robot/dock irobot_create_msgs/action/Dock {}",
    "undock": "ros2 action send_goal /robot/undock irobot_create_msgs/action/Undock {}",
    "battery": "ros2 topic echo /robot/battery_state --qos-reliability reliable --qos-durability transient_local --once",
    "arrows": arrows,
    "rviz": lambda: execInAnotherTerminal("ros2 launch turtlebot4_viz view_robot.launch.py namespace:=/robot"),
    "slam": lambda: execInAnotherTerminal("ros2 launch turtlebot4_navigation slam.launch.py namespace:=/robot"),
}

print("Available commands:", list(commands.keys()))
print("Write 'quit' or 'exit' to exit from the CLI\n")

try:
    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == "quit" or cmd == "exit":
            byeByePrinter()
            break
        elif cmd in commands:
            if callable(commands[cmd]):
                commands[cmd]()
            else:
                subprocess.run(commands[cmd], shell=True, executable='/bin/bash', env=env)
        else:
            print(f"Command '{cmd}' not found. Available ones: {list(commands.keys())}")
except KeyboardInterrupt:
    byeByePrinter()