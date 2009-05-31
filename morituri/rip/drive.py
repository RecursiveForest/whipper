# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Morituri - for those about to RIP

# Copyright (C) 2009 Thomas Vander Stichele

# This file is part of morituri.
# 
# morituri is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# morituri is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with morituri.  If not, see <http://www.gnu.org/licenses/>.

import pycdio
import cdio

from morituri.common import logcommand

class List(logcommand.LogCommand):
    summary = "list drives"

    def do(self, args):
        print 'getting paths'
        
        # using FS_AUDIO here only makes it list the drive when an audio cd
        # is inserted
        paths = cdio.get_devices_with_cap(pycdio.FS_MATCH_ALL, False)
        for path in paths:
            device = cdio.Device(path)
            ok, vendor, model, release = device.get_hwinfo()
            print "drive: %s, vendor: %s, model: %s, release: %s" % (
                path, vendor, model, release)

class Drive(logcommand.LogCommand):
    summary = "handle drives"

    subCommandClasses = [List, ]

