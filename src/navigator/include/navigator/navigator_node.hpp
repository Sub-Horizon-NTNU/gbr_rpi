#ifndef POWER_TO_PWM_HPP
#define POWER_TO_PWM_HPP

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "std_msgs/msg/float64.hpp"
#include <vector>

using std_msgs::msg::Float64MultiArray;
using std_msgs::msg::Float64;

class Navigator : public rclcpp::Node
{
public:
    Navigator();

private:
    void powerCallback(Float64MultiArray::UniquePtr msg);

    void lightCallback(Float64::UniquePtr msg);

    void idleTimerCallback();

    void setPower(const std::vector<double> &thruster_power);

    double normalisedToDutyCycle(double norm);

private:
    static constexpr double MAX_POWER = 0.75;
    static constexpr int MAX_REPRESENTABLE_TIME = 4000;
    static constexpr int MIN_DURATION = 1100;
    static constexpr int OFF_DURATION = 1500;
    static constexpr int MAX_DURATION = 1900;
    static constexpr int DURATION_RANGE = MAX_DURATION - MIN_DURATION;
    rclcpp::Subscription<Float64MultiArray>::SharedPtr power_subscriber_;
    rclcpp::Subscription<Float64>::SharedPtr light_subscriber_;
    rclcpp::TimerBase::SharedPtr idle_timer_;
};

#endif // POWER_TO_PWM_HPP
