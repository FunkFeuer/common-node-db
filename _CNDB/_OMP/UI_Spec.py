# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the repository CNDB.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.UI_Spec
#
# Purpose
#    UI specification for E_Types defined by CNDB.OMP
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `Node_has_Net_Device`
#    10-May-2012 (CT) Add `Wired_Interface`, `Wired_Link`, and `Wireless_Link`
#    19-Jul-2012 (RS) Add `Person`
#    20-Jul-2012 (RS) Add `Person_has_Node`
#    20-Aug-2012 (RS) Add `Wireless_Standard`, `Wireless_Channel`,
#                     `Regulatory_Domain`, `Regulatory_Permission`,
#                     `Wireless_Interface_uses_Wireless_Channel`
#    06-Sep-2012 (RS) Remove `Node_has_Net_Device`
#    12-Sep-2012 (RS) Add `Nickname` and `Person_mentors_Person`
#    18-Sep-2012 (RS) Remove `Subject_owns_Node`
#    11-Oct-2012 (RS) `Nickname` from `PAP`
#     7-Dec-2012 (RS) Add Spec for `Antenna_Type`
#    17-Dec-2012 (RS) Add Specs for `Antenna` and `Net_Device`
#    17-Dec-2012 (RS) Add `list_display` for `Wireless_Interface`
#    17-Dec-2012 (CT) Remove `Wireless_Mode`
#    26-Feb-2013 (CT) Remove `Wired_Link` and `Wireless_Link`
#    26-Feb-2013 (CT) Add `Virtual_Wireless_Interface`
#    27-Feb-2013 (CT) Remove `hardware.left` from
#                     `Virtual_Wireless_Interface.list_display`
#    24-Apr-2013 (CT) Add `virtual_wireless_interfaces` to
#                     `Net_Device...include_links`
#     7-May-2013 (RS) Add IPv6 related classes
#     8-May-2013 (RS) Add `channels` to `Spec.Entity` for `Wireless_Interface`
#    27-Aug-2014 (CT) Replace `GTW.AFS` specification by `MF3_Form_Spec`
#    23-Sep-2014 (CT) Add `IP[46]_Pool`
#     6-Apr-2015 (CT) Use `id_entity_select` for `Wireless_Channel.left`,
#                     `Wireless_Interface.standard`
#     6-Apr-2015 (CT) Use `id_entity_select` for `Antenna.left`,
#                     `Net_Device.left`
#     1-Jun-2015 (CT) Enable `Net_Interface_in_IP[46]_Network`
#    16-Dec-2015 (CT) Change to `UI_Spec`
#    ««revision-date»»···
#--

from   _CNDB                    import CNDB
from   _TFL                     import TFL

import _CNDB._OMP

import _TFL.Sorted_By

class UI_Spec (object) :
    """UI specification for E_Types defined by CNDB.OMP."""

    Antenna               = dict \
        ( list_display    = ("left", "name", "gain")
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("interface", )
            )
        , MF3_Attr_Spec        = dict
            ( left             = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Antenna_Type          = dict \
        ( MF3_Form_Spec        = dict
            ( include_rev_refs = ("bands", )
            )
        )

    Firmware_Binary       = dict \
        (
        )

    Firmware_Bundle       = dict \
        (
        )

    Firmware_Type         = dict \
        (
        )

    Firmware_Version      = dict \
        (
        )

    IP_Network            = dict \
        (
        )

    IP4_Network           = dict \
        (
        )

    IP6_Network           = dict \
        (
        )

    IP4_Pool              = dict \
        (
        )

    IP6_Pool              = dict \
        (
        )

    Net_Credentials       = dict \
        (
        )

    Net_Device            = dict \
        ( MF3_Form_Spec        = dict
            ( include_rev_refs =
                ( "wired_interfaces"
                , "wireless_interfaces"
                , "virtual_wireless_interfaces"
                )
            )
        , MF3_Attr_Spec        = dict
            ( left             = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Net_Device_Type       = dict \
        (
        )

    Net_Interface         = dict \
        (
        )

    Nickname              = dict \
        (
        )

    Node                  = dict \
        (
        )

    Person                = dict \
        (
        )

    Regulatory_Domain     = dict \
        (
        )

    Regulatory_Permission = dict \
        (
        )

    Routing_Zone          = dict \
        (
        )

    Virtual_Wireless_Interface = dict \
        ( list_display    =
            ("hardware", "mac_address", "name", "is_active")
        )

    Wired_Interface       = dict \
        (
        )

    Wireless_Channel      = dict \
        ( MF3_Attr_Spec        = dict
            ( left             = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Wireless_Interface    = dict \
        ( list_display    =
            ("left", "mac_address", "name", "standard", "is_active")
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("antennas", "channels")
            )
        , MF3_Attr_Spec        = dict
            ( standard         = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Wireless_Standard     = dict \
        (
        )

    Zone                  = dict \
        (
        )

    IP4_Pool_permits_Group    = dict \
        (
        )

    IP6_Pool_permits_Group    = dict \
        (
        )

    Net_Interface_in_IP4_Network = dict \
        (
        )

    Net_Interface_in_IP6_Network = dict \
        (
        )

    if False :
        Device_Type_made_by_Company = dict \
            (
            )

        Person_mentors_Person = dict \
            (
            )

        Wireless_Interface_uses_Antenna = dict \
            (
            )

        Wireless_Interface_uses_Wireless_Channel = dict \
            (
            )

# end class UI_Spec

if __name__ != "__main__" :
    CNDB.OMP._Export ("UI_Spec")
### __END__ CNDB.OMP.UI_Spec
