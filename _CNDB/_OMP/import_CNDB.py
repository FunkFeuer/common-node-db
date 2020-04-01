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
#    CNDB.OMP.import_CNDB
#
# Purpose
#    Import CNDB object model
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `Node_has_Net_Device`, `Wired_Interface`, `Net_Link`
#    20-Aug-2012 (RS) Add `Wireless_Standard`, `Wireless_Channel`
#                    `Regulatory_Domain`, `Regulatory_Permission`,
#                    `Wireless_Interface_uses_Wireless_Channel`
#    30-Aug-2012 (RS) `Person_has_Node` -> `Subject_owns_Node`
#    30-Aug-2012 (RS) Remove `Node_has_Net_Device`
#     6-Sep-2012 (CT) Add `IP6_Network`
#    12-Sep-2012 (CT) Add `Nickname` and `Person_mentors_Person`
#    18-Sep-2012 (RS) remove `Subject_owns_Node` (replace by Id_Entity)
#    21-Sep-2012 (RS) Add `Net_Interface_in_IP6_Network`
#    11-Oct-2012 (RS) Import `Nickname` from `PAP` -- not imported by default
#    12-Oct-2012 (RS) Add `Node_has_Address`
#     9-Nov-2012 (RS) Import `IM_Handle` from `PAP`
#     7-Dec-2012 (RS) Add `Antenna_Band`
#    26-Feb-2013 (CT) Remove `Wired_Link` and `Wireless_Link`
#     4-Mar-2013 (CT) Add `GTW.OMP.PAP.Association`
#    28-Apr-2013 (CT) Add `Person_acts_for_Legal_Entity`
#    27-Mar-2014 (CT) Add `MOM.Document`
#     5-Jun-2014 (RS) Remove `Node_has_Address` (it's already in
#                     `refuse_links` of `Node`)
#    13-Jun-2014 (RS) Remove `Person_acts_for_Legal_Entity`,
#                     add `PAP.Adhoc_Group`, `PAP.Person_in_Group`
#    20-Jun-2014 (RS) Add `IP_Pool`, `IP4_Pool`, `IP6_Pool`
#     1-Jul-2014 (RS) `IP_DNS_Alias` and derivatives
#     3-Jul-2014 (RS) Add `IP_Network_in_IP_Pool`, `IP_Pool_permits_Group`
#                     and descendants
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

import _GTW._OMP._PAP.Association
import _GTW._OMP._PAP.IM_Handle
import _GTW._OMP._PAP.Nickname
import _GTW._OMP._PAP.Adhoc_Group
import _GTW._OMP._PAP.Person_in_Group
import _GTW._OMP._PAP.Id_Entity_permits_Group

import _CNDB._OMP.Antenna
import _CNDB._OMP.Antenna_Band
import _CNDB._OMP.Antenna_Type
import _CNDB._OMP.Device
import _CNDB._OMP.Device_Type
import _CNDB._OMP.Firmware
import _CNDB._OMP.IP4_DNS_Alias
import _CNDB._OMP.IP4_Network
import _CNDB._OMP.IP4_Pool
import _CNDB._OMP.IP6_DNS_Alias
import _CNDB._OMP.IP6_Network
import _CNDB._OMP.IP6_Pool
import _CNDB._OMP.IP_DNS_Alias
import _CNDB._OMP.IP_Network
import _CNDB._OMP.IP_Pool
import _CNDB._OMP.Net_Credentials
import _CNDB._OMP.Net_Device
import _CNDB._OMP.Net_Device_Type
import _CNDB._OMP.Net_Interface
import _CNDB._OMP.Node
import _CNDB._OMP.Regulatory_Domain
import _CNDB._OMP.Regulatory_Permission
import _CNDB._OMP.Routing_Zone
import _CNDB._OMP.Wired_Interface
import _CNDB._OMP.Wireless_Channel
import _CNDB._OMP.Wireless_Interface
import _CNDB._OMP.Wireless_Standard

import _CNDB._OMP.Wireless_Mode
import _CNDB._OMP.Zone

import _CNDB._OMP.Device_Type_made_by_Company
import _CNDB._OMP.IP_Network_in_IP_Pool
import _CNDB._OMP.IP4_Network_in_IP4_Pool
import _CNDB._OMP.IP6_Network_in_IP6_Pool
import _CNDB._OMP.IP_Pool_permits_Group
import _CNDB._OMP.IP4_Pool_permits_Group
import _CNDB._OMP.IP6_Pool_permits_Group
import _CNDB._OMP.Net_Interface_in_IP4_Network
import _CNDB._OMP.Net_Interface_in_IP6_Network
import _CNDB._OMP.Net_Interface_in_IP_Network
import _CNDB._OMP.Net_Link
import _CNDB._OMP.Person_mentors_Person
import _CNDB._OMP.Wireless_Interface_uses_Antenna
import _CNDB._OMP.Wireless_Interface_uses_Wireless_Channel

import _MOM.Document

### __END__ CNDB.OMP.import_CNDB
