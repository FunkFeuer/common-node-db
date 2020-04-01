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
#    CNDB.OMP.Device
#
# Purpose
#    Model a device in CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#     8-Dec-2012 (RS) Add `desc`
#    17-Dec-2012 (CT) Use `ui_type_name` in docstrings
#    13-Jun-2014 (RS) Add `ui_name` to `desc`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
import _CNDB._OMP.Device_Type

_Ancestor_Essence = CNDB.OMP.Link1

class Device (_Ancestor_Essence) :
    """Model a device used by a CNDB node."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Type of %(ui_type_name)s"""

            role_type          = CNDB.OMP.Device_Type
            role_name          = "type"
            ui_allow_new       = False

        # end class left

        class name (A_String) :
            """Name of %(ui_type_name)s"""

            kind               = Attr.Primary_Optional
            max_length         = 40
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class desc (A_Text) :
            """Description of device"""

            kind               = Attr.Optional
            ui_name            = "Description"

        # end class desc

    # end class _Attributes

# end class Device

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Device
