#!/usr/bin/env python3
"""Узел, который каждые 5 секунд выводит текущее время"""

import time
import rclpy
from rclpy.node import Node


class TimePrinter(Node):
    def __init__(self):
        super().__init__('time_printer')
        self.timer = self.create_timer(5.0, self.timer_callback)

    def timer_callback(self):
        now = time.strftime('%H:%M:%S', time.localtime())
        self.get_logger().info(f'Текущее время: {now}')


def main(args=None):
    rclpy.init(args=args)
    node = TimePrinter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
