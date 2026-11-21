#!/usr/bin/env python3
"""Публикует чётные числа 0..98 с частотой 10 Гц, на 100 сообщает о переполнении"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        # Имена топиков без "/" в начале, чтобы работали пространства имён
        self.even_pub = self.create_publisher(Int32, 'even_numbers', 10)
        self.overflow_pub = self.create_publisher(Int32, 'overflow', 10)
        self.counter = 0
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Гц
        self.get_logger().info('Узел even_pub запущен')

    def timer_callback(self):
        if self.counter >= 100:
            msg = Int32()
            msg.data = self.counter
            self.overflow_pub.publish(msg)
            self.get_logger().info(f'Переполнение: {self.counter}, сброс на 0')
            self.counter = 0

        msg = Int32()
        msg.data = self.counter
        self.even_pub.publish(msg)
        self.counter += 2


def main(args=None):
    rclpy.init(args=args)
    node = EvenNumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
