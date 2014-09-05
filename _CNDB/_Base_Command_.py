# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.
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
#    CNDB._Base_Command_
#
# Purpose
#    Common base class for CNDB `Command` and `deploy` classes
#
# Revision Dates
#     5-Sep-2014 (CT) Creation (factored from FFW)
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

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
