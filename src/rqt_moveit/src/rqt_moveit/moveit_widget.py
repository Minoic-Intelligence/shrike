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

import os
import sys
import threading

from python_qt_binding import loadUi
from python_qt_binding.QtCore import QModelIndex, QTimer, Signal
from python_qt_binding.QtGui import QStandardItem, QStandardItemModel
from python_qt_binding.QtWidgets import QWidget
import rospkg
import rospy
from rqt_py_common.rqt_roscomm_util import RqtRoscommUtil
from rqt_topic.topic_widget import TopicWidget
try:
    # Python 2
    from xmlrpclib import ServerProxy as XMLServerProxy
except ModuleNotFoundError:
    # Python 3
    from xmlrpc.client import ServerProxy as XMLServerProxy


class MoveitWidget(QWidget):
    """
    This Widget provides an overview about the presence of different parts of a running moveIt instance.
    """
    # To be connected to PluginContainerWidget
    sig_sysmsg = Signal(str)
    sig_param = Signal(bool, str)  # param name emitted
    sig_node = Signal(bool, str)  # node name emitted
    sig_topic = Signal(list)  # topic name emitted

    _SPLITTER_H = 'splitter_horizontal'

    def __init__(self, parent, plugin_context):
        """
        @type parent: MoveitMain
        """

        self._ros_master = XMLServerProxy(os.environ['ROS_MASTER_URI'])
        self._stop_event = threading.Event()

        self._nodes_monitored = ['/move_group']
        self._selected_topics = [('/pointcloud', 'sensor_msgs/PointCloud'),
                                 ('/pointcloud2', 'sensor_msgs/PointCloud2'),
                                 ('/image', 'sensor_msgs/Image'),
                                 ('/camera_info', 'sensor_msgs/CameraInfo')]
        self._params_monitored = ['/robot_description',
                                  '/robot_description_semantic']

        super(MoveitWidget, self).__init__()
        self._parent = parent
        self._plugin_context = plugin_context
        self._refresh_rate = 5  # With default value

        self._rospack = rospkg.RosPack()
        ui_file = os.path.join(self._rospack.get_path('rqt_moveit'),
                               'resource', 'moveit_top.ui')
        loadUi(ui_file, self, {'TopicWidget': TopicWidget})

        # Custom widget classes don't show in QSplitter when they instantiated
        # in .ui file and not explicitly added to QSplitter like this. Thus
        # this is a workaround.
        self._splitter.addWidget(self._widget_topic)

        self._spinbox_refreshrate.valueChanged.connect(self._update_refreshrate)

        # Show default ref rate on QSpinbox
        self._spinbox_refreshrate.setValue(self._refresh_rate)

        # Monitor node
        self._node_qitems = {}
        self._node_monitor_thread = self._init_monitor_nodes()
        self._node_monitor_thread.start()

        # topic to show
        self._registered_topics = None
        self._topic_monitor_thread = self._init_monitor_topics()
        self._topic_monitor_thread.start()

        # Init monitoring parameters.
        self._param_qitems = {}
        _col_names_paramtable = ['Param name', 'Found on Parameter Server?']
        self._param_check_thread = self._init_monitor_parameters(_col_names_paramtable)
        self._param_check_thread.start()

    def _init_monitor_nodes(self):
        """
        @rtype: Thread
        """
        self._node_datamodel = QStandardItemModel(0, 2)
        self._root_qitem = self._node_datamodel.invisibleRootItem()
        self._view_nodes.setModel(self._node_datamodel)

        node_monitor_thread = threading.Thread(target=self._check_nodes_alive,
                                     args=(self.sig_node, self._nodes_monitored, self._stop_event))

        self.sig_node.connect(self._update_output_nodes)
        return node_monitor_thread

    def _check_nodes_alive(self, signal, nodes_monitored, stop_event):
        """
        Working as a callback of Thread class, this method keeps looping to
        watch if the nodes whose names are passed exist and emits signal per
        each node.

        Notice that what MoveitWidget._check_nodes_alive &
        MoveitWidget._check_params_alive do is very similar, but since both of
        them are supposed to be passed to Thread class, there might not be
        a way to generalize these 2.

        @param signal: Signal(bool, str)
        @type nodes_monitored: str[]
        @type stop_event: Event()
        """
        rosnode_dynamically_loaded = __import__('rosnode')
        while True:
            for nodename in nodes_monitored:
                try:
                    registered_nodes = rosnode_dynamically_loaded.get_node_names()
                    is_node_running = nodename in registered_nodes

                except rosnode_dynamically_loaded.ROSNodeIOException as e:
                    # TODO: Needs to be indicated on GUI
                    # (eg. PluginContainerWidget)
                    is_node_running = False

                signal.emit(is_node_running, nodename)
                rospy.logdebug('_update_output_nodes')
            if stop_event.wait(self._refresh_rate):
                del rosnode_dynamically_loaded
                return

    def _init_monitor_topics(self):
        """
        @rtype: Thread
        """
        topic_monitor_thread = threading.Thread(target=self._check_topics_alive,
                                      args=(self.sig_topic, self._selected_topics, self._stop_event))
        self.sig_topic.connect(self._update_output_topics)
        return topic_monitor_thread

    def _check_topics_alive(self, signal, topics_monitored, stop_event):
        """
        Working as a callback of Thread class, this method keeps looping to
        watch if the topics whose names are passed exist and emits signal per
        each node.

        @param signal: Signal()
        @type topics_monitored: str[]
        @type stop_event: Event()
        """
        while True:
            try:
                code, msg, val = self._ros_master.getPublishedTopics('/rqt_moveit_update_script', "")
                if code == 1:
                    published_topics = dict(val)
                else:
                    rospy.logerr("Communication with rosmaster failed")
            except:
                rospy.logerr("Communication with rosmaster failed")

            registered_topics = []
            for topic in topics_monitored:
                if topic[0] in published_topics and topic[1] == published_topics.get(topic[0]):
                    registered_topics.append((topic[0], published_topics.get(topic[0])))

            signal.emit(list(registered_topics))
            rospy.logdebug('_update_output_topics')
            if stop_event.wait(self._refresh_rate):
                return

    def _init_monitor_parameters(self, _col_names_paramtable=None):
        """
        @rtype: Thread
        """

        self._param_datamodel = QStandardItemModel(0, 2)
        self._root_qitem = self._param_datamodel.invisibleRootItem()
        self._view_params.setModel(self._param_datamodel)

        # Names of header on the QTableView.
        if not _col_names_paramtable:
            _col_names_paramtable = ['Param name',
                                     'Found on Parameter Server?']
        self._param_datamodel.setHorizontalHeaderLabels(_col_names_paramtable)

        self.sig_param.connect(self._update_output_parameters)

        param_check_thread = threading.Thread(target=self._check_params_alive,
                                    args=(self.sig_param, self._params_monitored, self._stop_event))
        return param_check_thread

    def _update_output_nodes(self, is_node_running, node_name):
        """
        Slot for signals that tell nodes existence.

        @type is_node_running: bool
        @type node_name: str
        """
        # TODO: What this method does is exactly the same with
        # monitor_parameters. Unify them.

        rospy.logdebug('is_node_running={} par_name={}'.format(is_node_running, node_name))
        node_name = str(node_name)
        node_qitem = None
        if node_name not in self._node_qitems:
            node_qitem = QStandardItem(node_name)
            self._node_qitems[node_name] = node_qitem
            self._node_datamodel.appendRow(node_qitem)
        else:  # qsitem with the node name already exists.
            node_qitem = self._node_qitems[str(node_name)]

        qindex = self._node_datamodel.indexFromItem(node_qitem)
        _str_node_running = 'Not running'
        if is_node_running:
            _str_node_running = 'Running'
        qitem_node_status = QStandardItem(_str_node_running)
        self._node_datamodel.setItem(qindex.row(), 1, qitem_node_status)

    def _update_output_topics(self, registered_topics):
        """
        Slot for signals that tell topic's existence.

        @type registered_topics: list
        """
        # This branch will cause that once a selected topic was found the topic view will
        # never be empty again.
        if len(registered_topics) > 0:

            if self._registered_topics is None:
                self._widget_topic.set_selected_topics(registered_topics)
                self._widget_topic.set_topic_specifier(TopicWidget.SELECT_BY_NAME)
                self._widget_topic.start()
            elif self._registered_topics is not None and set(self._registered_topics) != set(registered_topics):
                self._widget_topic.set_selected_topics(registered_topics)

            self._registered_topics = registered_topics

    def _check_params_alive(self, signal, params_monitored, stop_event):
        """
        Working as a callback of Thread class, this method keeps looping to
        watch if the params whose names are passed exist and emits signal per
        each node.

        Notice that what MoveitWidget._check_nodes_alive &
        MoveitWidget._check_params_alive do is very similar, but since both of
        them are supposed to be passed to Thread class, there might not be
        a way to generalize these 2.

        @type signal: Signal(bool, str)
        @param_name signal: emitting a name of the parameter that's found.
        @type params_monitored: str[]
        @type stop_event: Event()
        """

        while True:
            has_param = False

            for param_name in params_monitored:
                is_rosmaster_running = RqtRoscommUtil.is_roscore_running()

                try:
                    if is_rosmaster_running:
                        # Only if rosmaster is running, check if the parameter
                        # exists or not.
                        has_param = rospy.has_param(param_name)
                except rospy.exceptions.ROSException as e:
                    rospy.logerr('Exception upon rospy.has_param {}'.format(e.message))
                    self.sig_sysmsg.emit('Exception upon rospy.has_param {}'.format(e.message))
                signal.emit(has_param, param_name)
                rospy.logdebug('has_param {}, check_param_alive: {}'.format(has_param, param_name))
            if stop_event.wait(self._refresh_rate):
                return

    def _update_output_parameters(self, has_param, param_name):
        """
        Slot

        @type has_param: bool
        @type param_name: str
        """
        rospy.logdebug('has_param={} par_name={}'.format(has_param,
                                                         param_name))
        param_name = str(param_name)
        param_qitem = None
        if param_name not in self._param_qitems:
            param_qitem = QStandardItem(param_name)
            self._param_qitems[param_name] = param_qitem
            self._param_datamodel.appendRow(param_qitem)
        else:  # qsitem with the param name already exists.
            param_qitem = self._param_qitems[str(param_name)]

        qindex = self._param_datamodel.indexFromItem(param_qitem)
        _str_param_found = 'No'
        if has_param:
            _str_param_found = 'Yes'
        qitem_param_status = QStandardItem(_str_param_found)
        self._param_datamodel.setItem(qindex.row(), 1, qitem_param_status)
        self._view_params.resizeColumnsToContents()

    def _update_refreshrate(self, refresh_rate):
        """
        Slot

        @type refresh_rate: int
        """
        self._refresh_rate = refresh_rate

    def save_settings(self, plugin_settings, instance_settings):
        instance_settings.set_value(self._SPLITTER_H,
                                    self._splitter.saveState())

    def restore_settings(self, plugin_settings, instance_settings):
        if instance_settings.contains(self._SPLITTER_H):
            self._splitter.restoreState(instance_settings.value(self._SPLITTER_H))
        else:
            self._splitter.setSizes([100, 100, 200])
        pass

    def shutdown(self):
        """
        Overridden.

        Close threads.

        @raise RuntimeError:
        """
        try:
            self._stop_event.set()

            self._node_monitor_thread.join()
            self._param_check_thread.join()
            self._topic_monitor_thread.join()

            self._node_monitor_thread = None
            self._param_check_thread = None
            self._topic_monitor_thread = None

        except RuntimeError as e:
            rospy.logerr(e)
            raise e


if __name__ == '__main__':
    # main should be used only for debug purpose.
    # This moveites this QWidget as a standalone rqt gui.
    from rqt_gui.main import Main

    main = Main()
    sys.exit(main.main(sys.argv, standalone='rqt_moveit'))
