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
# Author: Isaac Saito, Ze'ev Klapow, Austin Hendrix

from python_qt_binding.QtCore import Qt, Signal, Slot
from python_qt_binding.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget
import rospy

from rqt_robot_monitor.status_snapshot import StatusSnapshot, level_to_text
from rqt_robot_monitor.timeline_pane import TimelinePane
import rqt_robot_monitor.util_robot_monitor as util

from diagnostic_msgs.msg import DiagnosticArray


class InspectorWindow(QWidget):
    closed = Signal(str)
    _message_updated = Signal(dict)
    _queue_updated = Signal()

    def __init__(self, parent, name, timeline):
        """
        :param name: Name of inspecting diagnostic status
        :param timeline: Timeline object from which a status is fetched
        """
        #TODO(Isaac) UI construction that currently is done in this method,
        #            needs to be done in .ui file.
        super(InspectorWindow, self).__init__(parent=parent)
        self.setWindowTitle(name)
        self._name = name

        self.layout_vertical = QVBoxLayout(self)

        self.disp = StatusSnapshot(parent=self)

        self.layout_vertical.addWidget(self.disp, 1)

        self._message_updated_processing = False
        self._queue_updated_processing = False

        self.timeline = timeline
        self.timeline.message_updated.connect(
            self.message_updated, Qt.DirectConnection)
        self.timeline.queue_updated.connect(
            self.queue_updated, Qt.DirectConnection)
        self._message_updated.connect(
            self._signal_message_updated, Qt.QueuedConnection)
        self._queue_updated.connect(
            self._signal_queue_updated, Qt.QueuedConnection)

        self.timeline_pane = TimelinePane(self, self.timeline.paused)
        self.timeline_pane.pause_changed.connect(self.timeline.set_paused)
        self.timeline_pane.position_changed.connect(self.timeline.set_position)
        self.timeline.pause_changed.connect(self.timeline_pane.set_paused)
        self.timeline.position_changed.connect(self.timeline_pane.set_position)
        self.layout_vertical.addWidget(self.timeline_pane, 0)

        self.snapshot = QPushButton("Snapshot")
        self.snapshot.clicked.connect(self._take_snapshot)
        self.layout_vertical.addWidget(self.snapshot)

        self.snaps = []

        self.setLayout(self.layout_vertical)
        # TODO better to be configurable where to appear.
        self.resize(400, 600)

    def closeEvent(self, event):
        """ called when this window is closed

        Calls close on all snapshots, and emits the closed signal
        """
        # TODO: are snapshots kept around even after they're closed?
        #       this appears to work even if the user closes some snapshots,
        #       and they're still left in the internal array
        for snap in self.snaps:
            snap.close()
        self.closed.emit(self._name)

    @Slot()
    def queue_updated(self):
        """
        This method just calls _signal_queue_updated in 'best effort' manner.
        This method should be called by signal with DirectConnection.
        """
        if self._queue_updated_processing:
            return
        self._queue_updated_processing = True
        self._queue_updated.emit()

    @Slot()
    def _signal_queue_updated(self):
        # update timeline pane
        # collect worst status levels for each history
        status = self.timeline.get_all_status_by_name(self._name)
        if status is not None:
            self.timeline_pane.set_levels([s.level for s in status])
            self.timeline_pane.redraw.emit()
            self._queue_updated_processing = False

    @Slot(dict)
    def message_updated(self, status):
        """
        This method just calls _signal_message_updated in 'best effort' manner.
        This method should be called by signal with DirectConnection.
        """
        if self._message_updated_processing:
            return
        self._message_updated_processing = True
        self._message_updated.emit(status)

    @Slot(dict)
    def _signal_message_updated(self, status):
        rospy.logdebug('InspectorWin message_updated')

        try:
            status = status[self._name]
        except:
            return

        scroll_value = self.disp.verticalScrollBar().value()

        self.status = status
        self.disp.write_status.emit(status)

        if self.disp.verticalScrollBar().maximum() < scroll_value:
            scroll_value = self.disp.verticalScrollBar().maximum()
        self.disp.verticalScrollBar().setValue(scroll_value)
        self._message_updated_processing = False

    def _take_snapshot(self):
        snap = StatusSnapshot(status=self.status)
        self.snaps.append(snap)
