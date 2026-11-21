#!/usr/bin/env python3
"""Публикует чётные числа; частота, порог и топики задаются параметрами"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')

        # Объявляем параметры со значениями по умолчанию
        self.declare_parameter('publish_frequency', 10.0)
        self.declare_parameter('overflow_threshold', 100)
        self.declare_parameter('topic_name', 'even_numbers')
        self.declare_parameter('overflow_topic', 'overflow')

        freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        topic = self.get_parameter('topic_name').value
        overflow_topic = self.get_parameter('overflow_topic').value

        self.even_pub = self.create_publisher(Int32, topic, 10)
        self.overflow_pub = self.create_publisher(Int32, overflow_topic, 10)
        self.counter = 0
        self.timer = self.create_timer(1.0 / freq, self.timer_callback)

        self.get_logger().info(
            f'Запущен: {freq} Гц, порог {self.threshold}, '
            f'топик {topic}, переполнение в {overflow_topic}')

    def timer_callback(self):
        if self.counter >= self.threshold:
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
