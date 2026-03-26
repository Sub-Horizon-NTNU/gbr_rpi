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
                FindPackageShare('launcher'),
                'launch',
                "cameras.launch.py"
                ]),
                launch_arguments={
                    "left_cam_path": left_cam_path,
                    "right_cam_path": right_cam_path
                }.items()
            )

    navigator = Node(
        package="navigator",
        executable="navigator_node",
        name="navigator_node",
        namespace="/gbr"
    )

    # Return a launch description generated from node list
    return LaunchDescription([
            DeclareLaunchArgument("left_cam_path", default_value="/dev/video0"),
            DeclareLaunchArgument("right_cam_path", default_value="/dev/video4"),
            cameras,
            navigator
        ])
