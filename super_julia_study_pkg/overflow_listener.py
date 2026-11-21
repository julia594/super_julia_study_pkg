#!/usr/bin/env python3
"""Слушает топик переполнения; имя топика задаётся параметром"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class OverflowListener(Node):
    def __init__(self):
        super().__init__('overflow_listener')
        self.declare_parameter('overflow_topic', 'overflow')
        topic = self.get_parameter('overflow_topic').value

        self.subscription = self.create_subscription(
            Int32, topic, self.callback, 10)
        self.get_logger().info(f'Слушаю топик {topic}')

    def callback(self, msg):
        self.get_logger().warn(f'!!! ПЕРЕПОЛНЕНИЕ !!! Получено значение: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = OverflowListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
