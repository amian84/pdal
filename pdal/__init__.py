# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    Antonio Hernández <ahernandez at emergya.com>
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

import gettext
import os

language='en'
f = open('/etc/default/locale','r')
for line in f:
    default_locale=line.split('=')
    if default_locale[0] == 'LANG':
        value = default_locale[1].replace('"','')
        languages = value.split('_')
        language = languages[0]

print language
gettext.textdomain('pdal')

try:
    lang = gettext.translation('pdal',languages=[language])
    _ = lang.gettext

except:
    _ = gettext.gettext
