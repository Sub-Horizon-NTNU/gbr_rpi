from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    left_cam_path = LaunchConfiguration("left_cam_path")
    right_cam_path = LaunchConfiguration("right_cam_path")

    cameras = IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('h264_streamer'),
                'launch',
                "cameras.launch.py"
                ]),
                launch_arguments={
                    "left_cam_path": left_cam_path,
                    "right_cam_path": right_cam_path
                }.items()
            )

    imus = IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('imu_reader'),
                'launch',
                "imu_launch.py"
                ])
            )

    pressure_sensor = IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('pressure_reader'),
                'launch',
                "pressure.launch.py"
                ])
            )

    navigator = Node(
        package="navigator",
        executable="navigator_node",
        name="navigator_node",
        namespace="/gbr"
    )

    # Return a launch description generated from node list
    return LaunchDescription([
            DeclareLaunchArgument("left_cam_path", default_value="/dev/video2"),
            DeclareLaunchArgument("right_cam_path", default_value="/dev/video6"),
            cameras,
            imus,
            pressure_sensor,
            navigator
        ])
