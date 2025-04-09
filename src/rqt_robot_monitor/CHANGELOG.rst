^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rqt_robot_monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.5.15 (2023-10-02)
-------------------
* Import setup from setuptools instead of distutils.core

0.5.14 (2022-03-16)
-------------------
* Improve error and warning lists by only showing leaf-elements
* Backported alternative view.

0.5.13 (2020-09-07)
-------------------
* Fixed the functionality of the timeline_view

0.5.12 (2020-06-02)
-------------------
* use catkin_install_python instead of install

0.5.11 (2020-05-13)
-------------------
* add Python 3 conditional dependencies

0.5.10 (2020-04-19)
-------------------
* updated package to format 3
* added mutex and checks to fix (`#13 <https://github.com/ros-visualization/rqt_robot_monitor/issues/13>`_)

0.5.9 (2019-07-24)
------------------
* refactored code and made signaling more efficient
* stale messages appear now in the error pane

0.5.8 (2017-09-26)
------------------
* Fix apparent threading bug in timeline_view (`#5 <https://github.com/ros-visualization/rqt_robot_monitor/pull/5>`_)

0.5.7 (2017-04-26)
------------------

0.5.6 (2017-01-24)
------------------
* use Python 3 compatible syntax (`#121 <https://github.com/ros-visualization/rqt_robot_plugins/pull/121>`_)

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
* fix installing missing bag_plugin xml (`#288 <https://github.com/ros-visualization/rqt_common_plugins/issues/288>`_)

0.4.0 (2014-11-05)
------------------
* rewrite rqt_robot_monitor (`#3 <https://github.com/ros-visualization/rqt_robot_plugins/issues/3>`_, `#9 <https://github.com/ros-visualization/rqt_robot_plugins/issues/9>`_, `#32 <https://github.com/ros-visualization/rqt_robot_plugins/issues/32>`_, `#33 <https://github.com/ros-visualization/rqt_robot_plugins/issues/33>`_, `#71 <https://github.com/ros-visualization/rqt_robot_plugins/issues/71>`_)
* make diagnostics_agg a relative topic (`#32 <https://github.com/ros-visualization/rqt_robot_plugins/issues/32>`_)
* add rqt_bag plugin
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
* fix indication when not receiving deagnostic data (`#35 <https://github.com/ros-visualization/rqt_robot_plugins/issues/35>`_)
* fix scrolling of inspection window on new data (`#34 <https://github.com/ros-visualization/rqt_robot_plugins/issues/34>`_)

0.2.16 (2013-07-09)
-------------------
* First public release into Hydro

0.2.15 (2013-04-25)
-------------------

0.2.14 (2013-04-12)
-------------------

0.2.13 (2013-04-09)
-------------------

0.2.12 (2013-04-06 18:22)
-------------------------

0.2.11 (2013-04-06 18:00)
-------------------------

0.2.10 (2013-04-04)
-------------------

0.2.9 (2013-03-07)
------------------
* Fix

  * now run with pyside (it used to be not working with it w/o having been noticed).
  * Call .ui file in .ui is now successfully working

* Refactoring

  * Now TimelinePane uses .ui file

0.2.8 (2013-01-11)
------------------

0.2.7 (2012-12-23 15:58)
------------------------
* first public release into Groovy
