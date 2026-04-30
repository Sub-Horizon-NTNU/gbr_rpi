import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    imus = [
        {'channel': 0, 'acc_addr': 0x18, 'gyro_addr': 0x68, 'topic': '/gbr/imu1', 'acc_scale': 1367.0, 'gyro_scale': 16.4},
        {'channel': 1, 'acc_addr': 0x19, 'gyro_addr': 0x69, 'topic': '/gbr/imu2', 'acc_scale': 1367.0, 'gyro_scale': 16.4},
        {'channel': 2, 'acc_addr': 0x19, 'gyro_addr': 0x69, 'topic': '/gbr/imu3', 'acc_scale': 1367.0, 'gyro_scale': 16.4},
    ]
    # Konverter til JSON-streng
    import json
    imus_json = json.dumps(imus)

    return LaunchDescription([
        Node(
            package='imu_reader',
            executable='imu_node',
            name='imu_node',
            parameters=[{'imus': imus_json, 'i2c_bus': 6, 'mux_addr': 0x70}],
            output='screen'
        )
    ])
