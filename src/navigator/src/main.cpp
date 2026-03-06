#include "navigator/navigator_node.hpp"

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto navigator = std::make_shared<Navigator>();
    rclcpp::spin(navigator);
    rclcpp::shutdown();

    return 0;
}

