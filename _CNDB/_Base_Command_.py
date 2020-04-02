# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB._Base_Command_
#
# Purpose
#    Common base class for CNDB `Command` and `deploy` classes
#
# Revision Dates
#     5-Sep-2014 (CT) Creation (factored from FFW)
#    ««revision-date»»···
#--

from   _CNDB                    import CNDB
from   _TFL                     import TFL

import _TFL.Command

class _Base_Command_ (TFL.Command.Root_Command) :

    class Config_Dirs (TFL.Command.Root_Command.Config_Dirs) :

        _defaults = \
            ( "~/"
            , "$app_dir/../.."
            , "~/httpd_config"
            , "$app_dir/httpd_config"
            )

    # end class Config_Dirs

# end class _Base_Command_

if __name__ != "__main__" :
    CNDB._Export ("_Base_Command_")
### __END__ CNDB._Base_Command_
