#!/bin/bash

set -x
set -e

# add source list
# assume debian case is sid
if grep Ubuntu /etc/issue; then
    sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list # enable to run apt-get build-dep
else
    echo 'deb-src http://deb.debian.org/debian sid main' >> /etc/apt/sources.list
fi

apt-get update
# https://stackoverflow.com/questions/44331836/apt-get-install-tzdata-noninteractive
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
apt-get -y install git

# install catkin build deps
apt-get -y build-dep catkin

# compile geneus along with latest genmsg
mkdir -p ~/ros/ws_$REPOSITORY_NAME/src
cd ~/ros/ws_$REPOSITORY_NAME/src
ln -s $CI_SOURCE_PATH . # Link the repo we are testing to the new workspace

if [ "$USE_GENMSG_BINARY" == "true" ]; then
    # install catkin/genmsg from binary
    if apt-get install -y python-genmsg; then
        apt-get build-dep -y python-genmsg
    elif apt-get install -y python3-genmsg; then
        apt-get build-dep -y python3-genmsg
    else
        echo "Could not install python-genmsg"
        exit -1
    fi
    export BUILDER='catkin_make_isolated'
else
    # install catkin/genmsg from source
    git clone https://github.com/ros/catkin.git
    git clone https://github.com/ros/genmsg.git

    # install rosdep
    if apt-get -y install python-rosdep; then
        echo "python-rosdep installed"
    elif apt-get -y install python3-rosdep; then
        echo "python3-rosdep installed"
    else
        echo "failed to install rosdep"
        exit -1
    fi
    [ ! -e /etc/ros/rosdep/sources.list.d ] && rosdep init
    rosdep update
    # skip python3-empy, which is not has rosdep key for debian:sid and installed via apt build-dep catkin
    rosdep install -y --from-paths . --ignore-src --os=$DOCKER_IMAGE --skip-keys=python3-empy
    export BUILDER='python3 src/catkin/bin/catkin_make_isolated'
fi
cd ..
$BUILDER --cmake-args "-Werror=dev"

# check if geneus works
cd ~/ros/ws_$REPOSITORY_NAME/src
git clone https://github.com/ros/std_msgs.git
git clone https://github.com/ros/ros_comm_msgs.git
git clone https://github.com/ros/message_generation.git
git clone https://github.com/ros/message_runtime.git
sed -i 's/^catkin_package(CATKIN_DEPENDS/catkin_package(CATKIN_DEPENDS geneus) #/' message_generation/CMakeLists.txt
sed -i 's/^catkin_package(CATKIN_DEPENDS/catkin_package(CATKIN_DEPENDS) #/' message_runtime/CMakeLists.txt
cd ..
ROS_LANG_DISABLE=gencpp:gennodejs:genlisp:genpy $BUILDER --cmake-args "-Werror=dev"

