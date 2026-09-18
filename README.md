# 
# Install Dependencies
```
sudo apt install pkg-config gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev  python3-smbus2
```


## What this repository is for

ROS 2 workspace for the **Raspberry Pi onboard the GBR ROV**. It connects cameras, IMUs, a pressure/depth sensor and the Blue Robotics Navigator board to ROS topics.

## Components

- [h264_streamer](src/h264_streamer/): camera streaming with GStreamer.
- [imu_reader](src/imu_reader/): I2C IMU readings through a multiplexer.
- [pressure_reader](src/pressure_reader/): MS5837/Bar30 pressure and depth readings.
- [navigator](src/navigator/): Navigator IMU publishing and PWM output for eight thrusters and a light. The implementation selects Raspberry Pi 5.
- [rov_msgs](src/rov_msgs/): custom depth message.
- [launcher](src/launcher/): combined startup; camera device paths are launch arguments.
- [netplan/](netplan/) and [systemd/](systemd/): machine-specific network/service configuration.

## Build and integration

This repository already contains a `src/` workspace. After sourcing a suitable ROS 2 installation and installing dependencies, build from the repository root:

```sh
colcon build
source install/setup.bash
```

The combined entry point is `ros2 launch launcher bringup.launch.py`. It starts hardware drivers, including Navigator PWM output. Check camera paths, I2C configuration, board compatibility and thruster mapping before using it on hardware. The bundled Navigator shared library is platform-specific; this is not a platform-independent desktop application.
