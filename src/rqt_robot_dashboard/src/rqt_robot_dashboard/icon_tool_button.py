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

import os

from python_qt_binding.QtCore import Signal
from python_qt_binding.QtWidgets import QToolButton
import rospy

from .util import IconHelper


class IconToolButton(QToolButton):
    """
    This is the base class for all widgets.
    It provides state and icon switching support as well as convenience functions for creating icons.

    :raises IndexError: if ``icons`` is not a list of lists of strings

    :param name: name of the object
    :type name: str
    :param icons: A list of lists of strings to create icons for the states of this button.\
    If only one is supplied then ok, warn, error, stale icons will be created with overlays

    :type icons: list
    :param clicked_icons: A list of clicked state icons. len must equal icons
    :type clicked_icons: list
    :param suppress_overlays: if false and there is only one icon path supplied
    :type suppress_overlays: bool
    :param icon_paths: list of lists of package and subdirectory in the form\
    ['package name', 'subdirectory'] example ['rqt_pr2_dashboard', 'images/svg']

    :type icon_paths: list of lists of strings
    """
    state_changed = Signal(int)

    def __init__(self, name, icons, clicked_icons=None, suppress_overlays=False, icon_paths=None):
        super(IconToolButton, self).__init__()

        self.name = name
        self.setObjectName(self.name)

        self.state_changed.connect(self._update_state)
        self.pressed.connect(self._pressed)
        self.released.connect(self._released)

        import rospkg
        icon_paths = (icon_paths if icon_paths else []) + [['rqt_robot_dashboard', 'images']]
        paths = []
        rp = rospkg.RosPack()
        for path in icon_paths:
            paths.append(os.path.join(rp.get_path(path[0]), path[1]))
        self.icon_helper = IconHelper(paths, name)
        converted_icons = self.icon_helper.set_icon_lists(icons, clicked_icons, suppress_overlays)
        self._icons = converted_icons[0]
        self._clicked_icons = converted_icons[1]

        self.setStyleSheet('QToolButton {border: none;}')

        self.__state = 0


    def update_state(self, state):
        """
        Set the state of this button.
        This will also update the icon for the button based on the ``self._icons`` list

        :raises IndexError: If state is not a proper index to ``self._icons``

        :param state: The state to set.
        :type state: int
        """
        if 0 <= state and state < len(self._icons):
            self.__state = state
            self.state_changed.emit(self.__state)
        else:
            raise IndexError("%s update_state received invalid state: %s" % (self.name, state))

    @property
    def state(self):
        """
        Read-only accessor for the widgets current state.
        """
        return self.__state

    def _update_state(self, state):
        if self.isDown():
            self.setIcon(self._clicked_icons[self.__state])
        else:
            self.setIcon(self._icons[self.__state])

    def _pressed(self):
        self.setIcon(self._clicked_icons[self.__state])

    def _released(self):
        self.setIcon(self._icons[self.__state])
