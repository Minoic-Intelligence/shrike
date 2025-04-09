REM generated from ros_environment/env-hooks/1.ros_package_path.bat.em

setlocal EnableDelayedExpansion

set ROS_PACKAGE_PATH_PARENTS=
for /f %%a in ('@(PYTHON_EXECUTABLE) %~dp0_parent_package_path.py') do set ROS_PACKAGE_PATH_PARENTS=!ROS_PACKAGE_PATH_PARENTS!%%a

set ROS_PACKAGE_PATH=%ROS_PACKAGE_PATH_PARENTS%

REM Make sure the variable survives local scope
endlocal && set ROS_PACKAGE_PATH=%ROS_PACKAGE_PATH%
