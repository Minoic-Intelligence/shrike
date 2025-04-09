^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rospack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.6.2 (2020-05-13)
------------------
* fix umask for rospack cache files, regression from 2.5.4 (`#119 <https://github.com/ros/rospack/issues/119>`_)

2.6.1 (2020-04-06)
------------------
* best effort output on error (`#113 <https://github.com/ros/rospack/issues/113>`_)

2.6.0 (2020-03-02)
------------------
* declare specific boost dependencies (`#115 <https://github.com/ros/rospack/issues/115>`_)

2.5.5 (2020-01-24)
------------------
* bump to CMake 3.0.2 to avoid CMP0048 warning (`#114 <https://github.com/ros/rospack/issues/114>`_)
* only depend on catkin_pkg/rosdep-modules (`#109 <https://github.com/ros/rospack/issues/109>`_)
* rework validateCache for portability. (`#108 <https://github.com/ros/rospack/issues/108>`_)

2.5.4 (2019-10-03)
------------------
* use condition attributes to specify Python 2 and 3 dependencies (`#107 <https://github.com/ros/rospack/issues/107>`_)
* for fixing potential TOCTOU issue (`#104 <https://github.com/ros/rospack/issues/104>`_)
* fixing mkstemp without securely setting mask/unmask (`#106 <https://github.com/ros/rospack/issues/106>`_)
* fixing code unreachable (`#105 <https://github.com/ros/rospack/issues/105>`_)

2.5.3 (2019-03-04)
------------------
* enable to run rosstack depends for wetpackages (`#91 <https://github.com/ros/rospack/issues/91>`_)

2.5.2 (2018-09-05)
------------------
* add delete whitespace settings for backward compatibility, regression from 2.4.0 (`#94 <https://github.com/ros/rospack/issues/94>`_)
* fix build issue on Windows (`#90 <https://github.com/ros/rospack/issues/90>`_)
* use namespace to avoid name conflict between tinyxml2 and msxml (`#89 <https://github.com/ros/rospack/issues/89>`_)

2.5.1 (2018-05-31)
------------------
* add run_depend on ros_environment (`#88 <https://github.com/ros/rospack/issues/88>`_)

2.5.0 (2018-01-30)
------------------
* skip warning if permission to read directory was denied (`#87 <https://github.com/ros/rospack/issues/87>`_)

2.4.3 (2017-10-12)
------------------
* add README.md with notes about tinyxml2 (`#82 <https://github.com/ros/rospack/issues/82>`_)
* replace references to deprecated Boost.TR1 (`#80 <https://github.com/ros/rospack/issues/80>`_)
* fix Python.h redefining pre-processor definitions (`#78 <https://github.com/ros/rospack/issues/78>`_)

2.4.2 (2017-07-27)
------------------

2.4.1 (2017-02-27)
------------------
* fix inverted result code check, regression from 2.4.0 (`#70 <https://github.com/ros/rospack/issues/70>`_)

2.4.0 (2017-02-22)
------------------
* make some deps* functions public (`#65 <https://github.com/ros/rospack/pull/65>`_)
* switch from TinyXML to TinyXML2 (`#62 <https://github.com/ros/rospack/pull/62>`_)

2.3.2 (2017-02-14)
------------------
* add license field in Stackage class (`#66 <https://github.com/ros/rospack/issues/66>`_)

2.3.1 (2016-09-02)
------------------
* fix FTBFS on hurd-i386 (`#64 <https://github.com/ros/rospack/issues/64>`_)

2.3.0 (2016-03-09)
------------------
* allow caching of rospack results (`#49 <https://github.com/ros/rospack/issues/49>`_)
* fix memory leak in Rosstackage::addStackage (`#59 <https://github.com/ros/rospack/issues/59>`_)
* return false in depsOnDetail if the package name in rospack plugins can not be found (`#51 <https://github.com/ros/rospack/issues/51>`_)
* #undef symbols before #defining them to avoid preprocessor warnings in the case that they were already #defined (`#50 <https://github.com/ros/rospack/issues/50>`_)

2.2.5 (2014-09-04)
------------------
* support tags defined in package format 2 (`#43 <https://github.com/ros/rospack/issues/43>`_)

2.2.4 (2014-07-10)
------------------
* fix find_package(PythonLibs ...) with CMake 3 (`#42 <https://github.com/ros/rospack/issues/42>`_)

2.2.3 (2014-05-07)
------------------
* find library for exact Python version (even if not in CMake provided list of version numbers) (`#40 <https://github.com/ros/rospack/issues/40>`_)
* find TinyXML using cmake_modules (`#24 <https://github.com/ros/rospack/issues/24>`_)
* make error messages tool specific (rospack vs. rosstack) (`#38 <https://github.com/ros/rospack/issues/38>`_)

2.2.2 (2014-02-25)
------------------
* python 3 compatibility (`#35 <https://github.com/ros/rospack/issues/35>`_)

2.2.1 (2014-02-24)
------------------
* only perform backquote substitution when needed (`#34 <https://github.com/ros/rospack/issues/34>`_)

2.2.0 (2014-01-30)
------------------
* add hash of ROS_PACKAGE_PATH to rospack/rosstack cache filename, remove ROS_ROOT from cache (`#28 <https://github.com/ros/rospack/issues/28>`_)

2.1.22 (2014-01-07)
-------------------
* use specific python version catkin has decided on (`#29 <https://github.com/ros/rospack/issues/29>`_)
* python 3 compatibility (`#25 <https://github.com/ros/rospack/issues/25>`_, `#27 <https://github.com/ros/rospack/issues/27>`_)
* fall back gracefully whe gtest is not available
* update package urls

2.1.21 (2013-07-05)
-------------------
* honor CATKIN_IGNORE marker file when crawling for packages (`#21 <https://github.com/ros/rospack/issues/21>`_)

2.1.20 (2013-07-03)
-------------------
* improve error message to include package names when circular dependency is detected (`#18 <https://github.com/ros/rospack/issues/18>`_)
* check for CATKIN_ENABLE_TESTING to enable configure without tests
* add '-h' option

2.1.19 (2013-06-06)
-------------------
* modified command 'list-duplicates' to output the paths where the packages were found (`#3 <https://github.com/ros/rospack/issues/3>`_)
* modified 'rospack plugins' to not use rosdep (`#5 <https://github.com/ros/rospack/issues/5>`_)
* improve Windows support  (`#10 <https://github.com/ros/rospack/issues/10>`_)
* use find_package() for tinyxml (if available)

2.1.18 (2013-03-21)
-------------------
* invert order of package type detection (dry before wet) (`ros-infrastructure/rospkg#30 <https://github.com/ros-infrastructure/rospkg/issues/30>`_)

2.1.17 (2013-03-08)
-------------------
* output full pkg-config command in case of errors (`#8 <https://github.com/ros/rospack/issues/8>`_)
* handle None as return value for call_pkg_config (`#8 <https://github.com/ros/rospack/issues/8>`_)
* fix crawling to always recrawl when forced (`#9 <https://github.com/ros/rospack/issues/9>`_)

2.1.16 (2013-01-13)
-------------------
* fix segfault for command depends1 which ignores exceptions and calls isSysPackage again (`#4 <https://github.com/ros/rospack/issues/4>`_)

2.1.15 (2012-12-06)
-------------------
* first public release for Groovy
