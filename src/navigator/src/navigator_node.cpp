#include "navigator/navigator_node.hpp"
#include "bindings.h"

Navigator::Navigator()
    : rclcpp::Node("navigator_node")
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
            std::bind(&Navigator::powerCallback, this, std::placeholders::_1));

    light_subscriber_ = create_subscription<Float64>("/gbr/light", 1,
            std::bind(&Navigator::lightCallback, this, std::placeholders::_1));

    rclcpp::QoS sensorQos = rclcpp::SensorDataQoS();
    imu_publisher_ = create_publisher<Imu>("/gbr/navigator_imu", sensorQos);

    idle_timer_ = create_timer(std::chrono::milliseconds(1000), 
            std::bind(&Navigator::idleTimerCallback, this));

    imu_poll_timer_ = create_timer(std::chrono::milliseconds(10), 
            std::bind(&Navigator::imuPollCallback, this));
}

void Navigator::powerCallback(Float64MultiArray::UniquePtr msg)
{
    setPower(msg->data);
}

void Navigator::lightCallback(Float64::UniquePtr msg)
{
    // Zero indexed, PWM 12
    set_pwm_channel_duty_cycle(11, normalisedToDutyCycle(msg->data));
}

void Navigator::idleTimerCallback()
{
    std::vector<double> power(8, 0.0);
    setPower(power);
}

void Navigator::imuPollCallback()
{
    AxisData acceleration = read_accel();
    AxisData gyro = read_gyro();

    Imu msg;
    msg.linear_acceleration.x = acceleration.x;
    msg.linear_acceleration.y = acceleration.y;
    msg.linear_acceleration.z = acceleration.z;
    msg.angular_velocity.x = gyro.x;
    msg.angular_velocity.y = gyro.y;
    msg.angular_velocity.z = gyro.z;

    imu_publisher_->publish(msg);
}

void Navigator::setPower(const std::vector<double> &thruster_power)
{
    // Feels hacky, but works (kinda)
    idle_timer_->cancel();
    idle_timer_ = create_timer(std::chrono::milliseconds(1000), 
            std::bind(&Navigator::idleTimerCallback, this));

    // Ignore above 8 because we have 8 thrusters
    int size = std::min<int>(8, thruster_power.size());
    for (int i = 0; i < size; i++)
    {
        double power = thruster_power[i];
        power = std::min(power, 1.0);
        power = std::max(power, -1.0);

        double norm_power = (power + 1)/2;

        // double duty_cycle = normalisedToDutyCycle(norm_power);
        double duration =  OFF_DURATION + power * DURATION_RANGE / 2 * MAX_POWER;
        double duty_cycle = duration / MAX_REPRESENTABLE_TIME;

        set_pwm_channel_duty_cycle(i, duty_cycle);
        // RCLCPP_INFO(get_logger(), "%i: %fms, %f%%", i, duration, duty_cycle);
    }
}

double Navigator::normalisedToDutyCycle(double norm)
{
    double duration = norm * DURATION_RANGE + MIN_DURATION;
    double duty_cycle = duration / MAX_REPRESENTABLE_TIME;

    return duty_cycle;
}
