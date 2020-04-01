# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Net_Interface
#
# Purpose
#    Model network interfaces in CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `mac_address` to `Primary_Optional`, add `name`
#    13-Sep-2012 (RS) Set `is_partial`
#    22-Sep-2012 (RS) make `name` `A_DNS_Label`
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    26-Jan-2013 (CT) Set `Net_Interface.is_relevant`
#     7-May-2013 (RS) Add `desc`
#     8-May-2013 (RS) Fix comment for desc
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node_Left`, not `Belongs_to_Node`
#    14-Apr-2014 (CT) Add mixin `Belongs_to_Net_Device_Left`
#    17-Apr-2014 (CT) Fix typo in `Net_Interface.name.description`
#    30-Apr-2014 (CT) Set `left.Kind_Mixins` to `Attr.Init_Only_Mixin`
#    13-Jun-2014 (RS) Add `ui_name` for `desc`
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

from   _GTW._OMP._DNS.Attr_Type import A_DNS_Label

import _CNDB._OMP.Net_Device
import _CNDB._OMP.Belongs_to_Net_Device
import _CNDB._OMP.Belongs_to_Node

from   _GTW._OMP._NET           import NET
import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = CNDB.OMP.Link1
_Mixin_1 = CNDB.OMP.Belongs_to_Node_Left
_Mixin_2 = CNDB.OMP.Belongs_to_Net_Device_Left

class Net_Interface (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Model a network interface of a CNDB device"""

    is_partial  = True
    is_relevant = True

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Network device the interface is connected to."""

            role_type          = CNDB.OMP.Net_Device
            role_name          = "device"
            Kind_Mixins        = (Attr.Init_Only_Mixin, )
            show_in_ui_selector= False

        # end class left

        class mac_address (NET.A_MAC_Address) :
            """MAC address of interface."""

            kind               = Attr.Primary_Optional

        # end class mac_address

        class name (A_DNS_Label) :
            """Name of the interface."""

            kind               = Attr.Primary_Optional
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class is_active (A_Boolean) :
            """Indicates if this interface is active."""

            kind               = Attr.Optional

        # end class is_active

        class desc (A_Text) :
            """Description of interface"""

            kind               = Attr.Optional
            ui_name            = "Description"

        # end class desc

    # end class _Attributes

# end class Net_Interface

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Interface
