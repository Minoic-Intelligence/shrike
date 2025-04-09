# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
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
#  * Neither the name of Willow Garage, Inc. nor the names of its
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
# Author: Isaac Saito

from rqt_py_common.plugin_container_widget import PluginContainerWidget
from rqt_gui_py.plugin import Plugin

from rqt_moveit.moveit_widget import MoveitWidget


class MoveitPlugin(Plugin):

    def __init__(self, plugin_context):
        super(MoveitPlugin, self).__init__(plugin_context)
        self._plugin_context = plugin_context

        self._moveit_widget = MoveitWidget(self, plugin_context)
        self.mainwidget = PluginContainerWidget(self._moveit_widget,
                                                 True, False)

        if self._plugin_context.serial_number() > 1:
            self.mainwidget.setWindowTitle(self.mainwidget.windowTitle() +
                                   (' (%d)' % plugin_context.serial_number()))

        plugin_context.add_widget(self.mainwidget)

    def get_widget(self):
        return self.mainwidget

    def shutdown_plugin(self):
        self.mainwidget.shutdown()

    def save_settings(self, plugin_settings, instance_settings):
        self.mainwidget.save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        self.mainwidget.restore_settings(plugin_settings, instance_settings)

    def _update_msg(self):
        """
        Update necessary components (per topic) regularly
        """
        self._moveit_widget.update_topic_table()
