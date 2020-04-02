# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.__test__.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.__test__.fixtures
#
# Purpose
#    fixtures for e.g. testing REST api
#
# Revision Dates
#     8-Jan-2013 (RS) Creation
#     1-Feb-2013 (RS) Fix rounding error with python2.6
#     5-Mar-2013 (CT) Adapt to signature change of `Net_Interface_in_IP_Network`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    ««revision-date»»···
#--

from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP         import PAP

def create (scope) :
    CNDB = scope.CNDB
    PAP = scope.PAP
    Adr = CNDB.IP4_Network.net_address.P_Type
    mgr = PAP.Person \
        (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    node1 = CNDB.Node (name = "nogps", manager = mgr, raw = True)
    gps1 = dict (lat = "48 d 15 m", lon = "15 d 52 m 27.84 s")
    node2 = CNDB.Node \
        (name = "node2", manager = mgr, position = gps1, raw = True)
    net = CNDB.IP4_Network ('192.168.23.0/24', raw = True)
    a1  = net.reserve ('192.168.23.1/32')
    a2  = net.reserve (Adr ('192.168.23.2/32'))
    a3  = net.reserve ('192.168.23.3/32')
    a4  = net.reserve (Adr ('192.168.23.4/32'))
    devtype = CNDB.Net_Device_Type.instance_or_new \
        (name = 'Generic', raw = True)
    dev = CNDB.Net_Device \
        (left = devtype, node = node2, name = 'dev', raw = True)
    wr  = CNDB.Wired_Interface (left = dev, name = 'wr', raw = True)
    wl  = CNDB.Wireless_Interface (left = dev, name = 'wl', raw = True)
    ir1 = CNDB.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    il1 = CNDB.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    ir2 = CNDB.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    il2 = CNDB.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)
# end def create

def net_fixtures (scope) :
    """ Create more fixtures for testing IP allocation and polymorphic
        queries on owner.
    """
    create (scope)
    scope.commit ()
    CNDB   = scope.CNDB
    PAP   = scope.PAP
    cta   = PAP.Person \
        (first_name = 'Christian', last_name = 'Tanzer', raw = True)
    dtype = CNDB.Net_Device_Type.instance (name = 'Generic', raw = True)
    rsc   = PAP.Person.query (first_name = 'ralf').one ()
    swing = PAP.Company (name = "Swing")
    ff    = PAP.Association (name = "Funkfeuer")
    n1    = CNDB.Node \
        (name = "Node-net1", manager = cta, owner = swing, raw = True)
    n2    = CNDB.Node (name = "Node-net2", manager = cta, owner = ff, raw = True)
    n3    = CNDB.Node (name = "Node-net3", manager = rsc, owner = ff, raw = True)
    n4    = CNDB.Node (name = "Node-net4", manager = rsc, raw = True)
    net   = CNDB.IP4_Network \
        (net_address = '10.10.0.0/16', owner = ff, raw = True)
    nv6   = CNDB.IP6_Network ('2001:db8::/32', owner = swing, raw = True)
    n1d1  = CNDB.Net_Device \
        (left = dtype, node = n1, name = 'n1d1', raw = True)
    n1d2  = CNDB.Net_Device \
        (left = dtype, node = n1, name = 'n1d2', raw = True)
    n2d1  = CNDB.Net_Device \
        (left = dtype, node = n2, name = 'n2d1', raw = True)
    n2d2  = CNDB.Net_Device \
        (left = dtype, node = n2, name = 'n2d2', raw = True)
    n2d3  = CNDB.Net_Device \
        (left = dtype, node = n2, name = 'n2d3', raw = True)
    n3d1  = CNDB.Net_Device \
        (left = dtype, node = n3, name = 'n3d1', raw = True)
    n4d1  = CNDB.Net_Device \
        (left = dtype, node = n4, name = 'n4d1', raw = True)
    n4d2  = CNDB.Net_Device \
        (left = dtype, node = n4, name = 'n4d2', raw = True)
    n4d3  = CNDB.Net_Device \
        (left = dtype, node = n4, name = 'n4d3', raw = True)
    n4d4  = CNDB.Net_Device \
        (left = dtype, node = n4, name = 'n4d4', raw = True)
    n4d5  = CNDB.Net_Device \
        (left = dtype, node = n4, name = 'n4d5', raw = True)
# end def net_fixtures

### __END__ CNDB.OMP.__test__.fixtures
