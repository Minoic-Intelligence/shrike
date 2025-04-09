^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rqt_rviz
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.7.0 (2021-06-22)
------------------
* Fixup catkin_lint issues
* Update maintainers
* Correctly update window title with context serial no
* Notice changes of display config file
* Find quit action by name
* Suppress rviz splash screen
* fix shebang line for python3 (`#14 <https://github.com/ros-visualization/rqt_rviz/issues/14>`_)
* Contributors: Mikael Arguedas, Robert Haschke

0.6.1 (2020-05-12)
------------------
* Noetic release (`#11 <https://github.com/ros-visualization/rqt_rviz/issues/11>`_)
  * Bump CMake version to avoid CMP0048 warning
  * Use setuptools instead of distutils
* Use std::vector for variable length arrays. (`#10 <https://github.com/ros-visualization/rqt_rviz/issues/10>`_)
  * Use std::vector for variable length arrays. (`#3 <https://github.com/ros-visualization/rqt_rviz/issues/3>`_)
  Some compiler doesn't support variable length arrays feature like G++. Rework the code to use std::vector instead for between cross-compiling.
  * Fix build break in CI.
* Contributors: Alejandro Hernández Cordero, Sean Yen [MSFT]

0.6.0 (2018-06-27)
------------------
* Indigo -> Lunar
* Contributors: chapulina

0.5.10 (2018-06-27)
-------------------
* Config file for the plugin and hide_menu saving
* Contributors: Sammy Pfeiffer, chapulina

0.5.9 (2018-05-03)
------------------

0.5.8 (2017-05-02)
------------------
* Qt5 widgets bugfix (`#4 <https://github.com/ros-visualization/rqt_rviz/issues/4>`_)
  * add qtbase to dependency list
  * find widgets as components rather than package
* Contributors: Mikael Arguedas

0.5.7 (2017-04-27)
------------------

0.5.6 (2017-01-24)
------------------

0.5.5 (2016-11-02)
------------------

0.5.4 (2016-09-19)
------------------
* mark rviz plugin as experimental since it has severe issues for while

0.5.3 (2016-05-16)
------------------

0.5.2 (2016-04-29)
------------------
* fix using Qt 5 when rqt uses it

0.5.1 (2016-04-28)
------------------

0.5.0 (2016-04-27)
------------------

0.4.3 (2016-03-08)
------------------
* disable ogre-log by default, add command line option to enable it (fix `#95 <https://github.com/ros-visualization/rqt_robot_plugins/issues/95>`_)

0.4.2 (2015-07-24)
------------------

0.4.1 (2015-04-30)
------------------

0.4.0 (2014-11-05)
------------------
* update script to use full plugin name

0.3.7 (2014-08-18)
------------------
* fix argument parsing (`#68 <https://github.com/ros-visualization/rqt_robot_plugins/issues/68>`_) (regression of 0.3.5)

0.3.6 (2014-07-11)
------------------

0.3.5 (2014-06-02)
------------------
* fix compilation on OS X (`#64 <https://github.com/ros-visualization/rqt_robot_plugins/issues/64>`_)

0.3.4 (2014-05-07)
------------------
* add menu hiding and config as command-line args (`#62 <https://github.com/ros-visualization/rqt_robot_plugins/pull/62>`_)

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

0.2.8 (2013-01-11)
------------------

0.2.7 (2012-12-23 15:58)
------------------------
* restore rviz plugin and add it to metapackage (that was done in 0.2.6)
* first public release for Groovy
