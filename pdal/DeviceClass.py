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

import os.path
from gi.repository import GUdev
#import gudev
import sys
import gettext
from pdal import utils, InterfaceClass
from pdal.pdalconfig import get_data_path
from gettext import gettext as _
gettext.textdomain('pdal')

class DeviceClass():


    def __init__(self, sysfspath):
        self.sysfspath = sysfspath
        self.client = GUdev.Client.new('usb')
        #self.client = gudev.Client('usb')
        self.dev_udev = self.client.query_by_sysfs_path(sysfspath)
        
        if self.dev_udev == None:
            raise Exception('Device not found: ' + sysfspath)
        self.de = None
        self.list_interfaces = None

    def __str__(self):
        return self.get_formated_name()

    def get_sysfs_path(self):
        return self.sysfspath

    def get_udev_object(self):
        return self.dev_udev

    def get_formated_name(self):
        vendor = self.dev_udev.get_property('ID_VENDOR')
        model = self.dev_udev.get_property('ID_MODEL')
        vendor = vendor.replace('_', ' ')
        model = model.replace('_', ' ')
        return vendor + " " + model

    def get_vendor(self):
        vendor = self.dev_udev.get_property('ID_VENDOR')
        vendor = vendor.replace('_', ' ')
        return vendor

    def get_model(self):
        model = self.dev_udev.get_property('ID_MODEL')
        model = model.replace('_', ' ')
        return model

    def get_model_id(self):
        model_id = self.dev_udev.get_property('ID_MODEL_ID')
        return model_id

    def get_vendor_id(self):
        vendor_id = self.dev_udev.get_property('ID_VENDOR_ID')
        return vendor_id

    def get_devname(self):
        devname = self.dev_udev.get_property('DEVNAME')
        return devname

    def get_devices_fs(self):
        devices_fs = []
        num_interfaces = self.get_number_interfaces()
        for i in range(num_interfaces):
            iclass = self.get_interfaces()[i]
            devices_fs = devices_fs + iclass.get_devices_fs()

        return devices_fs                


    def get_interfaces(self):
        if self.list_interfaces == None:
            self.list_interfaces = list()
            l_usb_udev = self.client.query_by_subsystem('usb')
            for usb_udev in l_usb_udev:
                if self.sysfspath + "/" in usb_udev.get_sysfs_path():
                   interface_udev = InterfaceClass.InterfaceClass(usb_udev.get_sysfs_path())
                   self.list_interfaces.append(interface_udev)

            return self.list_interfaces
        else:
            return self.list_interfaces

    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flag=0):
        if self.dev_udev.get_property('ICON'):
            filename = self.dev_udev.get_property('ICON')
            if not os.path.exists(filename):
                filename = utils.get_theme_icon_path(filename, icon_size, flag)
                return filename
            return filename
        num_interfaces = self.get_number_interfaces()
        for i in range(num_interfaces):
            iclass = self.get_interfaces()[i]
            filename = iclass.get_icon(icon_size, flag)
            if type(filename) == str and not os.path.exists(filename):
                filename = utils.get_theme_icon_path(filename, icon_size, flag)

            if filename != None:
                return filename
        else:
            return utils.get_default_icon_device()

    def get_pixbuf(self, icon_size=utils.DEFAULT_ICON_SIZE, flag=0):
        return utils.get_pixbuf_from_file(self.get_icon(), icon_size, flag)

    def get_number_interfaces(self):
        if self.list_interfaces == None:
            self.list_interfaces = self.get_interfaces()
        return len(self.list_interfaces)

    def get_device_type(self):
        num_interfaces=self.get_number_interfaces()
        if self.dev_udev.get_property('ICON'):
            filename = self.dev_udev.get_property('ICON')
            if filename == 'camera-photo':
                return _("camera photo")
            elif filename == 'multimedia-player':
                return _("multimedia player")
            else:
                return filename
        else:
            if num_interfaces == 1:
                return self.get_interfaces()[0].get_formated_name()
            else:
                return _("device")


