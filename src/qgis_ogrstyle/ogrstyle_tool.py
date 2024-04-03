# -*- coding: utf-8 -*-
# ******************************************************************************
#
# Copy_Coords
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and copies them to the table
#
# Copyright (C) 2013 Maxim Dubinin (sim@gis-lab.info), NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
# ******************************************************************************

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMessageBox
from osgeo import ogr

from qgis.core import *
from qgis.gui import *

# initialize resources (icons) from resources.py
from . import resources


class OGRStyleTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        # self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface

        self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)

        self.layer = self.iface.activeLayer()

        self.identify_tool = QgsMapToolIdentify(self.canvas)

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def canvasReleaseEvent(self, event):
        clipboard = QApplication.clipboard()
        clipboard.setText(None)
        self.canvas.setCursor(self.cursor)
        if self.iface.activeLayer():
            x = event.pos().x()
            y = event.pos().y()
            clicked_feature = self.identify_tool.identify(x, y)
            if clicked_feature:
                clicked_feature_id = clicked_feature[0].mFeature.id()
                ds_uri = self.iface.activeLayer().dataProvider().dataSourceUri()
                if '|' in ds_uri:
                    ds_uri = ds_uri.split('|')
                    ds_path = ds_uri[0]
                    ogr_layer = ogr.Open(ds_path)
                    if ogr_layer:
                        feature = ogr_layer[0].GetFeature(clicked_feature_id)
                        clipboard.setText(f'{feature.GetStyleString()}')
