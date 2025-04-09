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

from python_qt_binding.QtCore import QMutex, QMutexLocker, QSize
from rqt_nav_view.nav_view import NavViewWidget

from .icon_tool_button import IconToolButton


class NavViewDashWidget(IconToolButton):
    """
    A widget which launches a nav_view widget in order to view and interact with the ROS nav stack

    :param context: The plugin context in which to dsiplay the nav_view, ''qt_gui.plugin_context.PluginContext''
    :param name: The widgets name, ''str''
    """
    def __init__(self, context, name='NavView', icon_paths=None):
        self._icons = [['bg-grey.svg', 'ic-navigation.svg']]
        super(NavViewDashWidget, self).__init__(name, icons=self._icons, suppress_overlays=True, icon_paths=icon_paths)
        self.context = context
        self.update_state(0)
        self.setFixedSize(self._icons[0].actualSize(QSize(50, 30)))

        self._navview = None
        self._navview_shown = False
        self.clicked.connect(self._show_navview)
        self._show_mutex = QMutex()

    def _show_navview(self):
        with QMutexLocker(self._show_mutex):
            if self._navview is None:
                self._navview = NavViewWidget()
            try:
                if self._navview_shown:
                    self.context.remove_widget(self._navview)
                    self._navview_shown = not self._navview_shown
                else:
                    self.context.add_widget(self._navview)
                    self._navview_shown = not self._navview_shown
            except Exception:
                self._navview_shown = not self._navview_shown
                self._show_navview()

    def shutdown_widget(self):
        if self._navview:
            self._navview.close()

    def save_settings(self, plugin_settings, instance_settings):
        self._navview.save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        self._navview.restore_settings(plugin_settings, instance_settings)
