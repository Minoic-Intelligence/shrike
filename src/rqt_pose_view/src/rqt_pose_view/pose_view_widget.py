# Copyright (c) 2011, Dorian Scholz, TU Darmstadt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the TU Darmstadt nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import division
import os
import rospkg

from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, qWarning, Slot
from python_qt_binding.QtWidgets import QAction, QMenu, QWidget

import rospy
from rostopic import get_topic_class
from rqt_py_common.topic_helpers import find_slots_by_type_bfs
from tf.transformations import quaternion_matrix, quaternion_about_axis
from geometry_msgs.msg import Quaternion, Pose, Point

from OpenGL.GL import glBegin, glColor3f, glEnd, glLineWidth, glMultMatrixf, glTranslatef, \
    glVertex3f, GL_LINES, GL_QUADS
from .gl_widget import GLWidget


# main class inherits from the ui window class
class PoseViewWidget(QWidget):

    def __init__(self, plugin):
        super(PoseViewWidget, self).__init__()
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('rqt_pose_view'), 'resource', 'PoseViewWidget.ui')
        loadUi(ui_file, self)
        self._plugin = plugin

        self._position = (2.0, 2.0, 2.0)
        self._orientation = quaternion_about_axis(0.0, (1.0, 0.0, 0.0))
        self._topic_name = None
        self._subscriber = None

        # create GL view
        self._gl_view = GLWidget()
        self._gl_view.setAcceptDrops(True)

        # backup and replace original paint method
        self._gl_view.paintGL_original = self._gl_view.paintGL
        self._gl_view.paintGL = self._gl_view_paintGL

        # backup and replace original mouse release method
        self._gl_view.mouseReleaseEvent_original = self._gl_view.mouseReleaseEvent
        self._gl_view.mouseReleaseEvent = self._gl_view_mouseReleaseEvent

        # add GL view to widget layout
        self.layout().addWidget(self._gl_view)

        # init and start update timer with 40ms (25fps)
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self.update_timeout)
        self._update_timer.start(40)

        # subscribe immediately if topic name found on param server
        if rospy.has_param('~pose_view_topic'):
            topic = rospy.get_param('~pose_view_topic')
            try:
                self._subscribe_topic(topic)
            except AttributeError:
                rospy.logwarn("invalid topic name '{}'".format(topic))

    def save_settings(self, plugin_settings, instance_settings):
        view_matrix_string = repr(self._gl_view.get_view_matrix())
        instance_settings.set_value('view_matrix', view_matrix_string)

    def restore_settings(self, plugin_settings, instance_settings):
        view_matrix_string = instance_settings.value('view_matrix')
        try:
            view_matrix = eval(view_matrix_string)
        except Exception:
            view_matrix = None

        if view_matrix is not None:
            self._gl_view.set_view_matrix(view_matrix)
        else:
            self._set_default_view()

    def _set_default_view(self):
        self._gl_view.makeCurrent()
        self._gl_view.reset_view()
        self._gl_view.rotate((0, 0, 1), 45)
        self._gl_view.rotate((1, 0, 0), -65)
        self._gl_view.translate((0, -3, -15))

    def update_timeout(self):
        self._gl_view.makeCurrent()
        self._gl_view.updateGL()

    def _gl_view_paintGL(self):
        self._gl_view.paintGL_original()
        self._paintGLGrid()
        self._paintGLCoorsystem()
        self._paintGLBox()

    def _paintGLBox(self):
        # FIXME: add user configurable setting to allow use of translation as well
        self._position = (2.0, 2.0, 2.0)  # Set fixed translation for now

        glTranslatef(*self._position)     # Translate Box

        matrix = quaternion_matrix(self._orientation)  # convert quaternion to translation matrix
        # tf uses row-major while gl expects column-major
        matrix = matrix.transpose()
        glMultMatrixf(matrix)             # Rotate Box

        glBegin(GL_QUADS)                 # Start Drawing The Box

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)        # Top Right Of The Quad (Top)
        glVertex3f(-1.0, 1.0, -1.0)       # Top Left Of The Quad (Top)
        glVertex3f(-1.0, 1.0, 1.0)        # Bottom Left Of The Quad (Top)
        glVertex3f(1.0, 1.0, 1.0)         # Bottom Right Of The Quad (Top)

        glColor3f(0.5, 1.0, 0.5)
        glVertex3f(1.0, -1.0, 1.0)        # Top Right Of The Quad (Bottom)
        glVertex3f(-1.0, -1.0, 1.0)       # Top Left Of The Quad (Bottom)
        glVertex3f(-1.0, -1.0, -1.0)      # Bottom Left Of The Quad (Bottom)
        glVertex3f(1.0, -1.0, -1.0)       # Bottom Right Of The Quad (Bottom)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)         # Top Right Of The Quad (Front)
        glVertex3f(-1.0, 1.0, 1.0)        # Top Left Of The Quad (Front)
        glVertex3f(-1.0, -1.0, 1.0)       # Bottom Left Of The Quad (Front)
        glVertex3f(1.0, -1.0, 1.0)        # Bottom Right Of The Quad (Front)

        glColor3f(0.5, 0.5, 1.0)
        glVertex3f(1.0, -1.0, -1.0)       # Bottom Left Of The Quad (Back)
        glVertex3f(-1.0, -1.0, -1.0)      # Bottom Right Of The Quad (Back)
        glVertex3f(-1.0, 1.0, -1.0)       # Top Right Of The Quad (Back)
        glVertex3f(1.0, 1.0, -1.0)        # Top Left Of The Quad (Back)

        glColor3f(1.0, 0.5, 0.5)
        glVertex3f(-1.0, 1.0, 1.0)        # Top Right Of The Quad (Left)
        glVertex3f(-1.0, 1.0, -1.0)       # Top Left Of The Quad (Left)
        glVertex3f(-1.0, -1.0, -1.0)      # Bottom Left Of The Quad (Left)
        glVertex3f(-1.0, -1.0, 1.0)       # Bottom Right Of The Quad (Left)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)        # Top Right Of The Quad (Right)
        glVertex3f(1.0, 1.0, 1.0)         # Top Left Of The Quad (Right)
        glVertex3f(1.0, -1.0, 1.0)        # Bottom Left Of The Quad (Right)
        glVertex3f(1.0, -1.0, -1.0)       # Bottom Right Of The Quad (Right)
        glEnd()                           # Done Drawing The Quad

    def _paintGLGrid(self):
        resolution_millimeters = 1
        gridded_area_size = 100

        glLineWidth(1.0)

        glBegin(GL_LINES)

        glColor3f(1.0, 1.0, 1.0)

        glVertex3f(gridded_area_size, 0, 0)
        glVertex3f(-gridded_area_size, 0, 0)
        glVertex3f(0, gridded_area_size, 0)
        glVertex3f(0, -gridded_area_size, 0)

        num_of_lines = int(gridded_area_size / resolution_millimeters)

        for i in range(num_of_lines):
            glVertex3f(resolution_millimeters * i, -gridded_area_size, 0)
            glVertex3f(resolution_millimeters * i, gridded_area_size, 0)
            glVertex3f(gridded_area_size, resolution_millimeters * i, 0)
            glVertex3f(-gridded_area_size, resolution_millimeters * i, 0)

            glVertex3f(resolution_millimeters * (-i), -gridded_area_size, 0)
            glVertex3f(resolution_millimeters * (-i), gridded_area_size, 0)
            glVertex3f(gridded_area_size, resolution_millimeters * (-i), 0)
            glVertex3f(-gridded_area_size, resolution_millimeters * (-i), 0)

        glEnd()

    def _paintGLCoorsystem(self):
        glLineWidth(10.0)

        glBegin(GL_LINES)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 1.0)

        glEnd()

    def _gl_view_mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            menu = QMenu(self._gl_view)
            action = QAction(self._gl_view.tr("Reset view"), self._gl_view)
            menu.addAction(action)
            action.triggered.connect(self._set_default_view)
            menu.exec_(self._gl_view.mapToGlobal(event.pos()))

    @Slot('QDragEnterEvent*')
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            topic_name = str(event.mimeData().text())
            if len(topic_name) == 0:
                qWarning('PoseViewWidget.dragEnterEvent(): event.mimeData() text is empty')
                return
        else:
            if not hasattr(event.source(), 'selectedItems') or len(event.source().selectedItems()) == 0:
                qWarning('PoseViewWidget.dragEnterEvent(): event.source() has no attribute selectedItems or length of selectedItems is 0')
                return
            item = event.source().selectedItems()[0]
            topic_name = item.data(0, Qt.UserRole)

            if topic_name is None:
                qWarning('PoseViewWidget.dragEnterEvent(): selectedItem has no UserRole data with a topic name')
                return

        # check for valid topic
        msg_class, self._topic_name, _ = get_topic_class(topic_name)
        if msg_class is None:
            qWarning('PoseViewWidget.dragEnterEvent(): No message class was found for topic "%s".' % topic_name)
            return

        # check for valid message class
        quaternion_slot_path, point_slot_path = self._get_slot_paths(msg_class)

        if quaternion_slot_path is None and point_slot_path is None:
            qWarning('PoseViewWidget.dragEnterEvent(): No Pose, Quaternion or Point data was found outside of arrays in "%s" on topic "%s".'
                     % (msg_class._type, topic_name))
            return

        event.acceptProposedAction()

    @Slot('QDropEvent*')
    def dropEvent(self, event):
        if event.mimeData().hasText():
            topic_name = str(event.mimeData().text())
        else:
            dropped_item = event.source().selectedItems()[0]
            topic_name = str(dropped_item.data(0, Qt.UserRole))

        self._unregister_topic()
        self._subscribe_topic(topic_name)

    def _unregister_topic(self):
        if self._subscriber:
            self._subscriber.unregister()

    @staticmethod
    def _make_path_list_from_path_string(path):
        path = path.split('/')
        if path == ['']:
            return []
        return path

    @staticmethod
    def _get_slot_paths(msg_class):
        # find first Pose in msg_class
        pose_slot_paths = find_slots_by_type_bfs(msg_class, Pose)
        for path in pose_slot_paths:
            # make sure the path does not contain an array, because we don't want to deal with empty arrays...
            if '[' not in path:
                path = PoseViewWidget._make_path_list_from_path_string(pose_slot_paths[0])
                return path + ['orientation'], path + ['position']

        # if no Pose is found, find first Quaternion and Point
        quaternion_slot_paths = find_slots_by_type_bfs(msg_class, Quaternion)
        for path in quaternion_slot_paths:
            if '[' not in path:
                quaternion_slot_path = PoseViewWidget._make_path_list_from_path_string(path)
                break
        else:
            quaternion_slot_path = None

        point_slot_paths = find_slots_by_type_bfs(msg_class, Point)
        for path in point_slot_paths:
            if '[' not in path:
                point_slot_path = PoseViewWidget._make_path_list_from_path_string(path)
                break
        else:
            point_slot_path = None

        return quaternion_slot_path, point_slot_path


    def _subscribe_topic(self, topic_name):
        msg_class, self._topic_name, _ = get_topic_class(topic_name)
        quaternion_slot_path, point_slot_path = self._get_slot_paths(msg_class)

        self._subscriber = rospy.Subscriber(
                self._topic_name,
                msg_class,
                self.message_callback,
                callback_args=(quaternion_slot_path, point_slot_path)
        )

    def message_callback(self, message, slot_paths):
        quaternion_slot_path = slot_paths[0]
        point_slot_path = slot_paths[1]

        if quaternion_slot_path is None:
            self._orientation = quaternion_about_axis(0.0, (1.0, 0.0, 0.0))
        else:
            orientation = message
            for slot_name in quaternion_slot_path:
                orientation = getattr(orientation, slot_name)
            self._orientation = (orientation.x, orientation.y, orientation.z, orientation.w)

        if point_slot_path is None:
            # if no point is given, set it to a fixed offset so the axes can be seen
            self._position = (2.0, 2.0, 2.0)
        else:
            position = message
            for slot_name in point_slot_path:
                position = getattr(position, slot_name)
            self._position = (position.x, position.y, position.z)

    def shutdown_plugin(self):
        self._unregister_topic()
