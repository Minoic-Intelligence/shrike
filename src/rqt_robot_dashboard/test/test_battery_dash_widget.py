#!/usr/bin/python

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
# * Neither the name of Willow Garage, Inc. nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Isaac Saito

import unittest

from python_qt_binding.QtWidgets import QApplication

from rqt_robot_dashboard.battery_dash_widget import BatteryDashWidget

class TestBatteryDashWidget(unittest.TestCase):
    """
    @author: Isaac Saito
    """
    _WIDGET_NAME = 'Title sample'
    _widget = None

    def setUp(self):
        unittest.TestCase.setUp(self)
        #self._item = TreenodeQstdItem(self._nodename, 0) # For unknown reason this
                                                       # stops operation.
        self._widget = BatteryDashWidget(self._WIDGET_NAME)
 
    def tearDown(self):
        #print 'Debug) in tearDown dict: {}'.format(self._widget.__dict__)

        unittest.TestCase.tearDown(self)
        del self._widget
                
    def test_update_time(self):
        val = '0.41'
        self._widget.update_time(val)

        print('toolTip={} name={}'
              .format(self._widget.toolTip(), self._widget._name))
        comp = "%s: %.2f%% remaining" % (self._WIDGET_NAME, float(val))
        tool_tip = self._widget.toolTip()
        self.assertEqual(comp, tool_tip)


if __name__ == '__main__':
    argv = ['']
    app = QApplication(argv)

    unittest.main()
