cmake_minimum_required(VERSION 3.0.2)
project(rqt_rviz)
# Load catkin and all dependencies required for this package

find_package(Boost REQUIRED COMPONENTS program_options)
include_directories(SYSTEM ${Boost_INCLUDE_DIRS})

find_package(catkin REQUIRED COMPONENTS rqt_gui rqt_gui_cpp rviz)
catkin_package(	
	INCLUDE_DIRS ${rqt_rviz_INCLUDE_DIRECTORIES}
	LIBRARIES ${PROJECT_NAME} 
	CATKIN_DEPENDS rqt_gui rqt_gui_cpp rviz
)
catkin_python_setup()

set(rqt_rviz_SRCS
  src/rqt_rviz/config_dialog.cpp
  src/rqt_rviz/rviz.cpp
)

set(rqt_rviz_HDRS
  include/rqt_rviz/config_dialog.h
  include/rqt_rviz/rviz.h
)

if("${qt_gui_cpp_USE_QT_MAJOR_VERSION} " STREQUAL "5 ")
  find_package(Qt5 REQUIRED COMPONENTS Widgets)
  qt5_wrap_cpp(rqt_rviz_MOCS ${rqt_rviz_HDRS})
  set(qt_LIBRARIES Qt5::Widgets)
else()
  find_package(Qt4 COMPONENTS QtCore QtGui REQUIRED)
  include(${QT_USE_FILE})
  qt4_wrap_cpp(rqt_rviz_MOCS ${rqt_rviz_HDRS})
  set(qt_LIBRARIES ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY})
endif()

include_directories(include ${catkin_INCLUDE_DIRS})
add_library(${PROJECT_NAME} ${rqt_rviz_SRCS} ${rqt_rviz_MOCS})
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${qt_LIBRARIES} ${Boost_LIBRARIES})

find_package(class_loader REQUIRED)
class_loader_hide_library_symbols(${PROJECT_NAME})

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION})

catkin_install_python(PROGRAMS scripts/rqt_rviz
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)
