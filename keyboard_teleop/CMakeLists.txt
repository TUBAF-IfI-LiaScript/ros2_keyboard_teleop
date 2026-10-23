cmake_minimum_required(VERSION 3.8)
project(keyboard_teleop)

# Dieses Paket enthält keinen eigenen Code. Es bündelt die beiden anderen
# Pakete (siehe package.xml) und bringt eine Launch-Datei mit.
find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
