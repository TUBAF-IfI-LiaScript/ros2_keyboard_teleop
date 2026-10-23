// Tastatureingabe für die Fahrbefehle eines Roboters.
//
// Liest einzelne Tasten aus dem Terminal und veröffentlicht die aktuelle
// Vorgabe für Vorwärts- und Drehgeschwindigkeit auf zwei Topics:
//
//   /keyboard_teleop/linear   std_msgs/msg/Float64   [m/s]
//   /keyboard_teleop/angular  std_msgs/msg/Float64   [rad/s]
//
// Tasten: w/s schneller/langsamer, a/d nach links/rechts drehen,
//         Leertaste anhalten, q beenden.
//
// Die Tastatur gehört genau einem Terminal. Starten Sie den Knoten deshalb
// mit `ros2 run` in einem eigenen Terminal, nicht aus einer Launch-Datei.
//
// Idee: Johannes Kohl · Autoren: Sebastian Zug & Claude Code (Opus 5.5)

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <memory>

#include <sys/select.h>
#include <termios.h>
#include <unistd.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

using namespace std::chrono_literals;

namespace
{

// Schaltet das Terminal in den Rohmodus (jede Taste sofort, ohne Echo)
// und stellt beim Verlassen des Gültigkeitsbereichs den alten Zustand wieder her.
class RawTerminal
{
public:
  RawTerminal()
  {
    tcgetattr(STDIN_FILENO, &alt_);
    termios roh = alt_;
    roh.c_lflag &= ~(ICANON | ECHO);
    roh.c_cc[VMIN] = 0;
    roh.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &roh);
  }
  ~RawTerminal() {tcsetattr(STDIN_FILENO, TCSANOW, &alt_);}

private:
  termios alt_{};
};

// Wartet höchstens `timeout` auf eine Taste; liefert 0, wenn keine kam.
char lies_taste(std::chrono::milliseconds timeout)
{
  fd_set lesen;
  FD_ZERO(&lesen);
  FD_SET(STDIN_FILENO, &lesen);
  timeval tv{0, static_cast<suseconds_t>(timeout.count() * 1000)};
  if (select(STDIN_FILENO + 1, &lesen, nullptr, nullptr, &tv) > 0) {
    char c = 0;
    if (read(STDIN_FILENO, &c, 1) == 1) {
      return c;
    }
  }
  return 0;
}

}  // namespace

class KeyboardInput : public rclcpp::Node
{
public:
  KeyboardInput()
  : Node("keyboard_input")
  {
    schritt_linear_ = declare_parameter("step_linear", 0.05);    // m/s je Tastendruck
    schritt_angular_ = declare_parameter("step_angular", 0.25);  // rad/s je Tastendruck
    max_linear_ = declare_parameter("max_linear", 0.5);
    max_angular_ = declare_parameter("max_angular", 2.0);
    const double rate = declare_parameter("rate", 10.0);         // Hz

    pub_linear_ = create_publisher<std_msgs::msg::Float64>("/keyboard_teleop/linear", 10);
    pub_angular_ = create_publisher<std_msgs::msg::Float64>("/keyboard_teleop/angular", 10);
    // Die Vorgabe wird regelmäßig gesendet, nicht nur bei einem Tastendruck:
    // So sieht auch ein später gestarteter Knoten sofort den aktuellen Wert.
    timer_ = create_wall_timer(
      std::chrono::duration<double>(1.0 / rate), [this] {veroeffentlichen();});
  }

  // Verarbeitet eine Taste; liefert false, wenn das Programm enden soll.
  bool taste(char c)
  {
    switch (c) {
      case 'w': linear_ += schritt_linear_; break;
      case 's': linear_ -= schritt_linear_; break;
      case 'a': angular_ += schritt_angular_; break;
      case 'd': angular_ -= schritt_angular_; break;
      case ' ': linear_ = 0.0; angular_ = 0.0; break;
      case 'q': return false;
      default: return true;
    }
    linear_ = std::clamp(linear_, -max_linear_, max_linear_);
    angular_ = std::clamp(angular_, -max_angular_, max_angular_);
    std::printf("\rlinear: %+5.2f m/s   angular: %+5.2f rad/s   ", linear_, angular_);
    std::fflush(stdout);
    return true;
  }

  void stopp()
  {
    linear_ = 0.0;
    angular_ = 0.0;
    veroeffentlichen();
  }

private:
  void veroeffentlichen()
  {
    std_msgs::msg::Float64 msg;
    msg.data = linear_;
    pub_linear_->publish(msg);
    msg.data = angular_;
    pub_angular_->publish(msg);
  }

  double linear_ = 0.0, angular_ = 0.0;
  double schritt_linear_, schritt_angular_, max_linear_, max_angular_;
  rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_linear_, pub_angular_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  if (!isatty(STDIN_FILENO)) {
    std::fprintf(stderr,
      "keyboard_input braucht ein eigenes Terminal: starten Sie es mit\n"
      "  ros2 run keyboard_teleop_cpp keyboard_input\n");
    rclcpp::shutdown();
    return 1;
  }
  auto node = std::make_shared<KeyboardInput>();
  std::printf(
    "Tastatur: w/s schneller/langsamer, a/d links/rechts, Leertaste Stopp, q Ende\n");
  {
    RawTerminal terminal;
    while (rclcpp::ok()) {
      const char c = lies_taste(50ms);
      if (c && !node->taste(c)) {
        break;
      }
      rclcpp::spin_some(node);
    }
    node->stopp();
  }
  std::printf("\n");
  rclcpp::shutdown();
  return 0;
}
