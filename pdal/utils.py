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

import pynotify
import os
import gtk
import sys
from pdal import _
from pdal.pdalconfig import get_data_path

def notify(title, message, icon, timeout=pynotify.EXPIRES_DEFAULT, transient=True):

    # Desktop Notifications Specification: http://www.galago-project.org/specs/notification/0.9/index.html

    if not pynotify.init("Pdal " + _("Notifications")):
        return

    notify = pynotify.Notification(title, message)
    notify.set_icon_from_pixbuf(icon)
    notify.set_category('device.added')
    notify.set_urgency(pynotify.URGENCY_LOW)
    notify.set_hint('transient', transient)
    notify.set_timeout(timeout)

    if not notify.show():
        print _("Failed to send notification")

def get_script_user_path():
    return os.path.join(os.path.expanduser('~'), ".pdal/scripts/")

def get_system_user_path():
    return os.path.join(get_data_path(), "scripts")
