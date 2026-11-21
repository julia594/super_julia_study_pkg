#!/usr/bin/env python3
"""Запуск публикатора чётных чисел и слушателя переполнения.

Примеры:
  ros2 launch super_julia_study_pkg robot_system.launch.py              # 8 Гц, порог 80
  ros2 launch super_julia_study_pkg robot_system.launch.py mode:=fast   # 20 Гц, порог 50
  ros2 launch super_julia_study_pkg robot_system.launch.py mode:=slow   # 5 Гц, порог 150
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PKG = 'super_julia_study_pkg'

# Настройки режимов из задания два
MODES = {
    'fast': {'publish_frequency': 20.0, 'overflow_threshold': 50,
             'topic_name': '/even_numbers_fast'},
    'slow': {'publish_frequency': 5.0, 'overflow_threshold': 150,
             'topic_name': '/even_numbers_slow'},
}


def launch_setup(context):
    # Читаем значения аргументов как обычные строки
    mode = LaunchConfiguration('mode').perform(context)
    pub_name = LaunchConfiguration('pub_name').perform(context)
    listener_name = LaunchConfiguration('listener_name').perform(context)
    topic_name = LaunchConfiguration('topic_name').perform(context)
    overflow_topic = LaunchConfiguration('overflow_topic').perform(context)

    if mode == 'normal':
        yaml_path = os.path.join(
            get_package_share_directory(PKG), 'params', 'robot_params.yaml')
        pub_params = [yaml_path]
    elif mode in MODES:
        pub_params = [MODES[mode]]
    else:
        raise RuntimeError(f'Неизвестный режим "{mode}". Используйте normal, fast или slow')

    # Явно заданный топик важнее настроек режима
    if topic_name:
        pub_params.append({'topic_name': topic_name})
    pub_params.append({'overflow_topic': overflow_topic})

    return [
        Node(
            package=PKG,
            executable='even_number_publisher',
            name=pub_name,
            parameters=pub_params,
            output='screen',
        ),
        Node(
            package=PKG,
            executable='overflow_listener',
            name=listener_name,
            parameters=[{'overflow_topic': overflow_topic}],
            output='screen',
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='normal',
                              description='Режим: normal (8 Гц), fast (20 Гц) или slow (5 Гц)'),
        DeclareLaunchArgument('pub_name', default_value='even_pub',
                              description='Имя узла-публикатора'),
        DeclareLaunchArgument('listener_name', default_value='overflow_listener',
                              description='Имя узла-слушателя'),
        DeclareLaunchArgument('topic_name', default_value='',
                              description='Топик чётных чисел (пусто — взять из режима)'),
        DeclareLaunchArgument('overflow_topic', default_value='/overflow',
                              description='Топик переполнения'),
        OpaqueFunction(function=launch_setup),
    ])
