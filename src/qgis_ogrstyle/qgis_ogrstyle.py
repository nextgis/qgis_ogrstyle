# -*- coding: utf-8 -*-
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
import os
from os import path

from PyQt5.QtWidgets import QApplication
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .ogrstyle_tool import OGRStyleTool
from . import about_dialog

# initialize resources (icons) from resources.py
from . import resources
from .qgis_ogrstyle_dialog import QgisOgrStyleDialog


class CopyOGRStyle:

    def __init__(self, iface):
        """Initialize class"""
        # save reference to QGIS interface
        self.clipboard = None
        self.iface = iface
        self.plugin_dir = path.dirname(__file__)
        self._translator = None
        self.__init_translator()

    def initGui(self):
        """Initialize graphic user interface"""

        # create action that will be run by the plugin
        self.action = QAction(
            self.tr("NextGIS OGRStyle"), self.iface.mainWindow()
        )
        self.action.setIcon(QIcon(":/icons/cursor.png"))
        self.action.setWhatsThis(self.tr("NextGIS OGRStyle"))
        self.actionAbout = QAction(
            self.tr("About plugin…"), self.iface.mainWindow()
        )
        self.actionAbout.setWhatsThis(self.tr("About NextGIS OGRStyle plugin"))

        # add plugin menu to Vector toolbar
        self.iface.addPluginToMenu("NextGIS OGRStyle", self.action)
        self.iface.addPluginToMenu("NextGIS OGRStyle", self.actionAbout)

        # add icon to new menu item in Vector toolbar
        self.iface.addToolBarIcon(self.action)

        # connect action to the run method
        self.action.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

        # prepare map tool
        self.mapTool = OGRStyleTool(self.iface)

    def __init_translator(self):
        # initialize locale
        locale = QgsApplication.instance().locale()

        def add_translator(locale_path):
            if not path.exists(locale_path):
                return
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            self._translator = translator  # Should be kept in memory

        add_translator(path.join(
            self.plugin_dir, 'i18n',
            'copy_ogr_style_{}.qm'.format(locale)
        ))

    def unload(self):
        """Actions to run when the plugin is unloaded"""
        # remove menu and icon from the menu
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("NextGIS OGRStyle", self.action)
        self.iface.removePluginMenu("NextGIS OGRStyle", self.actionAbout)
        self.actionAbout.deleteLater()
        self.action.deleteLater()

        if self.iface.mapCanvas().mapTool() == self.mapTool:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)

        del self.mapTool

    def run(self):
        """Action to run"""
        # create a string and show it

        self.iface.mapCanvas().setMapTool(self.mapTool)

    def about(self):
        dialog = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec_()

    def tr(self, message):
        return QCoreApplication.translate(__class__.__name__, message)
