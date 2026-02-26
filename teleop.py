#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel_unstamped', 10)

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

    def run(self):
        print("Use keyboard arrows to move the robot. CTRL+C to exit.")
        while True:
            key = self.get_key()
            msg = Twist()
            if key == '\x1b[A':    # up
                msg.linear.x = 0.4
            elif key == '\x1b[B':  # down
                msg.linear.x = -0.2
            elif key == '\x1b[C':  # right
                msg.angular.z = -1.0
            elif key == '\x1b[D':  # left
                msg.angular.z = 1.0
            elif key == '\x03':    # CTRL+C
                break
            self.publisher.publish(msg)

def main():
    rclpy.init()
    node = TeleopKeyboard()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()