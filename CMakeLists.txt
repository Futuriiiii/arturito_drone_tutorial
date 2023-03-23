cmake_minimum_required(VERSION 3.8)
project(arturito_drone_tutorial)

find_package(ament_cmake REQUIRED)

install(DIRECTORY 
	images
	launch
	meshes
	models
	rviz
	urdf
	worlds
	
  DESTINATION share/${PROJECT_NAME})
  
  ament_package()
