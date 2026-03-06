cmake_minimum_required(VERSION 3.8)
project(navigator)

set(NODE_NAME "${PROJECT_NAME}_node")

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(${NODE_NAME} src/main.cpp src/navigator_node.cpp)

target_include_directories(${NODE_NAME} PRIVATE
    include
    lib/navigator-lib
)

target_link_directories(${NODE_NAME} PRIVATE lib/navigator-lib/lib)
target_link_libraries(${NODE_NAME} 
    rclcpp::rclcpp
    ${std_msgs_TARGETS}
    bluerobotics_navigator
)

install(TARGETS
    ${NODE_NAME}
    DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
