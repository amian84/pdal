# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
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

class User():
    def __init__(self,uid, username, display, home):
        self.uid = uid
        self.username = username
        self.display = None
        if not display == '':
            self.display = display
        self.home = home

    def get_username(self):
        return self.username

    def get_uid(self):
        return self.uid

    def get_display(self):
        return self.display

    def get_home(self):
        return self.home

    def have_display(self):
        if not self.display == None:
            return True
        return False

