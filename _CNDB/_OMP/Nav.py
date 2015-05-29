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
#    CNDB.OMP.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
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
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL                     import TFL
from   _CNDB                    import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP           import PAP

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Antenna               = dict \
        ( ETM             = "CNDB.OMP.Antenna"
        , list_display    = ("left", "name", "gain")
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("interface", )
            )
        , MF3_Attr_Spec        = dict
            ( left             = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Antenna_Type          = dict \
        ( ETM             = "CNDB.OMP.Antenna_Type"
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("bands", )
            )
        )

    Firmware_Binary       = dict \
        ( ETM             = "CNDB.OMP.Firmware_Binary"
        )

    Firmware_Bundle       = dict \
        ( ETM             = "CNDB.OMP.Firmware_Bundle"
        )

    Firmware_Type         = dict \
        ( ETM             = "CNDB.OMP.Firmware_Type"
        )

    Firmware_Version      = dict \
        ( ETM             = "CNDB.OMP.Firmware_Version"
        )

    IP_Network            = dict \
        ( ETM             = "CNDB.OMP.IP_Network"
        )

    IP4_Network           = dict \
        ( ETM             = "CNDB.OMP.IP4_Network"
        )

    IP6_Network           = dict \
        ( ETM             = "CNDB.OMP.IP6_Network"
        )

    IP4_Pool              = dict \
        ( ETM             = "CNDB.OMP.IP4_Pool"
        )

    IP6_Pool              = dict \
        ( ETM             = "CNDB.OMP.IP6_Pool"
        )

    Net_Credentials       = dict \
        ( ETM             = "CNDB.OMP.Net_Credentials"
        )

    Net_Device            = dict \
        ( ETM             = "CNDB.OMP.Net_Device"
        , MF3_Form_Spec        = dict
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
        ( ETM             = "CNDB.OMP.Net_Device_Type"
        )

    Net_Interface         = dict \
        ( ETM             = "CNDB.OMP.Net_Interface"
        )

    Nickname              = dict \
        ( ETM             = "PAP.Nickname"
        )

    Node                  = dict \
        ( ETM             = "CNDB.OMP.Node"
        )

    Person                = dict \
        ( ETM             = "PAP.Person"
        )

    Regulatory_Domain     = dict \
        ( ETM             = "CNDB.OMP.Regulatory_Domain"
        )

    Regulatory_Permission = dict \
        ( ETM             = "CNDB.OMP.Regulatory_Permission"
        )

    Routing_Zone          = dict \
        ( ETM             = "CNDB.OMP.Routing_Zone"
        )

    Virtual_Wireless_Interface = dict \
        ( ETM             = "CNDB.OMP.Virtual_Wireless_Interface"
        , list_display    =
            ("hardware", "mac_address", "name", "is_active")
        )

    Wired_Interface       = dict \
        ( ETM             = "CNDB.OMP.Wired_Interface"
        )

    Wireless_Channel      = dict \
        ( ETM             = "CNDB.OMP.Wireless_Channel"
        , MF3_Attr_Spec        = dict
            ( left             = dict
                (input_widget = "mf3_input, id_entity_select")
            )
        )

    Wireless_Interface    = dict \
        ( ETM             = "CNDB.OMP.Wireless_Interface"
        , list_display    =
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
        ( ETM             = "CNDB.OMP.Wireless_Standard"
        )

    Zone                  = dict \
        ( ETM             = "CNDB.OMP.Zone"
        )

    IP4_Pool_permits_Group    = dict \
        ( ETM                 = "CNDB.OMP.IP4_Pool_permits_Group"
        )

    IP6_Pool_permits_Group    = dict \
        ( ETM                 = "CNDB.OMP.IP6_Pool_permits_Group"
        )

    Net_Interface_in_IP4_Network = dict \
        ( ETM            = "CNDB.OMP.Net_Interface_in_IP4_Network"
        )

    Net_Interface_in_IP6_Network = dict \
        ( ETM            = "CNDB.OMP.Net_Interface_in_IP6_Network"
        )

    if False :
        Device_Type_made_by_Company = dict \
            ( ETM            = "CNDB.OMP.Device_Type_made_by_Company"
            )

        Person_mentors_Person = dict \
            ( ETM            = "CNDB.OMP.Person_mentors_Person"
            )

        Wireless_Interface_uses_Antenna = dict \
            ( ETM            = "CNDB.OMP.Wireless_Interface_uses_Antenna"
            )

        Wireless_Interface_uses_Wireless_Channel = dict \
            ( ETM            = "CNDB.OMP.Wireless_Interface_uses_Wireless_Channel"
            )

# end class Admin

if __name__ != "__main__" :
    CNDB.OMP._Export_Module ()
### __END__ CNDB.OMP.Nav
