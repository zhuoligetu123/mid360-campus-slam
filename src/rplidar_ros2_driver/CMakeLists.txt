cmake_minimum_required(VERSION 3.8)
project(rplidar_ros2_driver)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# =========================================================
# 1. Find Dependencies
# =========================================================
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(diagnostic_updater REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)

# =========================================================
# 2. Build SDK (Static Library)
# =========================================================
file(GLOB SDK_SOURCES
    "src/sdk/src/*.cpp"
    "src/sdk/src/hal/*.cpp"
    "src/sdk/src/dataunpacker/*.cpp"
    "src/sdk/src/dataunpacker/unpacker/*.cpp"
    "src/sdk/src/arch/linux/*.cpp"
)

add_library(rplidar_sdk STATIC ${SDK_SOURCES})
set_target_properties(rplidar_sdk PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(rplidar_sdk PUBLIC
  src/sdk/include
  src/sdk/src
)

# =========================================================
# 3. Build Component (Shared Library)
# =========================================================
# Create a shared library containing the node logic.
# This allows the node to be loaded into a container process for zero-copy communication.
add_library(rplidar_node_component SHARED
  src/rplidar_node.cpp
  src/lidar_driver_wrapper.cpp
)

target_include_directories(rplidar_node_component PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# Link against the RPLIDAR SDK
target_link_libraries(rplidar_node_component rplidar_sdk)

# Link ROS 2 dependencies
ament_target_dependencies(rplidar_node_component
  rclcpp
  rclcpp_components
  rclcpp_lifecycle
  sensor_msgs
  std_srvs
  diagnostic_updater
  tf2
  tf2_ros
  geometry_msgs
)

# Register the component to make it discoverable by rclcpp_components
rclcpp_components_register_nodes(rplidar_node_component "RPlidarNode")

# =========================================================
# 4. Build Standalone Executable
# =========================================================
# Create an executable wrapper for standalone usage (e.g., 'ros2 run ...').
add_executable(rplidar_node src/standalone_main.cpp)

# Link against the component library to avoid code duplication
target_link_libraries(rplidar_node rplidar_node_component)
ament_target_dependencies(rplidar_node rclcpp rclcpp_lifecycle rclcpp_components)

# =========================================================
# 5. Install Rules
# =========================================================
# Install the shared library (Component)
install(TARGETS rplidar_node_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# Install the executable
install(TARGETS rplidar_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

# Install launch files, parameters, and configurations
install(DIRECTORY
  launch
  param
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
