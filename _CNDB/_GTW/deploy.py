# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#     2-Sep-2014 (CT) Redefine `Babel` to augment `_package_dirs`
#     2-Sep-2014 (CT) Add `template_package_dirs` to `_defaults`
#     6-Mar-2015 (CT) Use `update_combined.List_DC` for `lib_dir`
#    ««revision-date»»···
#--

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _TFL                     import TFL
from   _TFL.update_combined     import update_combined

import _CNDB._GTW
import _GTW.deploy

_Ancestor = GTW.deploy.Command

class _CNDB_deploy_Command_ (_Ancestor) :
    """Manage deployment of CNDB application"""

    _real_name     = "Command"
    _rn_prefix     = "_CNDB_"

    _defaults      = dict \
        ( lib_dir  = update_combined.List_DC (["cndb", "tapyr"])
                         ### override, i.e., don't combine, `lib_dir`
        , template_package_dirs = ["_CNDB._JNJ", "_JNJ"]
        )

    class _CNDB_Babel_ (_Ancestor._Babel_) :

        _package_dirs           = \
            [ "_CNDB"
            , "_CNDB._GTW"
            , "_CNDB._JNJ"
            , "_CNDB._OMP"
            ]

    _Babel_ = _CNDB_Babel_ # end class

Command = _CNDB_deploy_Command_ # end class

if __name__ != "__main__" :
    CNDB.GTW._Export_Module ()
### __END__ CNDB.GTW.deploy
