#!/bin/bash

set -x

function error {
  if [ ~/ros/ws_$REPOSITORY_NAME/build/test_results ]; then find ~/ros/ws_$REPOSITORY_NAME/build/test_results -type f -exec echo "=== {} ===" \; -exec cat {} \; ; fi
  # # after_failure:
  rostest -t roseus test-genmsg.catkin.test
  rostest -t roseus test-genmsg-oneworkspace.catkin.launch
  exit 1
}

trap error ERR

apt-get update
# https://stackoverflow.com/questions/44331836/apt-get-install-tzdata-noninteractive
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
apt-get install -y sudo software-properties-common git wget sed gcc g++

echo "Testing branch $TRAVIS_BRANCH of $REPOSITORY_NAME"
sudo sh -c 'echo "deb http://packages.ros.org/ros-shadow-fixed/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get update -qq
sudo apt-get install -qq -y python-catkin-pkg python-rosdep python-wstool python-catkin-tools ros-$ROS_DISTRO-catkin
sudo rosdep init
rosdep update --include-eol-distros; while [ $? != 0 ]; do sleep 1; rosdep update --include-eol-distros; done
###
### theck if ${BUILDER} works for common messages
###
mkdir -p ~/ros/ws_$REPOSITORY_NAME/src
cd ~/ros/ws_$REPOSITORY_NAME/src
ln -s $CI_SOURCE_PATH . # Link the repo we are testing to the new workspace
git clone https://github.com/ros-gbp/std_msgs-release.git       std_msgs -b release/${ROS_DISTRO}/std_msgs
git clone https://github.com/ros-gbp/ros_comm_msgs-release.git  std_srvs -b release/${ROS_DISTRO}/std_srvs
git clone https://github.com/ros-gbp/ros_comm_msgs-release.git  rosgraph_msgs -b release/${ROS_DISTRO}/rosgraph_msgs
for pkg in actionlib_msgs diagnostic_msgs geometry_msgs nav_msgs sensor_msgs shape_msgs stereo_msgs trajectory_msgs visualization_msgs; do
  git clone https://github.com/ros-gbp/common_msgs-release.git  $pkg -b release/${ROS_DISTRO}/$pkg
done
git clone https://github.com/ros-gbp/actionlib-release.git      actionlib -b release/${ROS_DISTRO}/actionlib
find actionlib  -name CMakeLists.txt  -exec sed -i 's@add_subdirectory(test)@#add_subdirectory(test)@' {} \;
cd ..
rosdep install -q -n --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
# script:
source /opt/ros/$ROS_DISTRO/setup.bash
## on indigo we have to compile geneus before other packages..
if [ "${BUILDER}" == "catkin_make" ]; then ${BUILDER} geneus $ROS_PARALLEL_JOBS; rm -fr build; source devel/setup.bash; fi
${BUILDER} $ROS_PARALLEL_JOBS
## test for roseus
sudo apt-get install -qq -y ros-${ROS_DISTRO}-roseus
sudo dpkg -r --force-depends ros-${ROS_DISTRO}-geneus
###
### theck if ${BUILDER} works with test code
###
## need to use latest test codes
rm -fr devel build src/*
cd src
# clone only roseus package
git clone http://github.com/jsk-ros-pkg/jsk_roseus /tmp/jsk_roseus
(cd /tmp/jsk_roseus; git checkout `git describe --abbrev=0 --tags`)
cp -r /tmp/jsk_roseus/roseus ./
# clone std_msgs which is required by test codes
git clone https://github.com/ros-gbp/std_msgs-release.git       std_msgs -b release/${ROS_DISTRO}/std_msgs
# copy geneus package
##- sudo wget https://raw.githubusercontent.com/k-okada/jsk_roseus/fix_generate_all/roseus/scripts/generate-all-msg-srv.sh -O /opt/ros/hydro/share/roseus/scripts/generate-all-msg-srv.sh
ln -s $CI_SOURCE_PATH . # Link the repo we are testing to the new workspace
cd ..
## check roseus
source /opt/ros/$ROS_DISTRO/setup.bash
rm -fr build devel # need to clean up to check #42 case
if [ "${BUILDER}" == "catkin_make" ]; then ${BUILDER} --only-pkg-with-deps geneus $ROS_PARALLEL_JOBS; rm -fr build; source devel/setup.bash; fi
if [ "${BUILDER}" == "catkin build" ]; then ${BUILDER} geneus $ROS_PARALLEL_JOBS; source devel/setup.bash; fi
${BUILDER}
source devel*/setup.bash
if [ "${BUILDER}" == "catkin_make_isolated" ] ; then cat devel_isolated/roseus/share/roseus/ros/roseus/manifest.l; fi
if [ "${BUILDER}" != "catkin_make_isolated" ] ; then cat devel/share/roseus/ros/roseus/manifest.l; fi
## check https://github.com/jsk-ros-pkg/geneus/pull/42
if [ "${BUILDER}" == "catkin_make_isolated" ] ; then [ `grep -c -e "/opt/ros/${ROS_DISTRO}/share/roseus/package.xml" devel_isolated/roseus/share/roseus/ros/roseus/manifest.l` != 1 ]; fi
if [ "${BUILDER}" != "catkin_make_isolated" ] ; then [ `grep -c -e "/opt/ros/${ROS_DISTRO}/share/roseus/package.xml" devel/share/roseus/ros/roseus/manifest.l` != 1 ]; fi
rostest geneus test-geneus.test
rostest roseus test-genmsg.catkin.test
rostest roseus test-genmsg-oneworkspace.catkin.launch
## check pr2eus
git clone http://github.com/jsk-ros-pkg/jsk_pr2eus src/jsk_pr2eus
(cd src/jsk_pr2eus; git checkout `git describe --abbrev=0 --tags`)
sudo apt-get -qq -f install
rosdep install -q -r -n --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
sudo dpkg -r --force-depends ros-${ROS_DISTRO}-geneus
rm -fr build devel install logs .catkin*
source /opt/ros/$ROS_DISTRO/setup.bash
if [ "${BUILDER}" == "catkin_make" ]; then ${BUILDER} --only-pkg-with-deps geneus $ROS_PARALLEL_JOBS; rm -fr build; source devel/setup.bash; fi
if [ "${BUILDER}" == "catkin build" ]; then ${BUILDER} geneus $ROS_PARALLEL_JOBS; source devel/setup.bash; fi
${BUILDER}
source devel*/setup.bash
rostest pr2eus default-ri-test.test
# pr2_controllers_msgs is not released on kinetic and that's ok for geneus test
# rostest pr2eus pr2-ri-test-simple.launch
# rostest pr2eus pr2eus-test.launch
#
# # after_failure:
# rostest -t roseus test-genmsg.catkin.test
# rostest -t roseus test-genmsg-oneworkspace.catkin.launch
