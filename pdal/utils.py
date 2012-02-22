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

from gi.repository import Notify
import os
import sys
from pdal import _
from pdal.pdalconfig import get_data_path

DEFAULT_ICON_INTERFACE = 'media/default-icon-interface.svg'
DEFAULT_ICON_DEVICE = 'media/default-icon-device.svg'
DEFAULT_ICON_SIZE = 48


def get_default_icon_interface():
    return os.path.join(get_data_path(), DEFAULT_ICON_INTERFACE)

def get_default_icon_device():
    return os.path.join(get_data_path(), DEFAULT_ICON_DEVICE)


def notify(title, message, icon, timeout=Notify.EXPIRES_DEFAULT, transient=True):

    # Desktop Notifications Specification: http://www.galago-project.org/specs/notification/0.9/index.html
    #from gi.repository import Gtk, GdkPixbuf

    if not Notify.init("Pdal " + _("Notifications")):
        return
    #image = Gtk.Image()
    #image.set_from_file(icon)
    #pixbuf = image.get_pixbuf()
    #pixbuf = pixbuf.scale_simple(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE, GdkPixbuf.InterpType.BILINEAR)
    notify_daemon = Notify.Notification()
    notify = notify_daemon.new(title, '\n'+message, icon)
    notify.set_category('device.added')
    notify.set_hint('transient', True)
    notify.set_timeout(timeout)

    if not notify.show():
        print _("Failed to send notification")

def get_script_user_path(home_path):
    return os.path.join(home_path, ".pdal/scripts/")

def get_system_user_path():
    return os.path.join(get_data_path(), "scripts")


#def get_pixbuf_from_file(file_name, icon_size=DEFAULT_ICON_SIZE, flags=GdkPixbuf.InterpType.BILINEAR):
#    if not os.path.exists(file_name):
#        return None
#    image = Gtk.Image()
#    image.set_from_file(file_name)
#    pixbuf = image.get_pixbuf()
#    pixbuf = pixbuf.scale_simple(icon_size, icon_size, flags)
#    return pixbuf

#def get_theme_icon_path(icon_name, icon_size=DEFAULT_ICON_SIZE, flags=0):
#    icon_theme = gtk.icon_theme_get_default()
#    icons = icon_theme.list_icons()
#    if not icon_name in icons:
#        return None
#    return file_name
#
#    file_name = icon_theme.lookup_icon(icon_name, icon_size, flags).get_filename()
