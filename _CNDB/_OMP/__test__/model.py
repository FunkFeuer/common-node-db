# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.__test__.
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
#    CNDB.OMP.__test__.model
#
# Purpose
#    CNDB-specific descendent of GTW.__test__.Test_Command
#
# Revision Dates
#    18-Sep-2012 (CT) Creation
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CNDB                      import CNDB
import _CNDB._OMP
from   _GTW.__test__.Test_Command import *

import _CNDB._OMP.import_CNDB
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._OMP._Auth.Nav
import _GTW._OMP._PAP.Nav
import _CNDB._OMP.Nav

class _CNDB_Test_Command_ (GTW_Test_Command) :

    _rn_prefix              = "_CNDB_Test"

    ANS                     = CNDB

    def fixtures (self, scope) :
        if sos.environ.get ("GTW_FIXTURES") :
            pass ### XXX add fixtures if necessary
    # end def fixtures

    def _nav_admin_groups (self) :
        RST = GTW.RST
        return \
            [ self.nav_admin_group
                ( "CNDB"
                , _ ("Administration of node database")
                , "CNDB"
                , permission = RST.In_Group ("CNDB-admin")
                )
            , self.nav_admin_group
                ( "PAP"
                , _ ("Administration of persons/addresses...")
                , "GTW.OMP.PAP"
                , permission = RST.In_Group ("CNDB-admin")
                )
            , self.nav_admin_group
                ( _ ("Users")
                , _ ("Administration of user accounts and groups")
                , "GTW.OMP.Auth"
                , permission = RST.Is_Superuser ()
                )
            ]
    # end def _nav_admin_groups

_Command_  = _CNDB_Test_Command_ # end class

Scaffold   = _Command_ ()

### __END__ CNDB.OMP.__test__.model
