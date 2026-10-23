"""Zeigt die aktuelle Tastatur-Vorgabe als Balken im Terminal an.

Abonniert /keyboard_teleop/linear und /keyboard_teleop/angular (std_msgs/Float64)
und gibt zweimal pro Sekunde eine Zeile aus, z. B.

    linear  [          |#####     ] +0.25 m/s   angular [     #####|          ] +1.00 rad/s

Idee: Johannes Kohl · Autoren: Sebastian Zug & Claude Code (Opus 5.5)
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


def balken(wert, maximum, breite=10):
    """Zeichnet einen Balken von der Mitte aus nach links (negativ) oder rechts (positiv)."""
    n = min(breite, round(abs(wert) / maximum * breite)) if maximum > 0 else 0
    links = ' ' * (breite - n) + '#' * n if wert < 0 else ' ' * breite
    rechts = '#' * n + ' ' * (breite - n) if wert > 0 else ' ' * breite
    return f'[{links}|{rechts}]'


class Anzeige(Node):
    def __init__(self):
        super().__init__('keyboard_viz')
        self.max_linear = self.declare_parameter('max_linear', 0.5).value
        self.max_angular = self.declare_parameter('max_angular', 2.0).value
        self.linear = self.angular = 0.0
        self.letzte = None  # Zeitpunkt der letzten Nachricht
        self.create_subscription(Float64, '/keyboard_teleop/linear', self.bei_linear, 10)
        self.create_subscription(Float64, '/keyboard_teleop/angular', self.bei_angular, 10)
        self.create_timer(0.5, self.zeigen)

    def bei_linear(self, msg):
        self.linear = msg.data
        self.letzte = self.get_clock().now()

    def bei_angular(self, msg):
        self.angular = msg.data
        self.letzte = self.get_clock().now()

    def zeigen(self):
        if self.letzte is None or (self.get_clock().now() - self.letzte).nanoseconds > 1e9:
            self.get_logger().warn('keine Eingabe – läuft keyboard_input in einem eigenen Terminal?')
            return
        self.get_logger().info(
            f'linear  {balken(self.linear, self.max_linear)} {self.linear:+.2f} m/s   '
            f'angular {balken(self.angular, self.max_angular)} {self.angular:+.2f} rad/s')


def main(args=None):
    rclpy.init(args=args)
    node = Anzeige()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
