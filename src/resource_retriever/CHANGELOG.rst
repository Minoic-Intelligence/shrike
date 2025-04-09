^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package resource_retriever
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.12.8 (2025-02-13)
-------------------
* Allow spaces (`#85 <https://github.com/ros/resource_retriever/issues/85>`_)
* Drop old C++ standard (`#73 <https://github.com/ros/resource_retriever/issues/73>`_)
* On Windows install .dll libraries in <prefix>/bin (`#91 <https://github.com/ros/resource_retriever/issues/91>`_)
* Make importing the library fast (`#87 <https://github.com/ros/resource_retriever/issues/87>`_)
* Contributors: Jochen Sprickerhof, Silvio Traversaro, Simon Schmeisser, Yuki Furuta

1.12.7 (2021-12-06)
-------------------
* Split curl dependency to avoid dev package at runtime (`#67 <https://github.com/ros/resource_retriever/issues/67>`_)
* Contributors: Scott K Logan

1.12.6 (2020-02-14)
-------------------
* Bump CMake version to avoid CMP0048 warning (`#37 <https://github.com/ros/resource_retriever/issues/37>`_)
* Contributors: Shane Loretz

1.12.5 (2019-09-11)
-------------------
* Update the exec_depend keys for Python 3. (`#29 <https://github.com/ros/resource_retriever/issues/29>`_)
* point to the ros/resource_retriever repository (`#28 <https://github.com/ros/resource_retriever/issues/28>`_)
* append trailing zero to memory buffer, to allow safe use as char* (`#27 <https://github.com/ros/resource_retriever/issues/27>`_)
* Contributors: Chris Lalancette, Mikael Arguedas, Robert Haschke

1.12.4 (2018-03-19)
-------------------
* Fix an intermittent test failure.
  Both the C++ and python tests were using test/large_file.dat,
  which means if they were run concurrently, they would sometimes
  collide.  Avoid this by having them use different filenames.
* Cleanup resource_retriever packaging.
  In particular, make sure that resource_retriever properly
  depends on all of the things it needs.  While we are in here,
  switch over to package xml version 2.
* Contributors: Chris Lalancette

1.12.3 (2017-03-27)
-------------------
* Fix C++11 to use set_directory_properties
* Make Shane and Chris the maintainers.
* Python3 compatibility (`#10 <https://github.com/ros/resource_retriever/issues/10>`_)
  * Replace urlgrabber with urllib[2]
  As urlgrabber is not supported for Python 3 replace it with either the built-in urllib (Python 2) or urllib2 (Python 3)
  * Use rospkg instead of system call for rospack
  * Add test for python functionality
  * Fix rospkg dependency definition
* Update URL in http test to something which exists (`#8 <https://github.com/ros/resource_retriever/issues/8>`_)
  * Update URL in http test to something which exists
* Contributors: Chris Lalancette, Mike Purvis, Ruben Smits

1.12.2 (2016-06-10)
-------------------
* fix failing build due to cmake error (`#6 <https://github.com/ros/resource_retriever/issues/6>`_)
* Contributors: Jackie Kay

1.12.1 (2016-06-10)
-------------------
* Fix warnings in test (`#5 <https://github.com/ros/resource_retriever/issues/5>`_)
  add spaces around ROS_PACKAGE_NAME
* Merge pull request `#4 <https://github.com/ros/resource_retriever/issues/4>`_ from DLu/kinetic-devel
  Add c++11 flag
* Contributors: David V. Lu!!, Jackie Kay, Steven Peters

1.12.0 (2016-03-23)
-------------------
* resource_retriever: adding missing dep
  Using the python resource_retriever requires the `python-urlgrabber` system dependency: http://rosindex.github.io/d/python-urlgrabber/
* Contributors: Jonathan Bohren

1.11.6 (2014-11-30)
-------------------

1.11.5 (2014-07-24)
-------------------

1.11.4 (2014-07-07)
-------------------

1.11.3 (2014-06-24)
-------------------

1.11.2 (2014-03-22)
-------------------

1.11.1 (2014-03-20)
-------------------

1.11.0 (2014-02-21)
-------------------

1.10.18 (2013-12-04)
--------------------
* add DEPENDS for kdl_parser
* Contributors: Ioan Sucan

1.10.16 (2013-11-18)
--------------------
* check for CATKIN_ENABLE_TESTING

1.10.15 (2013-08-17)
--------------------

* resource_retriever: install python package using setup.py
