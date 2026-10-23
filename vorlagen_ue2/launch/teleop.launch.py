"""Vorlage für Ü 2, Aufgabe C3: startet turtlesim, die Anzeige und Ihren Umsetzer mit Parameterdatei.

Kopieren nach ~/ros2_ws/src/mein_teleop/launch/teleop.launch.py.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # findet install/mein_teleop/share/mein_teleop – dorthin kopiert colcon die Dateien aus data_files
    parameter = os.path.join(get_package_share_directory('mein_teleop'), 'config', 'umsetzer.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        Node(package='keyboard_teleop_viz', executable='anzeige', output='screen'),
        Node(package='mein_teleop', executable='umsetzer', name='umsetzer',
             parameters=[parameter],
             remappings=[('cmd_vel', '/turtle1/cmd_vel')]),
    ])
