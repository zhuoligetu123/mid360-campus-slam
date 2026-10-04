from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            name='scanner', default_value='scanner',
            description='Namespace for sample topics'
        ),
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in',  ['/segmentation/obstacle']),
                        ('scan',  ['/scan'])],
            parameters=[{
                'target_frame': 'livox_frame',
                'transform_tolerance': 0.01,
                'min_height': 0.1,          # 最小高度
                'max_height': 1.5,          # 最大高度
                'angle_min': -3.14159,      # -π，完整360度扫描
                'angle_max': 3.14159,       # π，完整360度扫描
                'angle_increment': 0.002618,  # 0.15度（π/1200），高密度
                'scan_time': 0.2333,        # 扫描时间
                'range_min': 0.18,          # 最小检测距离
                'range_max': 100.6,         # 最大检测距离
                'use_inf': True,            # 是否使用无穷大值
                'inf_epsilon': 1.0          # 无穷大值阈值
            }],
            name='pointcloud_to_laserscan'
        )
    ])