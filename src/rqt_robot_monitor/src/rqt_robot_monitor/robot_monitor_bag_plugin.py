#!/usr/bin/env python
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2014, Austin Hendrix
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Austin Hendrix. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
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
# Author: Austin Hendrix


from rqt_bag.plugins.plugin import Plugin
from rqt_bag import TopicMessageView

from rqt_robot_monitor.robot_monitor import RobotMonitorWidget
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus

class RobotMonitorBagPlugin(Plugin):
    def __init__(self):
        pass

    def get_view_class(self):
        return RobotMonitorBagView

    def get_renderer_class(self):
        return None

    def get_message_types(self):
        return ['diagnostic_msgs/DiagnosticArray']

class RobotMonitorBagView(TopicMessageView):
    name = 'Diagnostics Viewer'

    def __init__(self, timeline, parent, topic):
        super(RobotMonitorBagView, self).__init__(timeline, parent, topic)
        
        self._widget = RobotMonitorWidget(parent)
        parent.layout().addWidget(self._widget)

    def message_viewed(self, bag, msg_details):
        msg = msg_details[1]
        # generic conversion of DiagnosticStatus from bag type to current type
        #  this should be fairly robust to minor changes in the message format
        status = [DiagnosticStatus(**dict((slot, getattr(m, slot)) for slot in m.__slots__)) for m in msg.status]
        msg = DiagnosticArray(msg.header, status)
        self._widget.message_updated.emit(msg)

    def close(self):
        self._widget.shutdown()  # Closes unclosed popup windows.
