#ifndef POWER_TO_PWM_HPP
#define POWER_TO_PWM_HPP

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

using std_msgs::msg::Float64MultiArray;

class PowerToPwm : public rclcpp::Node
{
public:
    PowerToPwm();

private:
    void PowerCallback(Float64MultiArray::UniquePtr msg);

private:
    static constexpr int MAX_REPRESENTABLE_TIME = 4000;
    static constexpr int MIN_DURATION = 1100;
    static constexpr int MAX_DURATION = 1900;
    static constexpr int DURATION_RANGE = MAX_DURATION - MIN_DURATION;
    rclcpp::Subscription<Float64MultiArray>::SharedPtr power_subscriber_;
};

#endif // POWER_TO_PWM_HPP
