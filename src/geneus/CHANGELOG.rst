^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package geneus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3.0.0 (2020-01-27)
------------------

* **CAUTION** This version will not work on 14.04, If you want to run on 14.04 due to bump CMake version to avoid CMP0048 warning
  Use `cmake_minimum_required(VERSION 2.8.3)` for CMakeLists.txt

* [generate.py] add feature to write const to string (`#13 <https://github.com/jsk-ros-pkg/geneus/issues/13>`_)
* update geneus for 20.04 / Noetic (`#69 <https://github.com/jsk-ros-pkg/geneus/issues/69>`_)

  * from __future_\_ import print_function is required for python2
  * Python 3 suppoort. Generated using 2to3
  * Use setuptools instead of distutils
  * Make setup.py not executable
  * Drop trusty/indigo from CI
  * Bump CMake version to avoid CMP0048 warning
  * add test to run ubuntu/focal and debian/stable
  * run rosdep update with --incldue-eol-distros for indigo

* fix bug of write_constants (`#62 <https://github.com/jsk-ros-pkg/geneus/issues/52>`_)

  * add test to check `#59 <https://github.com/jsk-ros-pkg/geneus/issues/59>`_

* fix wrongly commited in #61 (`#63 <https://github.com/jsk-ros-pkg/geneus/issues/63>`_)

  * .travis: catkin build needs to run with geneus first, befor compiling std_msgs
  * .travis.sh: fix script errors with ¥ == -> ¥
  * copy std_msgs repository for geneus test codes
  * .travis.sh: add comments
  * fix https://github.com/jsk-ros-pkg/geneus/pull/61/commits/ef9868e4e621297449e5931453fbe4582a542ca4
  * fix wrongly commited in #61

* add test to check #56 case (`#61 <https://github.com/jsk-ros-pkg/geneus/issues/61>`_)

  * generate.py change generator for field_type == bool
  * remove unnecessary (ros::load-ros-manifeset 'euslisp')
    [ WARN] [1547033310.743978735]: Calling (load-ros-manifest euslisp) for the package without msg/srv will be deprecated
    [ WARN] [1547033310.744036587]: ACTION REQUIRED
    [ WARN] [1547033310.744049863]:  Use (load-ros-{package,msg,srv} pkg) for the dependent packages with msg/srv
    [ WARN] [1547033310.744059431]:  See https://github.com/jsk-ros-pkg/jsk_robot/issues/823
  * add test to check #56 case
  * add test/test-geneus.test from roseus package

* run test-geneus.test within geneus package (`#60 <https://github.com/jsk-ros-pkg/geneus/issues/60>`_)

  * run rostest geneus test-geneus.test
  * move test/{test-geneus.test,test-geneus.l,test_geneus_send_msgs.py} from roseus package

* add melodic test (`#58 <https://github.com/jsk-ros-pkg/geneus/issues/58>`_)

  * install tzdata with non-interactive mode
  * add melodic

* when array_len is nil, do not run dotimes..., see https://github.com/jsk-ros-pkg/jsk_roseus/issues/544 (`#55 <https://github.com/jsk-ros-pkg/geneus/issues/55>`_)

* add test kinetic on travis(`#54 <https://github.com/jsk-ros-pkg/geneus/issues/54>`_)

  * pr2_controllers_msgs is not released on kinetic and that's ok for geneus test

* need to use system python, with travis-python, we can not find python modeule install by ap (`#53 <https://github.com/jsk-ros-pkg/geneus/issues/53>`_)
  https://github.com/jsk-ros-pkg/jsk_3rdparty/pull/117

* Contributors: Kei Okada, Markus Grimm, Shane Loretz, Taichi Higashide

2.2.6 (2017-05-22)
------------------
* [geneus_main.py] suppress warning (`#52 <https://github.com/jsk-ros-pkg/geneus/issues/52>`_)
  * [geneus_main.py] do not write timestamp that makes different md5
  * [geneus_main.py] write depends by alphabetical order in manifest.l
* [.travis.yml] : add jade test  (`#49 <https://github.com/jsk-ros-pkg/geneus/issues/49>`_)
  * .travis.yml: add BUILDER=catkin_make_isolated
  * .travis.yml: add indigo/jade and catkin_make/catkin test
* [geneus_main.py]: add comment : 152683d depends on comment line (`#44 <https://github.com/jsk-ros-pkg/geneus/issues/44>`_)
* Contributors: Yuki Furuta, Kei Okada

2.2.5 (2015-11-21)
------------------
* add status badge to the README.md (`#41 <https://github.com/jsk-ros-pkg/geneus/issues/41>`_ )
* .travis.yml: use before_script and script
* .travis.yml: rosdep install with -q (quiet)

* Use package.xml in workspace, not deb installed one (`#42 <https://github.com/jsk-ros-pkg/geneus/issues/42>`_ )
  
  * do not overwrite pkg_map
  * add test code to check `#42 <https://github.com/jsk-ros-pkg/geneus/issues/42>`_ isseus
  * geneus_main.py: fix THIS FILE IS AUTOMAATICALLY GENERATED... comment
  * use latest released code

* use indiog/14.04 on travis test `#40 <https://github.com/jsk-ros-pkg/geneus/issues/40>`_ 

  * add ppa:openrave/release
  * default-ri-test.launch ->default-ri-test.test
  * install default python, use language:generic
  * ros_comm message has been move to ros_comm_msgs
  * use indigo/14.04

* Contributors: Kei Okada

2.2.4 (2015-07-08)
------------------
* [src/geneus/generate.py] bool array is list, not lisp-array
* [src/geneus/generate.py] use list for time type object
* src/geneus/generate.py fix for variable bool array case, https://github.com/jsk-ros-pkg/jsk_roseus/pull/330
* [package.xml] Now doesn't depend on python-rospkg
* Contributors: Kei Okada, Kentaro Wada

2.2.3 (2015-06-19)
------------------
* [src/geneus/geneus_main.py] Call get_pkg_map if pkg_map is None
* Contributors: Kentaro Wada

2.2.2 (2015-06-01)
------------------
* [.travis.yml] add pr2eus test
* [src/geneus/generate.py] make intern before shadow, see https://github.com/jsk-ros-pkg/jsk_roseus/issues/313
* [geneus_main.py] has_key -> in
* [geneus_main.py] generate message even if geneus is not found
* Contributors: Kei Okada, Kentaro Wada

2.2.1 (2015-04-24)
------------------
* [geneus_main.py] fix when pkg_map does not have geneus
* [geneus_main.py] Fix unexpected function resposes caused by python gabage collection algorightm
* [geneus_main.py] fix typo for warning
* [geneus_main.py] Yellow color for warnings
* Contributors: Kei Okada, Kentaro Wada

2.2.0 (2015-04-21)
------------------

* [generate.py] load roseus-add-msgs for srv too
* [geneus_main.py] add timestamp message to manifest.l

* [geneus_main.py] message loding problem https://github.com/start-jsk/2014-semi/issues/196, https://github.com/jsk-ros-pkg/jsk_roseus/issues/257

  * [geneus_main.py] gen msg/srv does not need get_pkg_map
  * [geneus_main.py] fix comment and messages
  * [geneus_main.py] use topological_order instaed of rearrange_depends
  * [geneus_main.py] use catkin as a substitute for rospkg
  * [geneus_main.py] see only run_depend in package.xml
  * [geneus_main.py] Resolve package dependencies with attention to the order

* [geneus] treat uint8[] as string like rospy https://github.com/jsk-ros-pkg/geneus/issues/14
  * [generate.py] fixed version of `#15 <https://github.com/jsk-ros-pkg/geneus/issues/15>`_ which did not pass test at  https://github.com/jsk-ros-pkg/jsk_roseus/pull/276
* [geneus_main.py] fix pakcage_dpeneds, to solve https://github.com/start-jsk/2014-semi/issues/196 issue
* [.travis.yml] use latest version of travis test
* [.travis.yml] use latest catkin for --no-jobserver option
* [.travis.yml] Add after failure
* [.gitignore] initial commit

* Contributors: Yuki Furuta Kei Okada, Kentaro Wada

2.1.2 (2015-02-25)
------------------
* [.travis.yml] remove hot-fix code
* fix not to use get_depends, which cause eerror when the package is not installed
* [package.xml] forget to add python-rospkg
* Contributors: Kei Okada

2.1.1 (2015-02-21)
------------------
* [geneus_main.py] use rospack to find build(only package have msg/src) dependency
* [.travis.yml] add test code to check work with roseus
* [src/geneus/geneus_main.py] add comments
* fix ros::load-ros-package order by dependencies
* Contributors: Kei Okada, Yuki Furuta

2.1.0 (2015-02-12)
------------------
* fix message generation for uint8(char)/int8(byte) (#4,#6)
* Contributors: Kei Okada

2.0.1 (2015-02-10)
------------------
* [scripts/gen_eus.py] set executable
* Contributors: Kei Okada

1.0.0 (2015-01-06)
------------------

0.1.0 (2014-10-02)
------------------
* rewrite everything only depends on genmsg
* Contributors: Kei Okada

