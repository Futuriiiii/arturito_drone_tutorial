from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
pkg_arturito_gazebo = get_package_share_path('arturito_drone_tutorial')


def generate_launch_description():
    arturito_drone_tutorial_path = get_package_share_path("arturito_drone_tutorial")
    arturito_drone_tutorial_model_path = arturito_drone_tutorial_path / "urdf/arturito.urdf.xacro"
    arturito_drone_tutorial_rviz = arturito_drone_tutorial_path / "rviz/rviz_minimal_visualization_urdf_config.rviz"

    gui_arg = DeclareLaunchArgument(name="gui", default_value="true", choices=["true", "false"], description="Flag to enable joint_state_publisher_gui")
    model_arg = DeclareLaunchArgument(name="model", default_value=str(arturito_drone_tutorial_model_path), description="Absolute path to robot urdf file")
    rviz_arg = DeclareLaunchArgument(name="rvizconfig", default_value=str(arturito_drone_tutorial_rviz), description="Absolute path to rviz config file")
    
    robot_description = ParameterValue(
   	 	Command(["xacro ", LaunchConfiguration("model")]) ,
      	value_type=str ,
    )
 
    robot_state_publisher_node = Node(
   	 	package= "robot_state_publisher" ,
   	 	executable= "robot_state_publisher" ,
   	 	name= "robot_state_publisher" ,
   	 	parameters= [{"robot_description" : robot_description}],
    )
 
    joint_state_publisher_node = Node(
   		package="joint_state_publisher",
   		executable="joint_state_publisher",
   		condition=UnlessCondition(LaunchConfiguration("gui"))
   	 )

    joint_state_publisher_gui_node = Node(
   		package="joint_state_publisher_gui",
   		executable="joint_state_publisher_gui",
  		condition=IfCondition(LaunchConfiguration("gui"))
   	 )
 
    
    rviz_node = Node(
   	 	package= "rviz2" ,
   	 	executable= "rviz2" ,
   	 	name= "rviz2" ,
   	 	output= "screen" ,
   	 	arguments=["-d", LaunchConfiguration("rvizconfig")] ,
    )
    
    
    gazebo_node = Node(
        package="gazebo_ros" ,
        executable="spawn_entity.py" ,
        name="arturito" ,
        output="screen" ,
        arguments= ["-topic", "/robot_description", "-entity", "arturito_drone_tutorial", "-z", "0.5"] ,
        
    )
    

    return LaunchDescription([
   	 	gui_arg,
    	model_arg ,
   	 	rviz_arg ,
   	 	robot_state_publisher_node ,
   	 	joint_state_publisher_node ,
   	 	joint_state_publisher_gui_node ,
   	 	rviz_node ,
   	 	gazebo_node ,
    ])
