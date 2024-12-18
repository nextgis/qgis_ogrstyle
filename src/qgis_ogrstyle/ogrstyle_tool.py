# ******************************************************************************
#
# Copy_Coords
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and copies them to the table
#
# Copyright (C) 2024 NextGIS (info@nextgis.com)
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

from osgeo import ogr
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import *
from qgis.gui import *

from . import resources  # noqa: F401

# initialize resources (icons) from resources.py
from .qgis_ogrstyle_dialog import QgisOgrStyleDialog


class OGRStyleTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        # self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface

        self.cursor = QCursor(
            QPixmap(":/plugins/qgis_ogrstyle/icons/cursor.png"), 1, 1
        )

        self.layer = self.iface.activeLayer()

        self.identify_tool = QgsMapToolIdentify(self.canvas)

        self.dlg = QgisOgrStyleDialog()

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def canvasReleaseEvent(self, event):
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        clipboard = QApplication.clipboard()
        clipboard.setText(None)
        self.canvas.setCursor(self.cursor)
        if self.iface.activeLayer():
            x = event.pos().x()
            y = event.pos().y()
            clicked_feature = self.identify_tool.identify(x, y)
            if clicked_feature:
                clicked_feature_id = clicked_feature[0].mFeature.id()
                ds_path = (
                    self.iface.activeLayer().dataProvider().dataSourceUri()
                )
                if "|" in ds_path:
                    ds_path = ds_path.split("|")
                    ds_path = ds_path[0]
                ogr_layer = ogr.Open(ds_path)
                if ogr_layer:
                    feature = ogr_layer[0].GetFeature(clicked_feature_id)
                    clipboard.setText(f"{feature.GetStyleString()}")
                    self.dlg.StyleLineEdit.setText(clipboard.text())
            else:
                self.dlg.StyleLineEdit.setText("")
        self.dlg.StyleLineEdit.setCursorPosition(0)
        self.dlg.show()
