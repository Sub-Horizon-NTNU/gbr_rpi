from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    left_cam_path = LaunchConfiguration("left_cam_path")
    right_cam_path = LaunchConfiguration("right_cam_path")

    left_cam = Node(
        package="h264_streamer",
        executable="h264_streamer",
        name="left_cam",
        namespace="gbr/cam_left",
        parameters=[{ "device": left_cam_path },
                    { "topic_name": "/gbr/cam_left/image_compressed" }],
        # arguments=[left_cam_path],
        output="screen"
    )

    right_cam = Node(
        package="h264_streamer",
        executable="h264_streamer",
        name="right_cam",
        namespace="gbr/cam_right",
        parameters=[{ "device": right_cam_path },
                    { "topic_name": "/gbr/cam_right/image_compressed" }],
        # arguments=[right_cam_path],
        output="screen"
    )

    # Return a launch description generated from node list
    return LaunchDescription([
        DeclareLaunchArgument("left_cam_path", default_value="/dev/video2"),
        DeclareLaunchArgument("right_cam_path", default_value="/dev/video6"),
        left_cam,
        right_cam
    ])
