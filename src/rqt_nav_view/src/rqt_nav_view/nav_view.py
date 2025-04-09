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

import rospy
import tf
from tf.transformations import quaternion_from_euler

import numpy
import random
from math import sqrt, atan, pi, degrees

from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PolygonStamped, PointStamped, PoseWithCovarianceStamped, PoseStamped

from python_qt_binding.QtCore import Signal, Slot, QPointF, qWarning, Qt
from python_qt_binding.QtGui import QPixmap, QImage, QPainterPath, QPen, QPolygonF, QColor, qRgb
from python_qt_binding.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QPushButton

from rqt_py_common.topic_helpers import get_field_type

def accepted_topic(topic):
    msg_types = [OccupancyGrid, Path, PolygonStamped, PointStamped]
    msg_type, array = get_field_type(topic)

    if not array and msg_type in msg_types:
        return True
    else:
        return False


class PathInfo(object):
    def __init__(self, name=None):
        self.color = None
        self.sub = None
        self.cb = None
        self.path = None
        self.item = None

        self.name = name


class NavViewWidget(QWidget):

    def __init__(self, map_topic='/map',
                 paths=['/move_base/NavFn/plan', '/move_base/TrajectoryPlannerROS/local_plan'],
                 polygons=['/move_base/local_costmap/robot_footprint']):
        super(NavViewWidget, self).__init__()
        self._layout = QVBoxLayout()
        self._button_layout = QHBoxLayout()

        self.setAcceptDrops(True)
        self.setWindowTitle('Navigation Viewer')

        self.paths = paths
        self.polygons = polygons
        self.map = map_topic
        self._tf = tf.TransformListener()

        self._nav_view = NavView(map_topic, paths, polygons, tf = self._tf, parent = self)

        self._set_pose = QPushButton('Set Pose')
        self._set_pose.clicked.connect(self._nav_view.pose_mode)
        self._set_goal = QPushButton('Set Goal')
        self._set_goal.clicked.connect(self._nav_view.goal_mode)

        self._button_layout.addWidget(self._set_pose)
        self._button_layout.addWidget(self._set_goal)

        self._layout.addLayout(self._button_layout)

        self._layout.addWidget(self._nav_view)

        self.setLayout(self._layout)

    def dragEnterEvent(self, e):
        if not e.mimeData().hasText():
            if not hasattr(e.source(), 'selectedItems') or len(e.source().selectedItems()) == 0:
                qWarning('NavView.dragEnterEvent(): not hasattr(event.source(), selectedItems) or len(event.source().selectedItems()) == 0')
                return
            item = e.source().selectedItems()[0]
            topic_name = item.data(0, Qt.UserRole)
            if topic_name == None:
                qWarning('NavView.dragEnterEvent(): not hasattr(item, ros_topic_name_)')
                return

        else:
            topic_name = str(e.mimeData().text())

        if accepted_topic(topic_name):
            e.accept()
            e.acceptProposedAction()

    def dropEvent(self, e):
        if e.mimeData().hasText():
            topic_name = str(e.mimeData().text())
        else:
            droped_item = e.source().selectedItems()[0]
            topic_name = str(droped_item.data(0, Qt.UserRole))

        topic_type, array = get_field_type(topic_name)
        if not array:
            if topic_type is OccupancyGrid:
                self.map = topic_name

                # Swap out the nav view for one with the new topics
                self._nav_view.close()
                self._nav_view = NavView(self.map, self.paths, self.polygons, self._tf, self)
                self._layout.addWidget(self._nav_view)
            elif topic_type is Path:
                self.paths.append(topic_name)
                self._nav_view.add_path(topic_name)
            elif topic_type is PolygonStamped:
                self.polygons.append(topic_name)
                self._nav_view.add_polygon(topic_name)

    def save_settings(self, plugin_settings, instance_settings):
        self._nav_view.save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        self._nav_view.restore_settings(plugin_settings, instance_settings)


class NavView(QGraphicsView):
    map_changed = Signal()
    path_changed = Signal(str)
    polygon_changed = Signal(str)

    def __init__(self, map_topic='/map',
                 paths=['/move_base/SBPLLatticePlanner/plan', '/move_base/TrajectoryPlannerROS/local_plan'],
                 polygons=['/move_base/local_costmap/robot_footprint'], tf=None, parent=None):
        super(NavView, self).__init__()
        self._parent = parent

        self._pose_mode = False
        self._goal_mode = False
        self.last_path = None


        self.map_changed.connect(self._update)
        self.destroyed.connect(self.close)

        #ScrollHandDrag
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self._map = None
        self._map_item = None

        self.w = 0
        self.h = 0

        self._paths = {}
        self._polygons = {}
        self.path_changed.connect(self._update_path)
        self.polygon_changed.connect(self._update_polygon)

        self._colors = [(238, 34, 116), (68, 134, 252), (236, 228, 46), (102, 224, 18), (242, 156, 6), (240, 64, 10), (196, 30, 250)]

        self._scene = QGraphicsScene()

        if tf is None:
            self._tf = tf.TransformListener()
        else:
            self._tf = tf
        self.map_sub = rospy.Subscriber('/map', OccupancyGrid, self.map_cb)

        for path in paths:
            self.add_path(path)

        for poly in polygons:
            self.add_polygon(poly)

        try:
            self._pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=100)
            self._goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=100)
        except TypeError:
            self._pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped)
            self._goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped)

        self.setScene(self._scene)

    def add_dragdrop(self, item):
        # Add drag and drop functionality to all the items in the view
        def c(x, e):
            self.dragEnterEvent(e)
        def d(x, e):
            self.dropEvent(e)
        item.setAcceptDrops(True)
        item.dragEnterEvent = c
        item.dropEvent = d

    def dragEnterEvent(self, e):
        if self._parent:
            self._parent.dragEnterEvent(e)

    def dropEvent(self, e):
        if self._parent:
            self._parent.dropEvent(e)

    def wheelEvent(self, event):
        event.ignore()
        try:
            delta = event.angleDelta().y()
        except AttributeError:
            delta = event.delta()
        if delta > 0:
            self.scale(1.15, 1.15)
        else:
            self.scale(0.85, 0.85)

    def map_cb(self, msg):
        self.resolution = msg.info.resolution
        self.w = msg.info.width
        self.h = msg.info.height

        a = numpy.array(msg.data, dtype=numpy.uint8, copy=False, order='C')
        a = a.reshape((self.h, self.w))
        if self.w % 4:
            e = numpy.empty((self.h, 4 - self.w % 4), dtype=a.dtype, order='C')
            a = numpy.append(a, e, axis=1)
        image = QImage(a.reshape((a.shape[0] * a.shape[1])), self.w, self.h, QImage.Format_Indexed8)

        for i in reversed(range(101)):
            image.setColor(100 - i, qRgb(i* 2.55, i * 2.55, i * 2.55))
        image.setColor(101, qRgb(255, 0, 0))  # not used indices
        image.setColor(255, qRgb(200, 200, 200))  # color for unknown value -1
        self._map = image
        self.setSceneRect(0, 0, self.w, self.h)
        self.map_changed.emit()

    def add_path(self, name):
        path = PathInfo(name)

        def c(msg):
            if not self._map:
                return

            pp = QPainterPath()

            # Transform everything in to the map frame
            if not (msg.header.frame_id == '/map' or msg.header.frame_id == ''):
                try:
                    self._tf.waitForTransform(msg.header.frame_id, '/map', rospy.Time(), rospy.Duration(10))
                    data = [self._tf.transformPose('/map', pose) for pose in msg.poses]
                except tf.Exception:
                    rospy.logerr("TF Error")
                    data = []
            else:
                data = msg.poses

            if len(data) > 0:
                start = data[0].pose.position
                pp.moveTo(start.x / self.resolution, start.y / self.resolution)

                for pose in data:
                    pt = pose.pose.position
                    pp.lineTo(pt.x / self.resolution, pt.y / self.resolution)

                path.path = pp
                self.path_changed.emit(name)

        path.color = random.choice(self._colors)
        self._colors.remove(path.color)

        path.cb = c
        path.sub = rospy.Subscriber(path.name, Path, path.cb)

        self._paths[name] = path

    def add_polygon(self, name):
        poly = PathInfo(name)

        def c(msg):
            if not self._map:
                return

            if not (msg.header.frame_id == '/map' or msg.header.frame_id == ''):
                try:
                    self._tf.waitForTransform(msg.header.frame_id, '/map', rospy.Time(), rospy.Duration(10))
                    points_stamped = []
                    for pt in msg.polygon.points:
                        ps = PointStamped()
                        ps.header.frame_id = msg.header.frame_id
                        ps.point.x = pt.x
                        ps.point.y = pt.y

                        points_stamped.append(ps)

                    trans_pts = [self._tf.transformPoint('/map', pt).point for pt in points_stamped]
                except tf.Exception:
                    rospy.logerr("TF Error")
                    trans_pts = []
            else:
                trans_pts = [pt for pt in msg.polygon.points]

            if len(trans_pts) > 0:
                pts = [QPointF(pt.x / self.resolution, pt.y / self.resolution) for pt in trans_pts]

                close = trans_pts[0]
                pts.append(QPointF(close.x / self.resolution, close.y / self.resolution))
                poly.path = QPolygonF(pts)

                self.polygon_changed.emit(name)

        poly.color = random.choice(self._colors)
        self._colors.remove(poly.color)

        poly.cb = c
        poly.sub = rospy.Subscriber(poly.name, PolygonStamped, poly.cb)

        self._polygons[name] = poly

    def pose_mode(self):
        if not self._pose_mode:
            self._pose_mode = True
            self._goal_mode = False
            self.setDragMode(QGraphicsView.NoDrag)
        elif self._pose_mode:
            self._pose_mode = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def goal_mode(self):
        if not self._goal_mode:
            self._goal_mode = True
            self._pose_mode = False
            self.setDragMode(QGraphicsView.NoDrag)
        elif self._goal_mode:
            self._goal_mode = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def draw_position(self, e, mirror=True):
        p = self.mapToScene(e.x(), e.y())
        v = (p.x() - self.drag_start[0], p.y() - self.drag_start[1])
        mag = sqrt(pow(v[0], 2) + pow(v[1], 2))
        u = (v[0]/mag, v[1]/mag)

        res = (u[0]*20, u[1]*20)
        path = self._scene.addLine(self.drag_start[0], self.drag_start[1],
                                   self.drag_start[0] + res[0], self.drag_start[1] + res[1])

        if self.last_path:
            self._scene.removeItem(self.last_path)
            self.last_path = None
        self.last_path = path

        if mirror:
            # Mirror point over x axis
            x = ((self.w / 2) - self.drag_start[0]) + (self.w /2)
        else:
            x = self.drag_start[0]

        map_p = [x * self.resolution, self.drag_start[1] * self.resolution]

        angle = atan(u[1] / u[0])
        quat = quaternion_from_euler(0, 0, degrees(angle))

        return map_p, quat

    def mousePressEvent(self, e):
        if self._goal_mode or self._pose_mode:
            p = self.mapToScene(e.x(), e.y())
            self.drag_start = (p.x(), p.y())
        else:
            super(NavView, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if self._goal_mode:
            self._goal_mode = False
            map_p, quat = self.draw_position(e)

            msg = PoseStamped()
            msg.header.frame_id = '/map'
            msg.header.stamp = rospy.Time.now()

            msg.pose.position.x = map_p[0]
            msg.pose.position.y = map_p[1]
            msg.pose.orientation.w = quat[0]
            msg.pose.orientation.z = quat[3]

            self._goal_pub.publish(msg)

        elif self._pose_mode:
            self._pose_mode = False
            map_p, quat = self.draw_position(e)

            msg = PoseWithCovarianceStamped()
            msg.header.frame_id = '/map'
            msg.header.stamp = rospy.Time.now()

            #TODO: Is it ok to just ignore the covariance matrix here?
            msg.pose.pose.orientation.w = quat[0]
            msg.pose.pose.orientation.z = quat[3]
            msg.pose.pose.position.x = map_p[0]
            msg.pose.pose.position.y = map_p[1]

            self._pose_pub.publish(msg)

        # Clean up the path
        if self.last_path:
            self._scene.removeItem(self.last_path)
            self.last_path = None

    #def mouseMoveEvent(self, e):
    #    if e.buttons() == Qt.LeftButton and (self._pose_mode or self._goal_mode):
    #        map_p, quat = self.draw_position(e)

    def close(self):
        if self.map_sub:
            self.map_sub.unregister()
        for p in self._paths.values():
            if p.sub:
                p.sub.unregister()

        for p in self._polygons.values():
            if p.sub:
                p.sub.unregister()

        super(NavView, self).close()

    def _update(self):
        if self._map_item:
            self._scene.removeItem(self._map_item)

        pixmap = QPixmap.fromImage(self._map)
        self._map_item = self._scene.addPixmap(pixmap)

        # Everything must be mirrored
        self._mirror(self._map_item)

        # Add drag and drop functionality
        self.add_dragdrop(self._map_item)

        self.centerOn(self._map_item)
        self.show()

    def _update_path(self, name):
        old_item = None
        if name in self._paths.keys():
            old_item = self._paths[name].item

        self._paths[name].item = self._scene.addPath(self._paths[name].path, pen=QPen(QColor(*self._paths[name].color)))

        # Everything must be mirrored
        self._mirror(self._paths[name].item)

        if old_item:
            self._scene.removeItem(old_item)

    def _update_polygon(self, name):
        old_item = None
        if name in self._polygons.keys():
            old_item = self._polygons[name].item

        self._polygons[name].item = self._scene.addPolygon(self._polygons[name].path, pen=QPen(QColor(*self._polygons[name].color)))

        # Everything must be mirrored
        self._mirror(self._polygons[name].item)

        if old_item:
            self._scene.removeItem(old_item)

    def _mirror(self, item):
        item.scale(-1, 1)
        item.translate(-self.w, 0)

    def save_settings(self, plugin_settings, instance_settings):
        # TODO add any settings to be saved
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO add any settings to be restored
        pass
