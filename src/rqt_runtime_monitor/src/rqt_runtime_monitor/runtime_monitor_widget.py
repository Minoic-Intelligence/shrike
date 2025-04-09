#!/usr/bin/env python
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
#  * Neither the name of the Willow Garage nor the names of its
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
import copy
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os
import rospkg
import threading

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QTreeWidgetItem, QWidget
from python_qt_binding.QtCore import Qt, QTimer, QObject
import rospy


class TreeItem(QObject):
    ##\param status DiagnosticsStatus : Diagnostic data of item
    ##\param tree_node wxTreeItemId : Tree ID of item in display
    def __init__(self, status, tree_node):
        super(TreeItem, self).__init__()
        self.status = status
        self.mark = False
        self.stale = False
        self.tree_node = tree_node


class RuntimeMonitorWidget(QWidget):
    def __init__(self, topic="diagnostics"):
        super(RuntimeMonitorWidget, self).__init__()
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('rqt_runtime_monitor'), 'resource', 'runtime_monitor_widget.ui')
        loadUi(ui_file, self)
        self.setObjectName('RuntimeMonitorWidget')

        self._mutex = threading.Lock()

        self._error_icon = QIcon.fromTheme('dialog-error')
        self._warning_icon = QIcon.fromTheme('dialog-warning')
        self._ok_icon = QIcon.fromTheme('dialog-information')

        self._stale_node = QTreeWidgetItem(self.tree_widget.invisibleRootItem(), ['Stale (0)'])
        self._stale_node.setIcon(0, self._error_icon)
        self.tree_widget.addTopLevelItem(self._stale_node)

        self._error_node = QTreeWidgetItem(self.tree_widget.invisibleRootItem(), ['Errors (0)'])
        self._error_node.setIcon(0, self._error_icon)
        self.tree_widget.addTopLevelItem(self._error_node)

        self._warning_node = QTreeWidgetItem(self.tree_widget.invisibleRootItem(), ['Warnings (0)'])
        self._warning_node.setIcon(0, self._warning_icon)
        self.tree_widget.addTopLevelItem(self._warning_node)

        self._ok_node = QTreeWidgetItem(self.tree_widget.invisibleRootItem(), ['Ok (0)'])
        self._ok_node.setIcon(0, self._ok_icon)
        self.tree_widget.addTopLevelItem(self._ok_node)
        self.tree_widget.itemSelectionChanged.connect(self._refresh_selection)
        self.keyPressEvent = self._on_key_press

        self._name_to_item = {}
        self._new_errors_callback = None

        self._subscriber = rospy.Subscriber(topic, DiagnosticArray, self._diagnostics_callback)

        self._previous_ros_time = rospy.Time.now()
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(1000)

        self._msg_timer = QTimer()
        self._msg_timer.timeout.connect(self._update_messages)
        self._msg_timer.start(100)

        self._messages = []
        self._used_items = 0

    def __del__(self):
        self.shutdown()
 
    def shutdown(self):
        """
        Unregisters subscriber and stops timers
        """
        self._msg_timer.stop()
        self._timer.stop()

        if rospy.is_shutdown():
            return

        if self._subscriber:
            self._subscriber.unregister()
            self._subscriber = None

    def change_diagnostic_topic(self, topic):
        """
        Changes diagnostics topic name. Must be of type diagnostic_msgs/DiagnosticArray
        """
        if not topic:
            self.reset_monitor()
            return

        if self._subscriber:
            self._subscriber.unregister()
            self._subscriber = rospy.Subscriber(str(topic), DiagnosticArray, self._diagnostics_callback)
        self.reset_monitor()

    def reset_monitor(self):
        """
        Removes all values from monitor display, resets buffers
        """
        self._name_to_item = {}  # Reset all stale topics
        self._messages = []
        self._clear_tree()

    def _clear_tree(self):
        for index in range(self._stale_node.childCount()):
            self._stale_node.removeChild(self._stale_node.child(index))
        for index in range(self._error_node.childCount()):
            self._error_node.removeChild(self._error_node.child(index))
        for index in range(self._warning_node.childCount()):
            self._warning_node.removeChild(self._warning_node.child(index))
        for index in range(self._ok_node.childCount()):
            self._ok_node.removeChild(self._ok_node.child(index))
        self._update_root_labels()

    # Diagnostics callbacks (subscriber thread)
    def _diagnostics_callback(self, message):
        with self._mutex:
            self._messages.append(message)

    # Update display of messages from main thread
    def _update_messages(self):
        with self._mutex:
            messages = self._messages[:]
            self._messages = []

        had_errors = False
        for message in messages:
            for status in message.status:
                was_selected = False
                if (status.name in self._name_to_item):
                    item = self._name_to_item[status.name]
                    if item.tree_node.isSelected():
                        was_selected = True
                    if (item.status.level == DiagnosticStatus.ERROR and status.level != DiagnosticStatus.ERROR):
                        had_errors = True
                    self._update_item(item, status, was_selected)
                else:
                    self._create_item(status, was_selected, True)
                    if (status.level == DiagnosticStatus.ERROR):
                        had_errors = True

        if (had_errors and self._new_errors_callback != None):
            self._new_errors_callback()

        self._update_root_labels()
        self.update()
        self._refresh_selection()

    def _update_item(self, item, status, was_selected):
        change_parent = False
        if (item.status.level != status.level):
            change_parent = True
        if (change_parent):
            if (item.status.level == DiagnosticStatus.OK):
                self._ok_node.removeChild(item.tree_node)
            elif (item.status.level == DiagnosticStatus.WARN):
                self._warning_node.removeChild(item.tree_node)
            elif (item.status.level == -1) or (item.status.level == DiagnosticStatus.STALE):
                self._stale_node.removeChild(item.tree_node)
            else: # ERROR
                self._error_node.removeChild(item.tree_node)

            if (status.level == DiagnosticStatus.OK):
                parent_node = self._ok_node
            elif (status.level == DiagnosticStatus.WARN):
                parent_node = self._warning_node
            elif (status.level == -1) or (status.level == DiagnosticStatus.STALE):
                parent_node = self._stale_node
            else: # ERROR
                parent_node = self._error_node

            item.tree_node.setText(0, status.name + ": " + status.message)
            item.tree_node.setData(0, Qt.UserRole, item)
            parent_node.addChild(item.tree_node)

            # expand errors automatically
            if (status.level > 1 or status.level == -1):
                parent_node.setExpanded(True)

            parent_node.sortChildren(0, Qt.AscendingOrder)

            if (was_selected):
                self.tree_widget.setCurrentItem(item.tree_node)

        else:
            item.tree_node.setText(0, status.name + ": " + status.message)

        item.status = status

        if (was_selected):
            self._fillout_info(item.tree_node)

        item.mark = True

    def _create_item(self, status, select, expand_if_error):
        if (status.level == DiagnosticStatus.OK):
            parent_node = self._ok_node
        elif (status.level == DiagnosticStatus.WARN):
            parent_node = self._warning_node
        elif (status.level == -1) or (status.level == DiagnosticStatus.STALE):
            parent_node = self._stale_node
        else: # ERROR
            parent_node = self._error_node

        item = TreeItem(status, QTreeWidgetItem(parent_node, [status.name + ": " + status.message]))
        item.tree_node.setData(0, Qt.UserRole, item)
        parent_node.addChild(item.tree_node)

        self._name_to_item[status.name] = item

        parent_node.sortChildren(0, Qt.AscendingOrder)

        if (select):
            item.tree_node.setSelected(True)

        if (expand_if_error and (status.level > 1 or status.level == -1)):
            parent_node.setExpanded(True)

        item.mark = True

        return item

    def _fillout_info(self, node):
        item = node.data(0, Qt.UserRole)
        if not item:
            return

        scroll_value = self.html_browser.verticalScrollBar().value()
        status = item.status

        s = StringIO()

        s.write("<html><body>")
        s.write("<b>Component</b>: %s<br>\n" % (status.name))
        s.write("<b>Message</b>: %s<br>\n" % (status.message))
        s.write("<b>Hardware ID</b>: %s<br><br>\n\n" % (status.hardware_id))

        s.write('<table border="1" cellpadding="2" cellspacing="0">')
        for value in status.values:
            value.value = value.value.replace("\n", "<br>")
            s.write("<tr><td><b>%s</b></td> <td>%s</td></tr>\n" % (value.key, value.value))

        s.write("</table></body></html>")

        self.html_browser.setHtml(s.getvalue())
        if self.html_browser.verticalScrollBar().maximum() < scroll_value:
            scroll_value = self.html_browser.verticalScrollBar().maximum()
        self.html_browser.verticalScrollBar().setValue(scroll_value)

    def _refresh_selection(self):
        current_item = self.tree_widget.selectedItems()
        if current_item:
            self._fillout_info(current_item[0])

    def _on_key_press(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            nodes = self.tree_widget.selectedItems()
            if (nodes != [] and nodes[0] not in (self._ok_node, self._warning_node, self._stale_node, self._error_node)):
                item = nodes[0].data(0, Qt.UserRole)
                if (item.status.level == 0):
                    self._ok_node.removeChild(item.tree_node)
                elif (item.status.level == 1):
                    self._warning_node.removeChild(item.tree_node)
                elif (item.status.level == -1) or (item.status.level == DiagnosticStatus.STALE):
                    self._stale_node.removeChild(item.tree_node)
                else:
                    self._error_node.removeChild(item.tree_node)
                del self._name_to_item[item.status.name]
            self._update_root_labels()
            self.update()
            event.accept()
        else:
            event.ignore()

    def _on_timer(self):
        if self._previous_ros_time + rospy.Duration(5) > rospy.Time.now():
            return
        self._previous_ros_time = rospy.Time.now()
        for name, item in self._name_to_item.items():
            node = item.tree_node
            if (item != None):
                if (not item.mark):
                    was_selected = False
                    selected = self.tree_widget.selectedItems()
                    if selected != [] and selected[0] == node:
                        was_selected = True

                    new_status = copy.deepcopy(item.status)
                    new_status.level = -1 # mark stale
                    self._update_item(item, new_status, was_selected)
                item.mark = False
        self._update_root_labels()
        self.update()

    def set_new_errors_callback(self, callback):
        self._new_errors_callback = callback

    def _update_root_labels(self):
        self._stale_node.setText(0, "Stale (%s)" % (self._stale_node.childCount()))
        self._error_node.setText(0, "Errors (%s)" % (self._error_node.childCount()))
        self._warning_node.setText(0, "Warnings (%s)" % (self._warning_node.childCount()))
        self._ok_node.setText(0, "Ok (%s)" % (self._ok_node.childCount()))
