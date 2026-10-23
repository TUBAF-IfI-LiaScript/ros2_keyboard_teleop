"""Startet die Anzeige der Tastatur-Vorgabe.

    ros2 launch keyboard_teleop anzeige.launch.py

Die Tastatureingabe selbst starten Sie in einem eigenen Terminal:

    ros2 run keyboard_teleop_cpp keyboard_input

Sie braucht die Tastatur – und die gehört genau einem Terminal. Aus einer
Launch-Datei heraus bekäme der Knoten keine Tasten.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='keyboard_teleop_viz', executable='anzeige', name='keyboard_viz', output='screen'),
    ])
