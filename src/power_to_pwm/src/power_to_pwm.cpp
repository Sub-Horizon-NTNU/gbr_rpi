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

    power_subscriber_ = create_subscription<Float64MultiArray>("/power_to_pwm/power_in", 10,
            std::bind(&PowerToPwm::PowerCallback, this, std::placeholders::_1));
}

void PowerToPwm::PowerCallback(Float64MultiArray::UniquePtr msg)
{
    // Ignore above 8 because we have 8 thrusters
    for (unsigned i = 0; i < 8; i++)
    {
        double power = msg->data[i];
        power = std::min(power, 1.0);
        power = std::max(power, -1.0);

        double norm_power = (power + 1)/2;

        double duration = norm_power * DURATION_RANGE + MIN_DURATION;

        double duty_cycle = duration / MAX_REPRESENTABLE_TIME;
        // Zero indexed
        set_pwm_channel_duty_cycle(8 + i, duty_cycle);
    }
}
