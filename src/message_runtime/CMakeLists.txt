cmake_minimum_required(VERSION 3.0.2)
project(message_runtime)

find_package(catkin REQUIRED)

catkin_package(CATKIN_DEPENDS cpp_common roscpp_serialization roscpp_traits rostime)
