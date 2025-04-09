cmake_minimum_required(VERSION 3.0.2)
project(message_generation)

find_package(catkin REQUIRED)

catkin_package(CATKIN_DEPENDS gencpp geneus gennodejs genlisp genmsg genpy)
