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
#    CNDB.OMP.Wireless_Channel
#
# Purpose
#    Model a wireless standard
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    20-Nov-2012 (CT) Fix ancestor of `left`, add `left.role_type`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

import _CNDB._OMP.Wireless_Standard

_Ancestor_Essence = CNDB.OMP.Link1

class Wireless_Channel (_Ancestor_Essence) :
    """Wireless channel of a wireless standard"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """The wireless standard for this channel"""

            role_name          = 'standard'
            role_type          = CNDB.OMP.Wireless_Standard
            ui_allow_new       = False

        # end class left

        class number (A_Int) :
            """number of this channel"""

            kind               = Attr.Primary

        # end class number

        class frequency (A_Frequency) :
            """Center frequency of this channel"""

            kind               = Attr.Necessary
            example            = "2.412 GHz"

        # end class frequency

    # end class _Attributes

# end class Wireless_Channel

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Wireless_Channel
