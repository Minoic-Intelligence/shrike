cmake_minimum_required(VERSION 3.0.2)
project(resource_retriever)

find_package(catkin REQUIRED COMPONENTS rosconsole roslib)

find_package(Boost REQUIRED)

include(FindCURL)
if(NOT CURL_FOUND)
  message("CURL not found!  Aborting...")
  fail()
endif(NOT CURL_FOUND)

include_directories(include
                    ${catkin_INCLUDE_DIRS}
                    ${CURL_INCLUDE_DIRS}
                    ${Boost_INCLUDE_DIRS})

link_directories(${catkin_LIBRARY_DIRS})

catkin_python_setup()

catkin_package(
  LIBRARIES ${PROJECT_NAME}
  INCLUDE_DIRS include)

add_library(${PROJECT_NAME} src/retriever.cpp)
target_link_libraries(${PROJECT_NAME} ${CURL_LIBRARIES} ${catkin_LIBRARIES})

if(CATKIN_ENABLE_TESTING)
  add_subdirectory(test EXCLUDE_FROM_ALL)
endif()

install(TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION})

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION})
