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
#    CNDB.deploy
#
# Purpose
#    Extendable Command for the deployment of applications based on CNDB
#
# Revision Dates
#     5-Sep-2014 (CT) Creation (factored from FFW)
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CNDB._GTW.deploy
import _GTW._Werkzeug.deploy

import _CNDB._Base_Command_

class CNDB_Command \
          ( CNDB._Base_Command_
          , CNDB.GTW.deploy.Command
          , GTW.Werkzeug.deploy.Command
          ) :

    _defaults               = dict \
        ( app_dir           = "www/app"
        , app_module        = "./Command.py"
        , bugs_address      = "tanzer@swing.co.at,ralf@runtux.com"
        , copyright_holder  = "Mag. Christian Tanzer, Ralf Schlatterbeck"
        , languages         = "de,en"
        )

Command = CNDB_Command # end class

if __name__ != "__main__" :
    CNDB._Export_Module ()
### __END__ CNDB.deploy
