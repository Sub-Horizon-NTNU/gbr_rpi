#include "power_to_pwm/power_to_pwm.hpp"
#include "bindings.h"

PowerToPwm::PowerToPwm()
    : rclcpp::Node("power_to_pwm")
{
    // Navigator Init
    printf("Initiating navigator module.\n");
    set_rgb_led_strip_size(1);
    set_raspberry_pi_version(Raspberry::Pi5);
    init();
    set_pwm_enable(true);
    // 250 Hz == 4000 µs max
    set_pwm_freq_hz(250);
    // Min: 1100 µs, 0.275 * 4000 µs
    // Max: 1900 µs, 0.475 * 4000 µs
    // End Navigator Init

    power_subscriber_ = create_subscription<Float64MultiArray>("/gbr/thrusters", 1,
            std::bind(&PowerToPwm::PowerCallback, this, std::placeholders::_1));

    idle_timer_ = create_timer(std::chrono::milliseconds(1000), 
            std::bind(&PowerToPwm::idleTimerCallback, this));
}

void PowerToPwm::PowerCallback(Float64MultiArray::UniquePtr msg)
{
    setPower(msg->data);
}

void PowerToPwm::idleTimerCallback()
{
    std::vector<double> power(8, 0.0);
    setPower(power);
}

void PowerToPwm::setPower(const std::vector<double> &thruster_power)
{
    // Feels hacky, but works
    idle_timer_->cancel();
    idle_timer_ = create_timer(std::chrono::milliseconds(1000), 
            std::bind(&PowerToPwm::idleTimerCallback, this));

    // Ignore above 8 because we have 8 thrusters
    int size = std::min<int>(8, thruster_power.size());
    for (int i = 0; i < size; i++)
    {
        double power = thruster_power[i];
        power = std::min(power, 1.0);
        power = std::max(power, -1.0);

        double norm_power = (power + 1)/2;

        double duration = norm_power * DURATION_RANGE + MIN_DURATION;

        double duty_cycle = duration / MAX_REPRESENTABLE_TIME;
        // Zero indexed
        set_pwm_channel_duty_cycle(8 + i, duty_cycle);
        RCLCPP_INFO(get_logger(), "%i: %fms, %f%%", i+9, duration, duty_cycle);
    }
}
