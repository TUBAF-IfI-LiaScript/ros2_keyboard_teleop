cmake_minimum_required(VERSION 3.8)
project(keyboard_teleop_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Abhängigkeiten: dieselben wie <depend> in package.xml
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Ein ausführbares Programm aus einer Quelldatei ...
add_executable(keyboard_input src/keyboard_input.cpp)
target_compile_features(keyboard_input PUBLIC cxx_std_17)
ament_target_dependencies(keyboard_input rclcpp std_msgs)

# ... wird dorthin installiert, wo `ros2 run keyboard_teleop_cpp keyboard_input` es sucht.
install(TARGETS keyboard_input
  DESTINATION lib/${PROJECT_NAME})

ament_package()
