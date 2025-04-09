# rospack
A command-line tool for retrieving information about ROS packages available on the filesystem.

## Installation

Install this with [catkin](http://wiki.ros.org/catkin).

#### tinyxml2

With tinyxml2 versions 4.0.0 and 4.0.1 XML parsing of ROS packages will fail for `<?xml-model ...` lines due to a bug (see [#77](https://github.com/ros/rospack/issues/77)). To fix this use versions 2.X, 3.X or >=5. Additionally the ROS apt repositories provide a patched version (4.0.1-2) which also works with rospack for all platform/architecture pairs targeted by ROS Lunar. 
