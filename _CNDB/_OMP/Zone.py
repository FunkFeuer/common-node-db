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
#    CNDB.OMP.Zone
#
# Purpose
#    Model a routing zone of CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Object

class Zone (_Ancestor_Essence) :
    """Model a routing zone of CNDB.OMP."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name of the zone"""

            kind               = Attr.Primary
            max_length         = 64
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

    # end class _Attributes

# end class Zone

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Zone
