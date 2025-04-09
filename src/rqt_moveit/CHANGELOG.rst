^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rqt_moveit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.5.11 (2023-04-14)
-------------------
* Import setup from setuptools instead of distutils.core
* added LICENSE file

0.5.10 (2021-04-07)
-------------------
* fixed renaming of xmlrpc in python 3

0.5.9 (2020-06-02)
------------------
* use catkin_install_python instead of install

0.5.8 (2020-04-19)
------------------
* updated package to format 3

0.5.7 (2017-04-26)
------------------

0.5.6 (2017-01-24)
------------------

0.5.5 (2016-11-02)
------------------

0.5.4 (2016-09-19)
------------------

0.5.3 (2016-05-16)
------------------

0.5.2 (2016-04-29)
------------------

0.5.1 (2016-04-28)
------------------

0.5.0 (2016-04-27)
------------------
* Support Qt 5 (in Kinetic and higher) as well as Qt 4 (in Jade and earlier) (`#101 <https://github.com/ros-visualization/rqt_robot_plugins/pull/101>`_)

0.4.3 (2016-03-08)
------------------

0.4.2 (2015-07-24)
------------------

0.4.1 (2015-04-30)
------------------
* marking plugin as experimental for now

0.4.0 (2014-11-05)
------------------
* update script to use full plugin name

0.3.7 (2014-08-18)
------------------

0.3.6 (2014-07-11)
------------------

0.3.5 (2014-06-02)
------------------

0.3.4 (2014-05-07)
------------------

0.3.3 (2014-01-28)
------------------

0.3.2 (2014-01-08)
------------------
* add groups for rqt plugins (`ros-visualization/rqt_common_plugins#167 <https://github.com/ros-visualization/rqt_common_plugins/issues/167>`_)

0.3.1 (2013-10-09)
------------------

0.3.0 (2013-08-28)
------------------

0.2.16 (2013-07-09)
-------------------
* First public release for Hydro
* Fix; Monitoring parameter doesn't turn to "No" even after the params are gone bug (#25 `ros-visualization/rqt_robot_plugins#25 <https://github.com/ros-visualization/rqt_robot_plugins/issues/25>`_)

* Refactoring

  * Removed unnecessary dependency (ie. rqt_moveit doesn't depend on any of MoveIt! packages)
  * Common steps ported to rqt_py_common pkg
  * Add exception handling around rosnode_ping

* Notation corrected (MoveIt! is correct) @davetcoleman

0.2.15 (2013-04-25)
-------------------
* Fix

  * monitoring parameter wasn't working
  * Removed dependency to MoveIt! (`#20 <https://github.com/rqt_robot_plugins/rqt_robot_plugins/issues/20>`_)
  * segfaults when plugin shutdown bug (`#14 <https://github.com/rqt_robot_plugins/rqt_robot_plugins/issues/14>`_)

* Enhancement

  * Change refresh rate enhancement (`#15 <https://github.com/rqt_robot_plugins/rqt_robot_plugins/issues/15>`_)
  * More efficient GUI layout (packed empty regions)
  * Layout improve (adjust width of tableview to its contents length)
  * Add clarification to its name displayed on rqt_gui (rqt_moveit only monitors, not interact with Moveit!).

0.2.14 (2013-04-12)
-------------------

0.2.13 (2013-04-09)
-------------------
* First public release for Groovy
