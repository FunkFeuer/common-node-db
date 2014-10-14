# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Wired_Interface
#
# Purpose
#    Model a wired interface of a CNDB device
#
# Revision Dates
#    10-May-2012 (CT) Creation
#    17-Dec-2012 (RS) Add `auto_cache` for `left`
#    13-May-2013 (CT) Remove `auto_cache`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

from   _CNDB._OMP.Attr_Type         import *
import _CNDB._OMP.Net_Interface

_Ancestor_Essence = CNDB.OMP.Net_Interface

class Wired_Interface (_Ancestor_Essence) :
    """Wired interface of a CNDB device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

        # end class left

        ### Phy, speed

    # end class _Attributes

# end class Wired_Interface

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Wired_Interface
