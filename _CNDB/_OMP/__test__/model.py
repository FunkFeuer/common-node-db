# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.__test__.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    16-Dec-2015 (CT) Change to `UI_Spec`
#    ««revision-date»»···
#--

from   _CNDB                      import CNDB
import _CNDB._OMP
from   _GTW.__test__.Test_Command import *

import _CNDB._OMP.import_CNDB
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._OMP._Auth.UI_Spec
import _GTW._OMP._PAP.UI_Spec
import _CNDB._OMP.UI_Spec

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
