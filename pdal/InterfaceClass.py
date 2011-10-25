# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    Antonio Hernández <ahernandez at emergya.com>
#    David Amian <damian at emergya.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

import sys
import os.path
from pdal import utils
#import gudev
from gi.repository import GUdev
import re
import sys

class InterfaceClass():

    def __init__(self, sysfspath):
        self.sysfspath = sysfspath
        self.client = GUdev.Client.new('usb')
        self.int_udev = self.client.query_by_sysfs_path(sysfspath)

    def __str__(self):
        return self.get_formated_name()

    def get_udev_object(self):
        return self.int_udev

    def get_devices_fs(self):
        devices_fs = []
        l_udev = self.client.query_by_subsystem('*')
        for udev_object in l_udev:
            if self.sysfspath + '/' in udev_object.get_sysfs_path():
                if udev_object.get_property('DEVTYPE')=='disk':
                    devices_fs.append(udev_object.get_property('DEVNAME'))
        return devices_fs
    
    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):
        filename = None
        l_udev = self.client.query_by_subsystem('*')
        for udev_object in l_udev:
            if self.sysfspath + '/' in udev_object.get_sysfs_path():
                filename = udev_object.get_property('ICON')
                if filename:
                    if not os.path.exists(filename):
                        filename = utils.get_theme_icon_path(filename, icon_size, flags)
                    return filename

        return filename

