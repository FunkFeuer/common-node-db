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
#    CNDB.OMP.Regulatory_Permission
#
# Purpose
#    Model a regulatory transmit permission
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    27-Aug-2012 (RS) Fix `bandwidth`
#    20-Nov-2012 (CT) Fix ancestor of `left`, add `left.role_type`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _MOM._Attr.Number_Interval import *
from   _CNDB                      import CNDB
import _CNDB._OMP
from   _CNDB._OMP.Attr_Type             import A_TX_Power

import _CNDB._OMP.Regulatory_Domain

_Ancestor_Essence = CNDB.OMP.Link1

class Regulatory_Permission (_Ancestor_Essence) :
    """Regulatory transmit permission"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """The regulatory domain that gives this permission."""

            role_name          = 'domain'
            role_type          = CNDB.OMP.Regulatory_Domain
            ui_allow_new       = False

        # end class left

        class band (A_Frequency_Interval) :
            """Frequency range for which transmission is allowed."""

            kind               = Attr.Primary

        # end class band

        class bandwidth (A_Frequency) :
            """Maximum allowed bandwidth."""

            kind               = Attr.Necessary
            example            = "20 MHz"

        # end class bandwidth

        class gain (A_Float) :
            """Maximum allowed antenna gain in dB."""

            kind               = Attr.Optional
            example            = "6"

        # end class gain

        class eirp (A_TX_Power) :
            """Maximum allowed TX power in dBm, dBW or units of W."""

            kind               = Attr.Optional
            example            = "20 dBm"

        # end class gain

        class need_DFS (A_Boolean) :
            """Band needs dynamic frequency selection."""

            kind               = Attr.Necessary
            default            = False

        # end class need_DFS

        class indoor_only (A_Boolean) :
            """Only indoor TX allowed."""

            kind               = Attr.Necessary
            default            = False

        # end class indoor_only

    # end class _Attributes

# end class Regulatory_Permission

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Regulatory_Permission
