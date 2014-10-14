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
#    CNDB.OMP.Wireless_Interface
#
# Purpose
#    Model a wireless interface of a CNDB device
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `protocol` and `ssid` from `Required` to
#                     `Necessary`
#    17-Aug-2012 (AK) `SSID` -> `ESSID`, add `BSSID`, `power` -> `tx_power`
#                     add `frequency`
#    20-Aug-2012 (RS) Cleanup, remove `frequency`, use `A_TX_Power`
#    13-Sep-2012 (RS) Remove `protocol`, add `standard`
#    17-Dec-2012 (RS) Add `auto_cache` for `left`
#    17-Dec-2012 (CT) Add attribute `mode`
#    17-Dec-2012 (CT) Set `standard.ui_allow_new` to `False`
#    26-Feb-2013 (CT) Add `Virtual_Wireless_Interface`,
#                     factor and export `_Wireless_Interface_`
#    27-Feb-2013 (CT) Add `Virtual_Wireless_Interface.hardware.sort_skip = True`
#    27-Feb-2013 (CT) Add `Init_Only_Mixin` and `ui_allow_new` to `hardware`
#    24-Apr-2013 (CT) Move `left.auto_cache` to non-partial classes
#    15-May-2013 (CT) Remove `auto_cache`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

from   _CNDB._OMP.Attr_Type           import *

import _CNDB._OMP.Net_Interface
import _CNDB._OMP.Wireless_Standard

from   _GTW._OMP._NET           import NET
import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = CNDB.OMP.Net_Interface

class _Wireless_Interface_ (_Ancestor_Essence) :
    """Base class for wireless interfaces"""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Non-primary attributes

        class mode (A_Wireless_Mode) :

            kind               = Attr.Optional
            raw_default        = "Ad_Hoc"

        # end class mode

        class essid (A_String) :
            """Network name."""

            example            = "freiesnetz.www.funkfeuer.at"
            kind               = Attr.Optional
            max_length         = 32
            ui_name            = "ESSID"

        # end class essid

        class bssid (NET.A_MAC_Address) :
            """Cell name."""

            kind               = Attr.Optional
            ui_name            = "BSSID"
            example            = "de:ad:be:ef:00:01"

        # end class bssid

        class standard (A_Id_Entity) :
            """Wireless standard used by the wireless interface."""

            kind               = Attr.Necessary
            P_Type             = CNDB.OMP.Wireless_Standard
            ui_allow_new       = False

        # end class standard

        class txpower (A_TX_Power) :
            """Transmit power with unit (units of dBW or W)."""

            kind               = Attr.Optional
            ui_name            = "TX power"

        # end class power

    # end class _Attributes

# end class _Wireless_Interface_

_Ancestor_Essence = _Wireless_Interface_

class Wireless_Interface (_Ancestor_Essence) :
    """Wireless interface of a CNDB device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

        # end class left

    # end class _Attributes

# end class Wireless_Interface

_Ancestor_Essence = _Wireless_Interface_

class Virtual_Wireless_Interface (_Ancestor_Essence) :
    """Virtual wireless interface of a CNDB device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

        # end class left

        class hardware (A_Id_Entity) :
            """Hardware interface used by virtual interface."""

            kind               = Attr.Primary
            Kind_Mixins        = (Attr.Init_Only_Mixin, )
            P_Type             = Wireless_Interface
            sort_skip          = True
            ui_allow_new       = False

        # end class hardware

        ### Non-primary attributes

        class standard (_Ancestor.standard) :

            kind               = Attr.Query
            auto_up_depends    = ("hardware", )
            query              = Q.hardware.standard

        # end class standard

        class txpower (_Ancestor.txpower) :

            kind               = Attr.Query
            auto_up_depends    = ("hardware", )
            query              = Q.hardware.txpower

        # end class power

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_left (Pred.Condition) :
            """`left` must be equal to `hardware.left`"""

            kind               = Pred.Object
            assertion          = "left is hardware.left"
            attributes         = ("left", "hardware.left")

        # end class valid_left

    # end class _Predicates

# end class Virtual_Wireless_Interface

if __name__ != "__main__" :
    CNDB.OMP._Export ("*", "_Wireless_Interface_")
### __END__ CNDB.OMP.Wireless_Interface
