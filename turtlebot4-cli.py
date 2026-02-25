#!/usr/bin/env python3
import subprocess
import os
import signal
from teleop import main as arrows

env = os.environ.copy()
processes = []

def byeByePrinter():
    print("\nBye Bye!")
    for proc in processes:
        if proc.poll() is None:
            print(f"Stopping PID {proc.pid}...")
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def execInAnotherTerminal(cmd: str):
    proc = subprocess.Popen(
        f"gnome-terminal -- bash -c \"{cmd}\"",
        shell=True,
        executable='/bin/bash',
        env=env,
        preexec_fn=os.setsid,
        stderr=subprocess.DEVNULL
    )

    processes.append(proc)
    print(f"Started process PID {proc.pid}")

commands = {
    "dock": "ros2 action send_goal /robot/dock irobot_create_msgs/action/Dock {}",
    "undock": "ros2 action send_goal /robot/undock irobot_create_msgs/action/Undock {}",
    "battery": "ros2 topic echo /robot/battery_state --qos-reliability reliable --qos-durability transient_local --once",
    "arrows": arrows,
    "rviz": lambda: execInAnotherTerminal(
        f"ros2 launch {os.path.dirname(os.path.abspath(__file__))}/my_view_robot.launch.py "
        f"namespace:=/robot model:=lite "
        f"rviz_config:={os.path.dirname(os.path.abspath(__file__))}/rviz_config.rviz"
    ),
    "slam": lambda: execInAnotherTerminal(
        "ros2 launch turtlebot4_navigation slam.launch.py namespace:=/robot"
    ),
}

print("Available commands:", list(commands.keys()))
print("Write 'quit' or 'exit' to exit from the CLI\n")

try:
    while True:
        cmd = input(">>> ").strip().lower()
        if cmd in ("quit", "exit"):
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