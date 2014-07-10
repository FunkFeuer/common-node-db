# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.GTW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    deploy
#
# Purpose
#    Deploy command for CNDB
#
# Revision Dates
#    10-Jul-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CNDB._GTW
import _GTW.deploy

class _CNDB_deploy_Command_ (GTW.deploy.Command) :
    """Manage deployment of CNDB application"""

    _real_name     = "Command"
    _defaults      = dict \
        ( lib_dir  = ["cndb", "tapyr"]
        )

Command = _CNDB_deploy_Command_ # end class

if __name__ != "__main__" :
    CNDB.GTW._Export_Module ()
### __END__ CNDB.GTW.deploy
