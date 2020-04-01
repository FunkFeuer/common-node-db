# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.Wireless_Standard
#
# Purpose
#    Model a wireless standard
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    17-Dec-2012 (CT) Change `name.completer.treshold` to `0` (was `2`)
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Object

class Wireless_Standard (_Ancestor_Essence) :
    """Wireless standard"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name of the standard"""

            kind               = Attr.Primary
            max_length         = 20
            ignore_case        = True
            completer          = Attr.Completer_Spec  (0, Attr.Selector.primary)

        # end class name

        class bandwidth (A_Frequency) :
            """Bandwidth of a channel"""

            kind               = Attr.Necessary

        # end class bandwidth

    # end class _Attributes

# end class Wireless_Standard

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Wireless_Standard
