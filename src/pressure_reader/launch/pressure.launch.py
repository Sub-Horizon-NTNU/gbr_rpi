from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
import smbus2

def is_bar30_present():
    bus = smbus2.SMBus(6) 
    address = 0x76        
    try:
        bus.read_byte_data(address, 0xA0)
        return True
    except OSError:
        return False

def generate_launch_description():
    if (is_bar30_present()):
        is_saltwater = LaunchConfiguration('is_saltwater', default=True)

        return LaunchDescription([
            DeclareLaunchArgument('is_saltwater', default_value='true'),
            Node(
                package='pressure_reader',
                executable='pressure_node',
                name='pressure_node',
                parameters=[{'is_saltwater': is_saltwater, 'i2c_bus': 6}],
                output='screen',
                namespace='/gbr'
            )
        ])
    else:
        return LaunchDescription([LogInfo(msg='Bar30 not found')])
