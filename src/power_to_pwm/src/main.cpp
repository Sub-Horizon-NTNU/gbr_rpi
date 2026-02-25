#include "power_to_pwm/power_to_pwm.hpp"

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto p2p = std::make_shared<PowerToPwm>();
    rclcpp::spin(p2p);
    rclcpp::shutdown();

    return 0;
}

