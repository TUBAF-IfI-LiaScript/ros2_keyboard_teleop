"""Vorlage für Ü 2, Aufgabe C1: macht aus den beiden Tastatur-Topics einen Fahrbefehl auf cmd_vel.

Kopieren nach ~/ros2_ws/src/mein_teleop/mein_teleop/umsetzer.py und die beiden TODO ergänzen.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class Umsetzer(Node):
    """Macht aus den beiden Tastatur-Topics einen Fahrbefehl auf cmd_vel."""

    def __init__(self):
        super().__init__('umsetzer')
        self.linear = 0.0
        self.angular = 0.0
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Float64, '/keyboard_teleop/linear', self.bei_linear, 10)
        # TODO 1: auch /keyboard_teleop/angular abonnieren (Rückruf: self.bei_angular)
        self.create_timer(0.1, self.senden)  # 10 Hz

    def bei_linear(self, msg):
        self.linear = msg.data

    def bei_angular(self, msg):
        self.angular = msg.data

    def senden(self):
        befehl = Twist()
        # TODO 2: befehl.linear.x und befehl.angular.z füllen
        self.pub.publish(befehl)


def main(args=None):
    rclpy.init(args=args)
    node = Umsetzer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
