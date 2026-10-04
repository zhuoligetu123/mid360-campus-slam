/* src/standalone_main.cpp */
#include "rclcpp/rclcpp.hpp"
#include "rplidar_node.hpp"
#include <memory>

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  auto node = std::make_shared<RPlidarNode>(rclcpp::NodeOptions());

  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node->get_node_base_interface());
  executor.spin();

  rclcpp::shutdown();
  return 0;
}
