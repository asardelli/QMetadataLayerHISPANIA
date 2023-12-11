#-----------------------------------------------------------
# Copyright (C) 2021 Aldo Sardelli
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from .QML_proceso import *

def classFactory(iface):
    return QML(iface)
