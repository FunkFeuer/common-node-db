# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.__test__.IP_Network
#
# Purpose
#    Test IP_Network
#
# Revision Dates
#    26-Jan-2013 (CT) Creation
#     4-Mar-2013 (CT) Add tests for `allocate`
#     5-Mar-2013 (CT) Add tests for `reserve`
#     5-Mar-2013 (CT) Add `electric`
#     7-Mar-2013 (RS) Test for previously failing `CONTAINS` query
#    19-Mar-2013 (CT) Add test case `test_AQ`
#    22-Mar-2013 (CT) Add test for `Query_Restriction`
#    28-Mar-2013 (CT) Add `AQ.Attrs_Transitive...ui_name`, `.pool.pool.pool...`
#    11-Apr-2013 (CT) Adapt to changes in `MOM.Attr.Querier`
#    28-Apr-2013 (CT) Adapt to addition of `IP_Network.desc`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    13-Aug-2013 (CT) Add `test_order`, adapt other tests to change in order
#    22-Aug-2013 (CT) Add tests for I4N and I6N calls with wrong `raw` value
#     7-Oct-2013 (CT) Add tests for `belongs_to_node`
#     8-Apr-2014 (RS) Test failing allocation in sub-pool
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    25-Apr-2014 (RS) Add `_test_partial`
#    13-Jun-2014 (RS) Fixes for new `PAP` objects, renaming of
#                     `IP_Network.cool_down`, `Node` no longer derived
#                     from `Subject`, addition of `Node.desc`, `ui_name`
#                     for `desc`
#    14-Jun-2014 (RS) Add `node` to `IP_Network`
#    20-Jun-2014 (RS) `IP_Pool` and derivatives, `node` moved to `IP_Pool`
#    20-Jun-2014 (RS) Add failing allocation test: Don't allocate from a
#                     sub-pool
#    20-Jun-2014 (RS) Re-add `IP_Network.pool`, make failing test pass
#    23-Jun-2014 (RS) Add tests for `free` and `collect_garbage`, make
#                     tests run again
#    24-Jun-2014 (RS) `A_Netmask_Interval` derived from `A_Int_Interval_C`
#     4-Jul-2014 (RS) `IP_Pool_permits_Group`, `IP_Network_in_IP_Pool`,
#                     changes to `IP_Pool`
#    11-Jul-2014 (CT) Add tests to `_test_partial`; clear ballast from it
#     5-Sep-2014 (RS) Garbage collector now frees networks with maximum
#                     netmask, to avoid garbage collection now all IPs
#                     have an associated `Net_Interface`.
#    12-Mar-2015 (CT) Adapt to sqlalchemy 0.9.8
#    12-Mar-2015 (CT) Fix backend dependent tests
#    19-Mar-2018 (CT) Use `expect_except` (Python-3 compatibility)
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _CNDB._OMP.__test__.model      import *
from   datetime                 import datetime

import _GTW._RST._TOP._MOM.Query_Restriction

from _MOM._Attr.Date_Time_Delta import A_Date_Time_Delta

from _CNDB._OMP.__test__.fixtures import net_fixtures, create as std_fixtures

_test_alloc = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> Adr = CNDB.IP4_Network.net_address.P_Type

    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> mg  = PAP.Person ("Glueck", "Martin", raw = True)
    >>> ak  = PAP.Person ("Kaplan", "Aaron", raw = True)
    >>> rs  = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> ct  = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> lt  = PAP.Person ("Tanzer", "Laurens", raw = True)
    >>> osc = PAP.Company ("Open Source Consulting", raw = True)

    >>> nod = CNDB.Node (name = "Test-Node", manager = ff, raw = True)
    >>> dt  = CNDB.Net_Device_Type (name = "Generic", raw = True)
    >>> dev = CNDB.Net_Device (left = dt, node = nod, name = "dev", raw = True)
    >>> ifc = CNDB.Wired_Interface (left = dev, name = "iface", raw = True)

    >>> ETM = scope.CNDB.IP4_Network
    >>> show_networks (scope, ETM) ### nothing allocated yet

    >>> ff_pool  = CNDB.IP4_Network ('10.0.0.0/8', owner = ff, raw = True)
    >>> show_networks (scope, ETM) ### 10.0.0.0/8
    10.0.0.0/8         Funkfeuer                : electric = F, children = F

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 1

    >>> osc_pool = ff_pool.allocate (16, osc)
    >>> show_networks (scope, ETM) ### 10.0.0.0/16
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/11       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 17

    >>> rs_pool = osc_pool.allocate (28, rs)
    >>> rs_pool.net_address
    10.0.0.0/28

    >>> show_networks (scope, ETM, pool = osc_pool) ### 10.0.0.0/28
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F

    >>> with expect_except (CNDB.OMP.Error.Address_Already_Used) :
    ...   ct_addr = osc_pool.reserve ('10.0.0.1/32', owner = ct)
    Address_Already_Used: Address 10.0.0.1 already in use by 'Schlatterbeck Ralf'

    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/28
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = F

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 41

    >>> ct_pool = rs_pool.allocate (30, ct)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/30 ct
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.4/30        Schlatterbeck Ralf       : electric = T, children = F
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> with expect_except (CNDB.OMP.Error.No_Free_Address_Range) :
    ...   ak_pool = rs_pool.allocate (28, ak)
    No_Free_Address_Range: Address range [10.0.0.0/28] of this IP4_Network doesn't contain a free subrange for mask length 28

    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/30 ct after alloc error
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.4/30        Schlatterbeck Ralf       : electric = T, children = F
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> for a, m in ETM.query (Q.net_address.IN (rs_pool.net_address), sort_key = TFL.Sorted_By ("-net_address.mask_len", "net_address")).attrs ("net_address", "net_address.mask_len") :
    ...     print (a, m)
    10.0.0.0/30 30
    10.0.0.4/30 30
    10.0.0.0/29 29
    10.0.0.8/29 29
    10.0.0.0/28 28

    >>> ak_pool = rs_pool.allocate (30, ak)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.4/30 ct+ak
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 45

    >>> mg_pool = rs_pool.allocate (29, mg)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.8/29
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T

    >>> with expect_except (CNDB.OMP.Error.No_Free_Address_Range) :
    ...   xx_pool = rs_pool.allocate (30, mg)
    No_Free_Address_Range: Address range [10.0.0.0/28] of this IP4_Network doesn't contain a free subrange for mask length 30

    >>> with expect_except (CNDB.OMP.Error.No_Free_Address_Range) :
    ...   yy_pool = mg_pool.allocate (29, mg)
    No_Free_Address_Range: Address range [10.0.0.8/29] of this IP4_Network doesn't contain a free subrange for mask length 29

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 45

    >>> mg_addr = ct_pool.reserve ('10.0.0.1/32', owner = mg)
    >>> ni = CNDB.Net_Interface_in_IP_Network (ifc, mg_addr, mask_len = 32)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.1/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.0           Tanzer Christian         : electric = T, children = F
    10.0.0.2/31        Tanzer Christian         : electric = T, children = F

    >>> lt_addr = ct_pool.reserve ('10.0.0.2/32', owner = lt)
    >>> ni = CNDB.Net_Interface_in_IP_Network (ifc, lt_addr, mask_len = 32)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.2/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.0           Tanzer Christian         : electric = T, children = F
    10.0.0.3           Tanzer Christian         : electric = T, children = F

    >>> rs_addr = ct_pool.reserve ('10.0.0.0/32', owner = rs)
    >>> ni = CNDB.Net_Interface_in_IP_Network (ifc, rs_addr, mask_len = 32)
    >>> rs_addr.pool
    CNDB.IP4_Network ("10.0.0.0/30")
    >>> ct_addr = ct_pool.reserve (Adr ('10.0.0.3/32'), owner = ct)
    >>> ni = CNDB.Net_Interface_in_IP_Network (ifc, ct_addr, mask_len = 32)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.3/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T

    >>> mg_pool_2 = mg_pool.allocate (30, mg)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.8/30
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F

    >>> ct_addr2 = ff_pool.reserve (Adr ('10.42.137.1/32'), owner = ct)
    >>> ni = CNDB.Net_Interface_in_IP_Network (ifc, ct_addr2, mask_len = 32)
    >>> show_networks (scope, ETM) ### 10.42.137.1/32
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.32.0.0/11       Funkfeuer                : electric = T, children = T
    10.32.0.0/12       Funkfeuer                : electric = T, children = T
    10.40.0.0/13       Funkfeuer                : electric = T, children = T
    10.40.0.0/14       Funkfeuer                : electric = T, children = T
    10.42.0.0/15       Funkfeuer                : electric = T, children = T
    10.42.0.0/16       Funkfeuer                : electric = T, children = T
    10.42.128.0/17     Funkfeuer                : electric = T, children = T
    10.42.128.0/18     Funkfeuer                : electric = T, children = T
    10.42.128.0/19     Funkfeuer                : electric = T, children = T
    10.42.128.0/20     Funkfeuer                : electric = T, children = T
    10.42.136.0/21     Funkfeuer                : electric = T, children = T
    10.42.136.0/22     Funkfeuer                : electric = T, children = T
    10.42.136.0/23     Funkfeuer                : electric = T, children = T
    10.42.137.0/24     Funkfeuer                : electric = T, children = T
    10.42.137.0/25     Funkfeuer                : electric = T, children = T
    10.42.137.0/26     Funkfeuer                : electric = T, children = T
    10.42.137.0/27     Funkfeuer                : electric = T, children = T
    10.42.137.0/28     Funkfeuer                : electric = T, children = T
    10.42.137.0/29     Funkfeuer                : electric = T, children = T
    10.42.137.0/30     Funkfeuer                : electric = T, children = T
    10.42.137.0/31     Funkfeuer                : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/13       Funkfeuer                : electric = T, children = F
    10.40.0.0/15       Funkfeuer                : electric = T, children = F
    10.42.0.0/17       Funkfeuer                : electric = T, children = F
    10.42.128.0/21     Funkfeuer                : electric = T, children = F
    10.42.136.0/24     Funkfeuer                : electric = T, children = F
    10.42.137.0        Funkfeuer                : electric = T, children = F
    10.42.137.2/31     Funkfeuer                : electric = T, children = F
    10.42.137.4/30     Funkfeuer                : electric = T, children = F
    10.42.137.8/29     Funkfeuer                : electric = T, children = F
    10.42.137.16/28    Funkfeuer                : electric = T, children = F
    10.42.137.32/27    Funkfeuer                : electric = T, children = F
    10.42.137.64/26    Funkfeuer                : electric = T, children = F
    10.42.137.128/25   Funkfeuer                : electric = T, children = F
    10.42.138.0/23     Funkfeuer                : electric = T, children = F
    10.42.140.0/22     Funkfeuer                : electric = T, children = F
    10.42.144.0/20     Funkfeuer                : electric = T, children = F
    10.42.160.0/19     Funkfeuer                : electric = T, children = F
    10.42.192.0/18     Funkfeuer                : electric = T, children = F
    10.43.0.0/16       Funkfeuer                : electric = T, children = F
    10.44.0.0/14       Funkfeuer                : electric = T, children = F
    10.48.0.0/12       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope, ETM)
    CNDB.IP4_Network count: 95

    >>> ETM = CNDB.IP4_Network
    >>> q   = ETM.query
    >>> n   = '10.42.137.0/28'
    >>> q (Q.net_address.IN (n)).count ()
    9

    >>> s = TFL.Sorted_By ("-net_address.mask_len")
    >>> q (Q.net_address.CONTAINS (n), sort_key = s).first ()
    CNDB.IP4_Network ("10.42.137.0/28")

    >>> with expect_except (CNDB.OMP.Error.Cannot_Free_Network) :
    ...   ff_pool.free ()
    Cannot_Free_Network: Cannot free toplevel network 10.0.0.0/8
    >>> with expect_except (CNDB.OMP.Error.Cannot_Free_Network) :
    ...   rs_pool.free ()
    Cannot_Free_Network: Cannot free network with allocations: 10.0.0.0/28

    >>> p1 = CNDB.IP4_Pool \\
    ...     ( name             = "ff_pool"
    ...     , cool_down_period = '1w'
    ...     , netmask_interval = '0-32'
    ...     , raw              = True
    ...     )
    >>> i1 = CNDB.IP4_Network_in_IP4_Pool (ff_pool, p1)
    >>> p2 = CNDB.IP4_Pool \\
    ...     ( name             = "osc_pool"
    ...     , netmask_interval = '0-32'
    ...     , raw              = True
    ...     )
    >>> i2 = CNDB.IP4_Network_in_IP4_Pool (osc_pool, p2)
    >>> p3 = CNDB.IP4_Pool \\
    ...     ( name             = "rs_pool"
    ...     , cool_down_period = '1d'
    ...     , netmask_interval = '32-32'
    ...     , raw              = True
    ...     )
    >>> i3 = CNDB.IP4_Network_in_IP4_Pool (rs_pool, p3)

    >>> CNDB.IP4_Network_in_IP4_Pool.query \\
    ...     ( Q.ip_network.net_address.CONTAINS (rs_pool.net_address)
    ...     , Q.ip_pool.cool_down_period != None
    ...     , sort_key = TFL.Sorted_By ("ip_pool.cool_down_period")
    ...     ).distinct ().all ()
    [CNDB.IP4_Network_in_IP4_Pool (("10.0.0.0/28", ), ('rs_pool', )), CNDB.IP4_Network_in_IP4_Pool (("10.0.0.0/8", ), ('ff_pool', ))]

    >>> IPP_ETM = rs_pool.home_scope [rs_pool.ETM.ip_pool.P_Type]
    >>> print (IPP_ETM.type_name)
    CNDB.IP4_Pool

    >>> IPPL_ETM = rs_pool.home_scope [rs_pool.ETM.ip_pool_link.P_Type]
    >>> print (IPPL_ETM.type_name)
    CNDB.IP4_Network_in_IP4_Pool

    >>> IPPL_ETM = CNDB.IP4_Network_in_IP4_Pool
    >>> IPPL_ETM.query \\
    ...     ( Q.ip_network.net_address.CONTAINS (rs_pool.net_address)
    ...     , Q.ip_pool.cool_down_period != None
    ...     , sort_key = TFL.Sorted_By ("ip_pool.cool_down_period")
    ...     ).first ()
    CNDB.IP4_Network_in_IP4_Pool (("10.0.0.0/28", ), ('rs_pool', ))

    >>> CNDB.IP4_Network_in_IP4_Pool.query \\
    ...     ( Q.ip_network.net_address.CONTAINS (rs_pool.net_address)
    ...     , Q.ip_pool.cool_down_period != None
    ...     , sort_key = TFL.Sorted_By ("ip_pool.cool_down_period")
    ...     ).distinct ().all ()
    [CNDB.IP4_Network_in_IP4_Pool (("10.0.0.0/28", ), ('rs_pool', )), CNDB.IP4_Network_in_IP4_Pool (("10.0.0.0/8", ), ('ff_pool', ))]

    >>> CNDB.IP4_Network_in_IP4_Pool.query \\
    ...     ( Q.ip_network.net_address.CONTAINS (rs_pool.net_address)
    ...     , sort_key = TFL.Sorted_By ("ip_pool.cool_down_period")
    ...     ).distinct ().count ()
    3

    >>> print ("mg_addr", mg_addr)
    mg_addr ("10.0.0.1")
    >>> mg_addr.free ()
    >>> mg_addr.net_interface_link
    >>> print ("lt_addr", lt_addr)
    lt_addr ("10.0.0.2")
    >>> lt_addr.free ()
    >>> lt_addr.net_interface_link
    >>> print ("rs_addr", rs_addr, rs_addr.pool)
    rs_addr ("10.0.0.0") ("10.0.0.0/30")
    >>> rs_addr.free ()
    >>> rs_addr.net_interface_link
    >>> print ("mg_pool_2", mg_pool_2)
    mg_pool_2 ("10.0.0.8/30")
    >>> mg_pool_2.free ()
    >>> print ("ct_addr", ct_addr)
    ct_addr ("10.0.0.3")
    >>> ct_addr.free ()
    >>> ct_addr.net_interface_link
    >>> lt_addr.net_interface_link
    >>> print ("lt_addr", lt_addr)
    lt_addr ("10.0.0.2")
    >>> lt_addr.free ()
    >>> print ("mg_addr", mg_addr)
    mg_addr ("10.0.0.1")
    >>> mg_addr.net_interface_link
    >>> mg_addr.free ()
    >>> print ("ct_pool", ct_pool)
    ct_pool ("10.0.0.0/30")
    >>> ct_pool.free ()
    >>> print ("ak_pool", ak_pool)
    ak_pool ("10.0.0.4/30")
    >>> ak_pool.free ()
    >>> print ("mg_pool", mg_pool)
    mg_pool ("10.0.0.8/29")
    >>> mg_pool.free ()
    >>> print ("rs_pool", rs_pool)
    rs_pool ("10.0.0.0/28")
    >>> rs_pool.free ()
    >>> print ("ct_addr2", ct_addr2)
    ct_addr2 ("10.42.137.1")

    # Don't free but destroy link. Picked up by garbage collector
    >>> ct_addr2.net_interface_link.destroy ()

    >>> show_networks (scope, ETM) # After free
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        expiring                 : electric = F, children = T
    10.0.0.0/30        expiring                 : electric = F, children = T
    10.0.0.8/29        expiring                 : electric = F, children = T
    10.0.0.0           expiring                 : electric = F, children = F
    10.0.0.1           expiring                 : electric = F, children = F
    10.0.0.2           expiring                 : electric = F, children = F
    10.0.0.3           expiring                 : electric = F, children = F
    10.0.0.4/30        expiring                 : electric = F, children = F
    10.0.0.8/30        expiring                 : electric = F, children = F
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.32.0.0/11       Funkfeuer                : electric = T, children = T
    10.32.0.0/12       Funkfeuer                : electric = T, children = T
    10.40.0.0/13       Funkfeuer                : electric = T, children = T
    10.40.0.0/14       Funkfeuer                : electric = T, children = T
    10.42.0.0/15       Funkfeuer                : electric = T, children = T
    10.42.0.0/16       Funkfeuer                : electric = T, children = T
    10.42.128.0/17     Funkfeuer                : electric = T, children = T
    10.42.128.0/18     Funkfeuer                : electric = T, children = T
    10.42.128.0/19     Funkfeuer                : electric = T, children = T
    10.42.128.0/20     Funkfeuer                : electric = T, children = T
    10.42.136.0/21     Funkfeuer                : electric = T, children = T
    10.42.136.0/22     Funkfeuer                : electric = T, children = T
    10.42.136.0/23     Funkfeuer                : electric = T, children = T
    10.42.137.0/24     Funkfeuer                : electric = T, children = T
    10.42.137.0/25     Funkfeuer                : electric = T, children = T
    10.42.137.0/26     Funkfeuer                : electric = T, children = T
    10.42.137.0/27     Funkfeuer                : electric = T, children = T
    10.42.137.0/28     Funkfeuer                : electric = T, children = T
    10.42.137.0/29     Funkfeuer                : electric = T, children = T
    10.42.137.0/30     Funkfeuer                : electric = T, children = T
    10.42.137.0/31     Funkfeuer                : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/13       Funkfeuer                : electric = T, children = F
    10.40.0.0/15       Funkfeuer                : electric = T, children = F
    10.42.0.0/17       Funkfeuer                : electric = T, children = F
    10.42.128.0/21     Funkfeuer                : electric = T, children = F
    10.42.136.0/24     Funkfeuer                : electric = T, children = F
    10.42.137.0        Funkfeuer                : electric = T, children = F
    10.42.137.2/31     Funkfeuer                : electric = T, children = F
    10.42.137.4/30     Funkfeuer                : electric = T, children = F
    10.42.137.8/29     Funkfeuer                : electric = T, children = F
    10.42.137.16/28    Funkfeuer                : electric = T, children = F
    10.42.137.32/27    Funkfeuer                : electric = T, children = F
    10.42.137.64/26    Funkfeuer                : electric = T, children = F
    10.42.137.128/25   Funkfeuer                : electric = T, children = F
    10.42.138.0/23     Funkfeuer                : electric = T, children = F
    10.42.140.0/22     Funkfeuer                : electric = T, children = F
    10.42.144.0/20     Funkfeuer                : electric = T, children = F
    10.42.160.0/19     Funkfeuer                : electric = T, children = F
    10.42.192.0/18     Funkfeuer                : electric = T, children = F
    10.43.0.0/16       Funkfeuer                : electric = T, children = F
    10.44.0.0/14       Funkfeuer                : electric = T, children = F
    10.48.0.0/12       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> show_networks (scope, ETM, pool = ct_addr2) ### 10.42.137.1
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    >>> mg_pool.collect_garbage ()
    >>> show_networks (scope, ETM, pool = ct_addr2) ### 10.42.137.1
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    >>> ff_pool.collect_garbage ()
    >>> show_networks (scope, ETM, pool = ct_addr2) ### 10.42.137.1
    10.42.137.1        expiring                 : electric = F, children = F
    >>> now = datetime.now ()
    >>> ct_addr2.set (expiration_date = now)
    1
    >>> ff_pool.collect_garbage ()
    >>> show_networks (scope, ETM) # After collect_garbage
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        expiring                 : electric = F, children = T
    10.0.0.0/30        expiring                 : electric = F, children = T
    10.0.0.8/29        expiring                 : electric = F, children = T
    10.0.0.0           expiring                 : electric = F, children = F
    10.0.0.1           expiring                 : electric = F, children = F
    10.0.0.2           expiring                 : electric = F, children = F
    10.0.0.3           expiring                 : electric = F, children = F
    10.0.0.4/30        expiring                 : electric = F, children = F
    10.0.0.8/30        expiring                 : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/11       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> tree_view (ff_pool) ### After collect_garbage
    10.0.0.0/8
     10.0.0.0/9 E
      10.0.0.0/10 E
       10.0.0.0/11 E
        10.0.0.0/12 E
         10.0.0.0/13 E
          10.0.0.0/14 E
           10.0.0.0/15 E
            10.0.0.0/16
             10.0.0.0/17 E
              10.0.0.0/18 E
               10.0.0.0/19 E
                10.0.0.0/20 E
                 10.0.0.0/21 E
                  10.0.0.0/22 E
                   10.0.0.0/23 E
                    10.0.0.0/24 E
                     10.0.0.0/25 E
                      10.0.0.0/26 E
                       10.0.0.0/27 E
                        10.0.0.0/28
                         10.0.0.0/29 E
                          10.0.0.0/30
                           10.0.0.0/31 E
                            10.0.0.0
                            10.0.0.1
                           10.0.0.2/31 E
                            10.0.0.2
                            10.0.0.3
                          10.0.0.4/30
                         10.0.0.8/29
                          10.0.0.8/30
                          10.0.0.12/30 E
                        10.0.0.16/28 E
                       10.0.0.32/27 E
                      10.0.0.64/26 E
                     10.0.0.128/25 E
                    10.0.1.0/24 E
                   10.0.2.0/23 E
                  10.0.4.0/22 E
                 10.0.8.0/21 E
                10.0.16.0/20 E
               10.0.32.0/19 E
              10.0.64.0/18 E
             10.0.128.0/17 E
            10.1.0.0/16 E
           10.2.0.0/15 E
          10.4.0.0/14 E
         10.8.0.0/13 E
        10.16.0.0/12 E
       10.32.0.0/11 E
      10.64.0.0/10 E
     10.128.0.0/9 E

    >>> mg_pool.set (expiration_date = now)
    1
    >>> show_networks (scope, ETM, pool = mg_pool) ### 10.0.0.8/29
    10.0.0.8/29        free                     : electric = F, children = T
    10.0.0.8/30        expiring                 : electric = F, children = F
    10.0.0.12/30       Glueck Martin            : electric = T, children = F

    >>> ff_pool.collect_garbage ()
    >>> tree_view (ff_pool) ### After collect_garbage 2
    10.0.0.0/8
     10.0.0.0/9 E
      10.0.0.0/10 E
       10.0.0.0/11 E
        10.0.0.0/12 E
         10.0.0.0/13 E
          10.0.0.0/14 E
           10.0.0.0/15 E
            10.0.0.0/16
             10.0.0.0/17 E
              10.0.0.0/18 E
               10.0.0.0/19 E
                10.0.0.0/20 E
                 10.0.0.0/21 E
                  10.0.0.0/22 E
                   10.0.0.0/23 E
                    10.0.0.0/24 E
                     10.0.0.0/25 E
                      10.0.0.0/26 E
                       10.0.0.0/27 E
                        10.0.0.0/28
                         10.0.0.0/29 E
                          10.0.0.0/30
                           10.0.0.0/31 E
                            10.0.0.0
                            10.0.0.1
                           10.0.0.2/31 E
                            10.0.0.2
                            10.0.0.3
                          10.0.0.4/30
                         10.0.0.8/29 E
                        10.0.0.16/28 E
                       10.0.0.32/27 E
                      10.0.0.64/26 E
                     10.0.0.128/25 E
                    10.0.1.0/24 E
                   10.0.2.0/23 E
                  10.0.4.0/22 E
                 10.0.8.0/21 E
                10.0.16.0/20 E
               10.0.32.0/19 E
              10.0.64.0/18 E
             10.0.128.0/17 E
            10.1.0.0/16 E
           10.2.0.0/15 E
          10.4.0.0/14 E
         10.8.0.0/13 E
        10.16.0.0/12 E
       10.32.0.0/11 E
      10.64.0.0/10 E
     10.128.0.0/9 E

    >>> ff_pool.ip_pool.set_raw (cool_down_period = '0d')
    1
    >>> ff_pool.collect_garbage ()
    >>> tree_view (ff_pool) ### After collect_garbage 2
    10.0.0.0/8

    >>> ETM = CNDB.IP4_Network
    >>> xpool  = CNDB.IP4_Network ('192.168.0.0/16', owner = ff, raw = True)
    >>> mgpool = xpool.allocate (17, mg)
    >>> ctpool = xpool.allocate (17, ct)
    >>> with expect_except (CNDB.OMP.Error.No_Free_Address_Range) :
    ...   rspool = xpool.allocate (32, rs)
    No_Free_Address_Range: Address range [192.168.0.0/16] of this IP4_Network doesn't contain a free subrange for mask length 32
    >>> ffpool = mgpool.allocate (22, ff)

    >>> with expect_except (CNDB.OMP.Error.No_Free_Address_Range) :
    ...   rspool = xpool.allocate (32, rs)
    No_Free_Address_Range: Address range [192.168.0.0/16] of this IP4_Network doesn't contain a free subrange for mask length 32
"""

_test_alloc_pg = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB

    >>> CNDB.IP4_Network.query \\
    ...   ( Q.net_address.CONTAINS ("10.0.0.0/28")
    ...   , Q.ip_pool != None
    ...   )
    SQL: SELECT
           cndb_ip4_network."desc" AS cndb_ip4_network_desc,
           cndb_ip4_network.expiration_date AS cndb_ip4_network_expiration_date,
           cndb_ip4_network.net_address AS cndb_ip4_network_net_address,
           cndb_ip4_network.owner AS cndb_ip4_network_owner,
           cndb_ip4_network.parent AS cndb_ip4_network_parent,
           cndb_ip4_network.pid AS cndb_ip4_network_pid,
           cndb_ip4_network.pool AS cndb_ip4_network_pool,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN cndb_ip4_network ON mom_id_entity.pid = cndb_ip4_network.pid
           LEFT OUTER JOIN cndb_ip4_network_in_ip4_pool AS cndb_ip4_network_in_ip4_pool__1 ON cndb_ip4_network_in_ip4_pool__1."left" = cndb_ip4_network.pid
           LEFT OUTER JOIN cndb_ip4_pool AS cndb_ip4_pool__1 ON cndb_ip4_pool__1.pid = cndb_ip4_network_in_ip4_pool__1."right"
         WHERE (cndb_ip4_network.net_address >>= :net_address_1)
            AND cndb_ip4_network_in_ip4_pool__1."right" IS NOT NULL

"""

_test_alloc_sq = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB

    >>> CNDB.IP4_Network.query \\
    ...   ( Q.net_address.CONTAINS ("10.0.0.0/28")
    ...   , Q.ip_pool != None
    ...   )
    SQL: SELECT
           cndb_ip4_network."desc" AS cndb_ip4_network_desc,
           cndb_ip4_network.expiration_date AS cndb_ip4_network_expiration_date,
           cndb_ip4_network.net_address AS cndb_ip4_network_net_address,
           cndb_ip4_network.net_address__mask_len AS cndb_ip4_network_net_address__mask_len,
           cndb_ip4_network.net_address__numeric AS cndb_ip4_network_net_address__numeric,
           cndb_ip4_network.net_address__upper_bound AS cndb_ip4_network_net_address__upper_bound,
           cndb_ip4_network.owner AS cndb_ip4_network_owner,
           cndb_ip4_network.parent AS cndb_ip4_network_parent,
           cndb_ip4_network.pid AS cndb_ip4_network_pid,
           cndb_ip4_network.pool AS cndb_ip4_network_pool,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN cndb_ip4_network ON mom_id_entity.pid = cndb_ip4_network.pid
           LEFT OUTER JOIN cndb_ip4_network_in_ip4_pool AS cndb_ip4_network_in_ip4_pool__1 ON cndb_ip4_network_in_ip4_pool__1."left" = cndb_ip4_network.pid
           LEFT OUTER JOIN cndb_ip4_pool AS cndb_ip4_pool__1 ON cndb_ip4_pool__1.pid = cndb_ip4_network_in_ip4_pool__1."right"
         WHERE cndb_ip4_network.net_address__numeric <= :net_address__numeric_1
            AND cndb_ip4_network.net_address__upper_bound >= :net_address__upper_bound_1
            AND cndb_ip4_network.net_address__mask_len <= :net_address__mask_len_1
            AND cndb_ip4_network_in_ip4_pool__1."right" IS NOT NULL

"""

_test_partial = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP

    >>> ff = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> rs = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> fp = CNDB.IP4_Network ('10.0.0.0/8', owner = ff, raw = True)
    >>> a4 = fp.reserve ('10.0.0.1/32', owner = ff)
    >>> a5 = fp.reserve ('10.0.0.2/32', owner = ff)
    >>> dt = CNDB.Net_Device_Type.instance_or_new (name = 'G', raw = True)
    >>> n1 = CNDB.Node (name = "nogps", manager = rs, raw = True)
    >>> dv = CNDB.Net_Device (left = dt, node = n1, name = 'dev', raw = True)
    >>> wl = CNDB.Wireless_Interface (left = dv, name = 'wl', raw = True)
    >>> wd = CNDB.Wired_Interface (left = dv, name = 'wd', raw = True)
    >>> scope.commit ()

    >>> il2 = CNDB.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)
    >>> id2 = CNDB.Net_Interface_in_IP_Network  (wd, a5, mask_len = 24)

    >>> il2
    CNDB.Wireless_Interface_in_IP4_Network (((('g', '', ''), ('nogps', ), 'dev'), '', 'wl'), ("10.0.0.1", ))

    >>> id2
    CNDB.Wired_Interface_in_IP4_Network (((('g', '', ''), ('nogps', ), 'dev'), '', 'wd'), ("10.0.0.2", ))

"""

_test_AQ = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> AQ = CNDB.IP4_Network.E_Type.AQ
    >>> AQ
    <Attr.Type.Querier.E_Type for CNDB.IP4_Network>
    >>> for aq in AQ.Attrs :
    ...     print (aq)
    <net_address.AQ [Attr.Type.Querier Ckd]>
    <desc.AQ [Attr.Type.Querier String]>
    <owner.AQ [Attr.Type.Querier Id_Entity]>
    <pool.AQ [Attr.Type.Querier Id_Entity]>
    <creation.AQ [Attr.Type.Querier Rev_Ref]>
    <last_change.AQ [Attr.Type.Querier Rev_Ref]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <expiration_date.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <parent.AQ [Attr.Type.Querier Id_Entity]>
    <ip_pool.AQ [Attr.Type.Querier Rev_Ref]>
    <net_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <documents.AQ [Attr.Type.Querier Rev_Ref]>
    <wired_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <wireless_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <virtual_wireless_interface.AQ [Attr.Type.Querier Rev_Ref]>

    >>> for aq in AQ.Attrs_Transitive :
    ...     print (aq, aq.E_Type.type_name if aq.E_Type else "-"*5)
    <net_address.AQ [Attr.Type.Querier Ckd]> -----
    <desc.AQ [Attr.Type.Querier String]> -----
    <owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <pool.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <pool.net_address.AQ [Attr.Type.Querier Ckd]> -----
    <pool.desc.AQ [Attr.Type.Querier String]> -----
    <pool.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <pool.pool.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <pool.expiration_date.AQ [Attr.Type.Querier Ckd]> expiration_date__277__type_desc
    <pool.has_children.AQ [Attr.Type.Querier Boolean]> -----
    <pool.is_free.AQ [Attr.Type.Querier Boolean]> -----
    <pool.parent.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <creation.AQ [Attr.Type.Querier Rev_Ref]> MOM.MD_Change
    <creation.c_time.AQ [Attr.Type.Querier Ckd]> c_time__126__type_desc
    <creation.c_user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <creation.kind.AQ [Attr.Type.Querier String]> -----
    <creation.time.AQ [Attr.Type.Querier Ckd]> time__133__type_desc
    <creation.user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_change.AQ [Attr.Type.Querier Rev_Ref]> MOM.MD_Change
    <last_change.c_time.AQ [Attr.Type.Querier Ckd]> c_time__126__type_desc
    <last_change.c_user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_change.kind.AQ [Attr.Type.Querier String]> -----
    <last_change.time.AQ [Attr.Type.Querier Ckd]> time__133__type_desc
    <last_change.user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <pid.AQ [Attr.Type.Querier Ckd]> -----
    <type_name.AQ [Attr.Type.Querier String]> -----
    <expiration_date.AQ [Attr.Type.Querier Ckd]> expiration_date__277__type_desc
    <has_children.AQ [Attr.Type.Querier Boolean]> -----
    <is_free.AQ [Attr.Type.Querier Boolean]> -----
    <parent.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <parent.net_address.AQ [Attr.Type.Querier Ckd]> -----
    <parent.desc.AQ [Attr.Type.Querier String]> -----
    <parent.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <parent.pool.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <parent.expiration_date.AQ [Attr.Type.Querier Ckd]> expiration_date__277__type_desc
    <parent.has_children.AQ [Attr.Type.Querier Boolean]> -----
    <parent.is_free.AQ [Attr.Type.Querier Boolean]> -----
    <parent.parent.AQ [Attr.Type.Querier Id_Entity]> CNDB.IP4_Network
    <ip_pool.AQ [Attr.Type.Querier Rev_Ref]> CNDB.IP4_Pool
    <ip_pool.name.AQ [Attr.Type.Querier String]> -----
    <ip_pool.cool_down_period.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <ip_pool.node.name.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <ip_pool.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <ip_pool.node.address.street.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.city.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.country.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.region.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.desc.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <ip_pool.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <ip_pool.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <ip_pool.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <ip_pool.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <ip_pool.netmask_interval.AQ [Attr.Type.Querier Composite]> MOM.Int_Interval_C__IP_Netmask_Interval__IP4_Netmask_Interval
    <ip_pool.netmask_interval.lower.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.upper.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.center.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.length.AQ [Attr.Type.Querier Ckd]> -----
    <net_interface.AQ [Attr.Type.Querier Rev_Ref]> CNDB.Net_Interface
    <documents.AQ [Attr.Type.Querier Rev_Ref]> MOM.Document
    <documents.url.AQ [Attr.Type.Querier String]> -----
    <documents.type.AQ [Attr.Type.Querier String]> -----
    <documents.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.AQ [Attr.Type.Querier Rev_Ref]> CNDB.Wired_Interface
    <wired_interface.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <wired_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <wired_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wired_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wired_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <wired_interface.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wired_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <wired_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <wired_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wired_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wired_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.AQ [Attr.Type.Querier Rev_Ref]> CNDB.Wireless_Interface
    <wireless_interface.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <wireless_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <wireless_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wireless_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.mode.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.essid.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.bssid.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.standard.AQ [Attr.Type.Querier Id_Entity]> CNDB.Wireless_Standard
    <wireless_interface.standard.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.txpower.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wireless_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <wireless_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.AQ [Attr.Type.Querier Rev_Ref]> CNDB.Virtual_Wireless_Interface
    <virtual_wireless_interface.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <virtual_wireless_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <virtual_wireless_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.AQ [Attr.Type.Querier Id_Entity]> CNDB.Wireless_Interface
    <virtual_wireless_interface.hardware.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <virtual_wireless_interface.hardware.left.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <virtual_wireless_interface.hardware.left.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.hardware.left.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.hardware.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.mac_address.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.mode.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.essid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.bssid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.standard.AQ [Attr.Type.Querier Id_Entity]> CNDB.Wireless_Standard
    <virtual_wireless_interface.hardware.standard.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.txpower.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.hardware.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <virtual_wireless_interface.hardware.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <virtual_wireless_interface.hardware.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.hardware.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.hardware.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.mode.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.essid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.bssid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device
    <virtual_wireless_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> CNDB.Net_Device_Type
    <virtual_wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> CNDB.Node
    <virtual_wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.standard.AQ [Attr.Type.Querier Id_Entity]> CNDB.Wireless_Standard
    <virtual_wireless_interface.standard.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.txpower.AQ [Attr.Type.Querier Raw]> -----

    >>> for aq in AQ.Attrs_Transitive :
    ...     str (aq._ui_name_T)
    'Net address'
    'Description'
    'Owner'
    'Pool'
    'Pool/Net address'
    'Pool/Description'
    'Pool/Owner'
    'Pool/Pool'
    'Pool/Expiration date'
    'Pool/Has children'
    'Pool/Is free'
    'Pool/Parent'
    'Creation'
    'Creation/C time'
    'Creation/C user'
    'Creation/Kind'
    'Creation/Time'
    'Creation/User'
    'Last change'
    'Last change/C time'
    'Last change/C user'
    'Last change/Kind'
    'Last change/Time'
    'Last change/User'
    'Last cid'
    'Pid'
    'Type name'
    'Expiration date'
    'Has children'
    'Is free'
    'Parent'
    'Parent/Net address'
    'Parent/Description'
    'Parent/Owner'
    'Parent/Pool'
    'Parent/Expiration date'
    'Parent/Has children'
    'Parent/Is free'
    'Parent/Parent'
    'Ip pool'
    'Ip pool/Name'
    'Ip pool/Cool down period'
    'Ip pool/Node'
    'Ip pool/Node/Name'
    'Ip pool/Node/Manager'
    'Ip pool/Node/Address'
    'Ip pool/Node/Address/Street'
    'Ip pool/Node/Address/Zip code'
    'Ip pool/Node/Address/City'
    'Ip pool/Node/Address/Country'
    'Ip pool/Node/Address/Description'
    'Ip pool/Node/Address/Region'
    'Ip pool/Node/Description'
    'Ip pool/Node/Owner'
    'Ip pool/Node/Position'
    'Ip pool/Node/Position/Latitude'
    'Ip pool/Node/Position/Longitude'
    'Ip pool/Node/Position/Height'
    'Ip pool/Node/Show in map'
    'Ip pool/Netmask interval'
    'Ip pool/Netmask interval/Lower'
    'Ip pool/Netmask interval/Upper'
    'Ip pool/Netmask interval/Center'
    'Ip pool/Netmask interval/Length'
    'Net interface'
    'Documents'
    'Documents/Url'
    'Documents/Type'
    'Documents/Description'
    'Wired interface'
    'Wired interface/Net device'
    'Wired interface/Net device/Net device type'
    'Wired interface/Net device/Net device type/Name'
    'Wired interface/Net device/Net device type/Model no'
    'Wired interface/Net device/Net device type/Revision'
    'Wired interface/Net device/Net device type/Description'
    'Wired interface/Net device/Node'
    'Wired interface/Net device/Node/Name'
    'Wired interface/Net device/Node/Manager'
    'Wired interface/Net device/Node/Address'
    'Wired interface/Net device/Node/Address/Street'
    'Wired interface/Net device/Node/Address/Zip code'
    'Wired interface/Net device/Node/Address/City'
    'Wired interface/Net device/Node/Address/Country'
    'Wired interface/Net device/Node/Address/Description'
    'Wired interface/Net device/Node/Address/Region'
    'Wired interface/Net device/Node/Description'
    'Wired interface/Net device/Node/Owner'
    'Wired interface/Net device/Node/Position'
    'Wired interface/Net device/Node/Position/Latitude'
    'Wired interface/Net device/Node/Position/Longitude'
    'Wired interface/Net device/Node/Position/Height'
    'Wired interface/Net device/Node/Show in map'
    'Wired interface/Net device/Name'
    'Wired interface/Net device/Description'
    'Wired interface/Net device/My node'
    'Wired interface/Net device/My node/Name'
    'Wired interface/Net device/My node/Manager'
    'Wired interface/Net device/My node/Address'
    'Wired interface/Net device/My node/Address/Street'
    'Wired interface/Net device/My node/Address/Zip code'
    'Wired interface/Net device/My node/Address/City'
    'Wired interface/Net device/My node/Address/Country'
    'Wired interface/Net device/My node/Address/Description'
    'Wired interface/Net device/My node/Address/Region'
    'Wired interface/Net device/My node/Description'
    'Wired interface/Net device/My node/Owner'
    'Wired interface/Net device/My node/Position'
    'Wired interface/Net device/My node/Position/Latitude'
    'Wired interface/Net device/My node/Position/Longitude'
    'Wired interface/Net device/My node/Position/Height'
    'Wired interface/Net device/My node/Show in map'
    'Wired interface/Mac address'
    'Wired interface/Name'
    'Wired interface/Is active'
    'Wired interface/Description'
    'Wired interface/My node'
    'Wired interface/My node/Name'
    'Wired interface/My node/Manager'
    'Wired interface/My node/Address'
    'Wired interface/My node/Address/Street'
    'Wired interface/My node/Address/Zip code'
    'Wired interface/My node/Address/City'
    'Wired interface/My node/Address/Country'
    'Wired interface/My node/Address/Description'
    'Wired interface/My node/Address/Region'
    'Wired interface/My node/Description'
    'Wired interface/My node/Owner'
    'Wired interface/My node/Position'
    'Wired interface/My node/Position/Latitude'
    'Wired interface/My node/Position/Longitude'
    'Wired interface/My node/Position/Height'
    'Wired interface/My node/Show in map'
    'Wired interface/My net device'
    'Wired interface/My net device/Net device type'
    'Wired interface/My net device/Net device type/Name'
    'Wired interface/My net device/Net device type/Model no'
    'Wired interface/My net device/Net device type/Revision'
    'Wired interface/My net device/Net device type/Description'
    'Wired interface/My net device/Node'
    'Wired interface/My net device/Node/Name'
    'Wired interface/My net device/Node/Manager'
    'Wired interface/My net device/Node/Address'
    'Wired interface/My net device/Node/Address/Street'
    'Wired interface/My net device/Node/Address/Zip code'
    'Wired interface/My net device/Node/Address/City'
    'Wired interface/My net device/Node/Address/Country'
    'Wired interface/My net device/Node/Address/Description'
    'Wired interface/My net device/Node/Address/Region'
    'Wired interface/My net device/Node/Description'
    'Wired interface/My net device/Node/Owner'
    'Wired interface/My net device/Node/Position'
    'Wired interface/My net device/Node/Position/Latitude'
    'Wired interface/My net device/Node/Position/Longitude'
    'Wired interface/My net device/Node/Position/Height'
    'Wired interface/My net device/Node/Show in map'
    'Wired interface/My net device/Name'
    'Wired interface/My net device/Description'
    'Wired interface/My net device/My node'
    'Wired interface/My net device/My node/Name'
    'Wired interface/My net device/My node/Manager'
    'Wired interface/My net device/My node/Address'
    'Wired interface/My net device/My node/Address/Street'
    'Wired interface/My net device/My node/Address/Zip code'
    'Wired interface/My net device/My node/Address/City'
    'Wired interface/My net device/My node/Address/Country'
    'Wired interface/My net device/My node/Address/Description'
    'Wired interface/My net device/My node/Address/Region'
    'Wired interface/My net device/My node/Description'
    'Wired interface/My net device/My node/Owner'
    'Wired interface/My net device/My node/Position'
    'Wired interface/My net device/My node/Position/Latitude'
    'Wired interface/My net device/My node/Position/Longitude'
    'Wired interface/My net device/My node/Position/Height'
    'Wired interface/My net device/My node/Show in map'
    'Wireless interface'
    'Wireless interface/Net device'
    'Wireless interface/Net device/Net device type'
    'Wireless interface/Net device/Net device type/Name'
    'Wireless interface/Net device/Net device type/Model no'
    'Wireless interface/Net device/Net device type/Revision'
    'Wireless interface/Net device/Net device type/Description'
    'Wireless interface/Net device/Node'
    'Wireless interface/Net device/Node/Name'
    'Wireless interface/Net device/Node/Manager'
    'Wireless interface/Net device/Node/Address'
    'Wireless interface/Net device/Node/Address/Street'
    'Wireless interface/Net device/Node/Address/Zip code'
    'Wireless interface/Net device/Node/Address/City'
    'Wireless interface/Net device/Node/Address/Country'
    'Wireless interface/Net device/Node/Address/Description'
    'Wireless interface/Net device/Node/Address/Region'
    'Wireless interface/Net device/Node/Description'
    'Wireless interface/Net device/Node/Owner'
    'Wireless interface/Net device/Node/Position'
    'Wireless interface/Net device/Node/Position/Latitude'
    'Wireless interface/Net device/Node/Position/Longitude'
    'Wireless interface/Net device/Node/Position/Height'
    'Wireless interface/Net device/Node/Show in map'
    'Wireless interface/Net device/Name'
    'Wireless interface/Net device/Description'
    'Wireless interface/Net device/My node'
    'Wireless interface/Net device/My node/Name'
    'Wireless interface/Net device/My node/Manager'
    'Wireless interface/Net device/My node/Address'
    'Wireless interface/Net device/My node/Address/Street'
    'Wireless interface/Net device/My node/Address/Zip code'
    'Wireless interface/Net device/My node/Address/City'
    'Wireless interface/Net device/My node/Address/Country'
    'Wireless interface/Net device/My node/Address/Description'
    'Wireless interface/Net device/My node/Address/Region'
    'Wireless interface/Net device/My node/Description'
    'Wireless interface/Net device/My node/Owner'
    'Wireless interface/Net device/My node/Position'
    'Wireless interface/Net device/My node/Position/Latitude'
    'Wireless interface/Net device/My node/Position/Longitude'
    'Wireless interface/Net device/My node/Position/Height'
    'Wireless interface/Net device/My node/Show in map'
    'Wireless interface/Mac address'
    'Wireless interface/Name'
    'Wireless interface/Is active'
    'Wireless interface/Description'
    'Wireless interface/Mode'
    'Wireless interface/ESSID'
    'Wireless interface/BSSID'
    'Wireless interface/Wi-Fi Standard'
    'Wireless interface/Wi-Fi Standard/Name'
    'Wireless interface/Wi-Fi Standard/Bandwidth'
    'Wireless interface/TX power'
    'Wireless interface/My node'
    'Wireless interface/My node/Name'
    'Wireless interface/My node/Manager'
    'Wireless interface/My node/Address'
    'Wireless interface/My node/Address/Street'
    'Wireless interface/My node/Address/Zip code'
    'Wireless interface/My node/Address/City'
    'Wireless interface/My node/Address/Country'
    'Wireless interface/My node/Address/Description'
    'Wireless interface/My node/Address/Region'
    'Wireless interface/My node/Description'
    'Wireless interface/My node/Owner'
    'Wireless interface/My node/Position'
    'Wireless interface/My node/Position/Latitude'
    'Wireless interface/My node/Position/Longitude'
    'Wireless interface/My node/Position/Height'
    'Wireless interface/My node/Show in map'
    'Wireless interface/My net device'
    'Wireless interface/My net device/Net device type'
    'Wireless interface/My net device/Net device type/Name'
    'Wireless interface/My net device/Net device type/Model no'
    'Wireless interface/My net device/Net device type/Revision'
    'Wireless interface/My net device/Net device type/Description'
    'Wireless interface/My net device/Node'
    'Wireless interface/My net device/Node/Name'
    'Wireless interface/My net device/Node/Manager'
    'Wireless interface/My net device/Node/Address'
    'Wireless interface/My net device/Node/Address/Street'
    'Wireless interface/My net device/Node/Address/Zip code'
    'Wireless interface/My net device/Node/Address/City'
    'Wireless interface/My net device/Node/Address/Country'
    'Wireless interface/My net device/Node/Address/Description'
    'Wireless interface/My net device/Node/Address/Region'
    'Wireless interface/My net device/Node/Description'
    'Wireless interface/My net device/Node/Owner'
    'Wireless interface/My net device/Node/Position'
    'Wireless interface/My net device/Node/Position/Latitude'
    'Wireless interface/My net device/Node/Position/Longitude'
    'Wireless interface/My net device/Node/Position/Height'
    'Wireless interface/My net device/Node/Show in map'
    'Wireless interface/My net device/Name'
    'Wireless interface/My net device/Description'
    'Wireless interface/My net device/My node'
    'Wireless interface/My net device/My node/Name'
    'Wireless interface/My net device/My node/Manager'
    'Wireless interface/My net device/My node/Address'
    'Wireless interface/My net device/My node/Address/Street'
    'Wireless interface/My net device/My node/Address/Zip code'
    'Wireless interface/My net device/My node/Address/City'
    'Wireless interface/My net device/My node/Address/Country'
    'Wireless interface/My net device/My node/Address/Description'
    'Wireless interface/My net device/My node/Address/Region'
    'Wireless interface/My net device/My node/Description'
    'Wireless interface/My net device/My node/Owner'
    'Wireless interface/My net device/My node/Position'
    'Wireless interface/My net device/My node/Position/Latitude'
    'Wireless interface/My net device/My node/Position/Longitude'
    'Wireless interface/My net device/My node/Position/Height'
    'Wireless interface/My net device/My node/Show in map'
    'Virtual wireless interface'
    'Virtual wireless interface/Net device'
    'Virtual wireless interface/Net device/Net device type'
    'Virtual wireless interface/Net device/Net device type/Name'
    'Virtual wireless interface/Net device/Net device type/Model no'
    'Virtual wireless interface/Net device/Net device type/Revision'
    'Virtual wireless interface/Net device/Net device type/Description'
    'Virtual wireless interface/Net device/Node'
    'Virtual wireless interface/Net device/Node/Name'
    'Virtual wireless interface/Net device/Node/Manager'
    'Virtual wireless interface/Net device/Node/Address'
    'Virtual wireless interface/Net device/Node/Address/Street'
    'Virtual wireless interface/Net device/Node/Address/Zip code'
    'Virtual wireless interface/Net device/Node/Address/City'
    'Virtual wireless interface/Net device/Node/Address/Country'
    'Virtual wireless interface/Net device/Node/Address/Description'
    'Virtual wireless interface/Net device/Node/Address/Region'
    'Virtual wireless interface/Net device/Node/Description'
    'Virtual wireless interface/Net device/Node/Owner'
    'Virtual wireless interface/Net device/Node/Position'
    'Virtual wireless interface/Net device/Node/Position/Latitude'
    'Virtual wireless interface/Net device/Node/Position/Longitude'
    'Virtual wireless interface/Net device/Node/Position/Height'
    'Virtual wireless interface/Net device/Node/Show in map'
    'Virtual wireless interface/Net device/Name'
    'Virtual wireless interface/Net device/Description'
    'Virtual wireless interface/Net device/My node'
    'Virtual wireless interface/Net device/My node/Name'
    'Virtual wireless interface/Net device/My node/Manager'
    'Virtual wireless interface/Net device/My node/Address'
    'Virtual wireless interface/Net device/My node/Address/Street'
    'Virtual wireless interface/Net device/My node/Address/Zip code'
    'Virtual wireless interface/Net device/My node/Address/City'
    'Virtual wireless interface/Net device/My node/Address/Country'
    'Virtual wireless interface/Net device/My node/Address/Description'
    'Virtual wireless interface/Net device/My node/Address/Region'
    'Virtual wireless interface/Net device/My node/Description'
    'Virtual wireless interface/Net device/My node/Owner'
    'Virtual wireless interface/Net device/My node/Position'
    'Virtual wireless interface/Net device/My node/Position/Latitude'
    'Virtual wireless interface/Net device/My node/Position/Longitude'
    'Virtual wireless interface/Net device/My node/Position/Height'
    'Virtual wireless interface/Net device/My node/Show in map'
    'Virtual wireless interface/Hardware'
    'Virtual wireless interface/Hardware/Net device'
    'Virtual wireless interface/Hardware/Net device/Net device type'
    'Virtual wireless interface/Hardware/Net device/Net device type/Name'
    'Virtual wireless interface/Hardware/Net device/Net device type/Model no'
    'Virtual wireless interface/Hardware/Net device/Net device type/Revision'
    'Virtual wireless interface/Hardware/Net device/Net device type/Description'
    'Virtual wireless interface/Hardware/Net device/Node'
    'Virtual wireless interface/Hardware/Net device/Node/Name'
    'Virtual wireless interface/Hardware/Net device/Node/Manager'
    'Virtual wireless interface/Hardware/Net device/Node/Address'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Street'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Zip code'
    'Virtual wireless interface/Hardware/Net device/Node/Address/City'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Country'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Description'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Region'
    'Virtual wireless interface/Hardware/Net device/Node/Description'
    'Virtual wireless interface/Hardware/Net device/Node/Owner'
    'Virtual wireless interface/Hardware/Net device/Node/Position'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Latitude'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Longitude'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Height'
    'Virtual wireless interface/Hardware/Net device/Node/Show in map'
    'Virtual wireless interface/Hardware/Net device/Name'
    'Virtual wireless interface/Hardware/Net device/Description'
    'Virtual wireless interface/Hardware/Net device/My node'
    'Virtual wireless interface/Hardware/Net device/My node/Name'
    'Virtual wireless interface/Hardware/Net device/My node/Manager'
    'Virtual wireless interface/Hardware/Net device/My node/Address'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Street'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/Net device/My node/Address/City'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Country'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Description'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Region'
    'Virtual wireless interface/Hardware/Net device/My node/Description'
    'Virtual wireless interface/Hardware/Net device/My node/Owner'
    'Virtual wireless interface/Hardware/Net device/My node/Position'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Height'
    'Virtual wireless interface/Hardware/Net device/My node/Show in map'
    'Virtual wireless interface/Hardware/Mac address'
    'Virtual wireless interface/Hardware/Name'
    'Virtual wireless interface/Hardware/Is active'
    'Virtual wireless interface/Hardware/Description'
    'Virtual wireless interface/Hardware/Mode'
    'Virtual wireless interface/Hardware/ESSID'
    'Virtual wireless interface/Hardware/BSSID'
    'Virtual wireless interface/Hardware/Wi-Fi Standard'
    'Virtual wireless interface/Hardware/Wi-Fi Standard/Name'
    'Virtual wireless interface/Hardware/Wi-Fi Standard/Bandwidth'
    'Virtual wireless interface/Hardware/TX power'
    'Virtual wireless interface/Hardware/My node'
    'Virtual wireless interface/Hardware/My node/Name'
    'Virtual wireless interface/Hardware/My node/Manager'
    'Virtual wireless interface/Hardware/My node/Address'
    'Virtual wireless interface/Hardware/My node/Address/Street'
    'Virtual wireless interface/Hardware/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/My node/Address/City'
    'Virtual wireless interface/Hardware/My node/Address/Country'
    'Virtual wireless interface/Hardware/My node/Address/Description'
    'Virtual wireless interface/Hardware/My node/Address/Region'
    'Virtual wireless interface/Hardware/My node/Description'
    'Virtual wireless interface/Hardware/My node/Owner'
    'Virtual wireless interface/Hardware/My node/Position'
    'Virtual wireless interface/Hardware/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/My node/Position/Height'
    'Virtual wireless interface/Hardware/My node/Show in map'
    'Virtual wireless interface/Hardware/My net device'
    'Virtual wireless interface/Hardware/My net device/Net device type'
    'Virtual wireless interface/Hardware/My net device/Net device type/Name'
    'Virtual wireless interface/Hardware/My net device/Net device type/Model no'
    'Virtual wireless interface/Hardware/My net device/Net device type/Revision'
    'Virtual wireless interface/Hardware/My net device/Net device type/Description'
    'Virtual wireless interface/Hardware/My net device/Node'
    'Virtual wireless interface/Hardware/My net device/Node/Name'
    'Virtual wireless interface/Hardware/My net device/Node/Manager'
    'Virtual wireless interface/Hardware/My net device/Node/Address'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Street'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Zip code'
    'Virtual wireless interface/Hardware/My net device/Node/Address/City'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Country'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Description'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Region'
    'Virtual wireless interface/Hardware/My net device/Node/Description'
    'Virtual wireless interface/Hardware/My net device/Node/Owner'
    'Virtual wireless interface/Hardware/My net device/Node/Position'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Latitude'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Longitude'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Height'
    'Virtual wireless interface/Hardware/My net device/Node/Show in map'
    'Virtual wireless interface/Hardware/My net device/Name'
    'Virtual wireless interface/Hardware/My net device/Description'
    'Virtual wireless interface/Hardware/My net device/My node'
    'Virtual wireless interface/Hardware/My net device/My node/Name'
    'Virtual wireless interface/Hardware/My net device/My node/Manager'
    'Virtual wireless interface/Hardware/My net device/My node/Address'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Street'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/My net device/My node/Address/City'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Country'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Description'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Region'
    'Virtual wireless interface/Hardware/My net device/My node/Description'
    'Virtual wireless interface/Hardware/My net device/My node/Owner'
    'Virtual wireless interface/Hardware/My net device/My node/Position'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Height'
    'Virtual wireless interface/Hardware/My net device/My node/Show in map'
    'Virtual wireless interface/Mac address'
    'Virtual wireless interface/Name'
    'Virtual wireless interface/Is active'
    'Virtual wireless interface/Description'
    'Virtual wireless interface/Mode'
    'Virtual wireless interface/ESSID'
    'Virtual wireless interface/BSSID'
    'Virtual wireless interface/My node'
    'Virtual wireless interface/My node/Name'
    'Virtual wireless interface/My node/Manager'
    'Virtual wireless interface/My node/Address'
    'Virtual wireless interface/My node/Address/Street'
    'Virtual wireless interface/My node/Address/Zip code'
    'Virtual wireless interface/My node/Address/City'
    'Virtual wireless interface/My node/Address/Country'
    'Virtual wireless interface/My node/Address/Description'
    'Virtual wireless interface/My node/Address/Region'
    'Virtual wireless interface/My node/Description'
    'Virtual wireless interface/My node/Owner'
    'Virtual wireless interface/My node/Position'
    'Virtual wireless interface/My node/Position/Latitude'
    'Virtual wireless interface/My node/Position/Longitude'
    'Virtual wireless interface/My node/Position/Height'
    'Virtual wireless interface/My node/Show in map'
    'Virtual wireless interface/My net device'
    'Virtual wireless interface/My net device/Net device type'
    'Virtual wireless interface/My net device/Net device type/Name'
    'Virtual wireless interface/My net device/Net device type/Model no'
    'Virtual wireless interface/My net device/Net device type/Revision'
    'Virtual wireless interface/My net device/Net device type/Description'
    'Virtual wireless interface/My net device/Node'
    'Virtual wireless interface/My net device/Node/Name'
    'Virtual wireless interface/My net device/Node/Manager'
    'Virtual wireless interface/My net device/Node/Address'
    'Virtual wireless interface/My net device/Node/Address/Street'
    'Virtual wireless interface/My net device/Node/Address/Zip code'
    'Virtual wireless interface/My net device/Node/Address/City'
    'Virtual wireless interface/My net device/Node/Address/Country'
    'Virtual wireless interface/My net device/Node/Address/Description'
    'Virtual wireless interface/My net device/Node/Address/Region'
    'Virtual wireless interface/My net device/Node/Description'
    'Virtual wireless interface/My net device/Node/Owner'
    'Virtual wireless interface/My net device/Node/Position'
    'Virtual wireless interface/My net device/Node/Position/Latitude'
    'Virtual wireless interface/My net device/Node/Position/Longitude'
    'Virtual wireless interface/My net device/Node/Position/Height'
    'Virtual wireless interface/My net device/Node/Show in map'
    'Virtual wireless interface/My net device/Name'
    'Virtual wireless interface/My net device/Description'
    'Virtual wireless interface/My net device/My node'
    'Virtual wireless interface/My net device/My node/Name'
    'Virtual wireless interface/My net device/My node/Manager'
    'Virtual wireless interface/My net device/My node/Address'
    'Virtual wireless interface/My net device/My node/Address/Street'
    'Virtual wireless interface/My net device/My node/Address/Zip code'
    'Virtual wireless interface/My net device/My node/Address/City'
    'Virtual wireless interface/My net device/My node/Address/Country'
    'Virtual wireless interface/My net device/My node/Address/Description'
    'Virtual wireless interface/My net device/My node/Address/Region'
    'Virtual wireless interface/My net device/My node/Description'
    'Virtual wireless interface/My net device/My node/Owner'
    'Virtual wireless interface/My net device/My node/Position'
    'Virtual wireless interface/My net device/My node/Position/Latitude'
    'Virtual wireless interface/My net device/My node/Position/Longitude'
    'Virtual wireless interface/My net device/My node/Position/Height'
    'Virtual wireless interface/My net device/My node/Show in map'
    'Virtual wireless interface/Wi-Fi Standard'
    'Virtual wireless interface/Wi-Fi Standard/Name'
    'Virtual wireless interface/Wi-Fi Standard/Bandwidth'
    'Virtual wireless interface/TX power'

    >>> AQ.parent.parent.parent.owner
    <parent.parent.parent.owner.AQ [Attr.Type.Querier Id_Entity]>

    >>> for aq in AQ.Atoms :
    ...     print (aq)
    <net_address.AQ [Attr.Type.Querier Ckd]>
    <desc.AQ [Attr.Type.Querier String]>
    <pool.net_address.AQ [Attr.Type.Querier Ckd]>
    <pool.desc.AQ [Attr.Type.Querier String]>
    <pool.expiration_date.AQ [Attr.Type.Querier Ckd]>
    <pool.has_children.AQ [Attr.Type.Querier Boolean]>
    <pool.is_free.AQ [Attr.Type.Querier Boolean]>
    <creation.c_time.AQ [Attr.Type.Querier Ckd]>
    <creation.kind.AQ [Attr.Type.Querier String]>
    <creation.time.AQ [Attr.Type.Querier Ckd]>
    <last_change.c_time.AQ [Attr.Type.Querier Ckd]>
    <last_change.kind.AQ [Attr.Type.Querier String]>
    <last_change.time.AQ [Attr.Type.Querier Ckd]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <expiration_date.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <parent.net_address.AQ [Attr.Type.Querier Ckd]>
    <parent.desc.AQ [Attr.Type.Querier String]>
    <parent.expiration_date.AQ [Attr.Type.Querier Ckd]>
    <parent.has_children.AQ [Attr.Type.Querier Boolean]>
    <parent.is_free.AQ [Attr.Type.Querier Boolean]>
    <ip_pool.name.AQ [Attr.Type.Querier String]>
    <ip_pool.cool_down_period.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.node.name.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.street.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.zip.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.city.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.country.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.desc.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.region.AQ [Attr.Type.Querier String]>
    <ip_pool.node.desc.AQ [Attr.Type.Querier String]>
    <ip_pool.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <ip_pool.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <ip_pool.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <ip_pool.netmask_interval.lower.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.upper.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.center.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.length.AQ [Attr.Type.Querier Ckd]>
    <documents.url.AQ [Attr.Type.Querier String]>
    <documents.type.AQ [Attr.Type.Querier String]>
    <documents.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.mac_address.AQ [Attr.Type.Querier String]>
    <wired_interface.name.AQ [Attr.Type.Querier String]>
    <wired_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.mac_address.AQ [Attr.Type.Querier String]>
    <wireless_interface.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.mode.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.essid.AQ [Attr.Type.Querier String]>
    <wireless_interface.bssid.AQ [Attr.Type.Querier String]>
    <wireless_interface.standard.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.txpower.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.mac_address.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.is_active.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.mode.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.essid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.bssid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.standard.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.txpower.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.mac_address.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.mode.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.essid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.bssid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.standard.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.txpower.AQ [Attr.Type.Querier Raw]>

    >>> print (formatted (AQ.As_Json_Cargo))
    { 'filters' :
        [ { 'name' : 'net_address'
          , 'sig_key' : 0
          , 'ui_name' : 'Net address'
          }
        , { 'name' : 'desc'
          , 'sig_key' : 3
          , 'ui_name' : 'Description'
          }
        , { 'Class' : 'Entity'
          , 'children_np' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Adhoc_Group'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Adhoc_Group'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Association'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Association'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'registered_in'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Registered in'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Company'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Company'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'last_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Last name'
                      }
                    , { 'name' : 'first_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'First name'
                      }
                    , { 'name' : 'middle_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Middle name'
                      }
                    , { 'name' : 'title'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Academic title'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Person'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Person'
                }
              ]
          , 'default_child' : 'PAP.Person'
          , 'name' : 'owner'
          , 'sig_key' : 2
          , 'ui_name' : 'Owner'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'net_address'
                , 'sig_key' : 0
                , 'ui_name' : 'Net address'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Adhoc_Group'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Adhoc_Group'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Association'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Association'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'registered_in'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Registered in'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Company'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Company'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'default_child' : 'PAP.Person'
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'ui_name' : 'Owner'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'pool'
                , 'sig_key' : 2
                , 'ui_name' : 'Pool'
                }
              , { 'name' : 'expiration_date'
                , 'sig_key' : 0
                , 'ui_name' : 'Expiration date'
                }
              , { 'name' : 'has_children'
                , 'sig_key' : 1
                , 'ui_name' : 'Has children'
                }
              , { 'name' : 'is_free'
                , 'sig_key' : 1
                , 'ui_name' : 'Is free'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'parent'
                , 'sig_key' : 2
                , 'ui_name' : 'Parent'
                }
              ]
          , 'name' : 'pool'
          , 'sig_key' : 2
          , 'ui_name' : 'Pool'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'c_time'
                , 'sig_key' : 0
                , 'ui_name' : 'C time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'c_user'
                , 'sig_key' : 2
                , 'ui_name' : 'C user'
                }
              , { 'name' : 'kind'
                , 'sig_key' : 3
                , 'ui_name' : 'Kind'
                }
              , { 'name' : 'time'
                , 'sig_key' : 0
                , 'ui_name' : 'Time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'user'
                , 'sig_key' : 2
                , 'ui_name' : 'User'
                }
              ]
          , 'name' : 'creation'
          , 'sig_key' : 2
          , 'ui_name' : 'Creation'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'c_time'
                , 'sig_key' : 0
                , 'ui_name' : 'C time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'c_user'
                , 'sig_key' : 2
                , 'ui_name' : 'C user'
                }
              , { 'name' : 'kind'
                , 'sig_key' : 3
                , 'ui_name' : 'Kind'
                }
              , { 'name' : 'time'
                , 'sig_key' : 0
                , 'ui_name' : 'Time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'user'
                , 'sig_key' : 2
                , 'ui_name' : 'User'
                }
              ]
          , 'name' : 'last_change'
          , 'sig_key' : 2
          , 'ui_name' : 'Last change'
          }
        , { 'name' : 'last_cid'
          , 'sig_key' : 0
          , 'ui_name' : 'Last cid'
          }
        , { 'name' : 'pid'
          , 'sig_key' : 0
          , 'ui_name' : 'Pid'
          }
        , { 'name' : 'type_name'
          , 'sig_key' : 3
          , 'ui_name' : 'Type name'
          }
        , { 'name' : 'expiration_date'
          , 'sig_key' : 0
          , 'ui_name' : 'Expiration date'
          }
        , { 'name' : 'has_children'
          , 'sig_key' : 1
          , 'ui_name' : 'Has children'
          }
        , { 'name' : 'is_free'
          , 'sig_key' : 1
          , 'ui_name' : 'Is free'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'net_address'
                , 'sig_key' : 0
                , 'ui_name' : 'Net address'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Adhoc_Group'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Adhoc_Group'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Association'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Association'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'registered_in'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Registered in'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Company'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Company'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'default_child' : 'PAP.Person'
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'ui_name' : 'Owner'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'pool'
                , 'sig_key' : 2
                , 'ui_name' : 'Pool'
                }
              , { 'name' : 'expiration_date'
                , 'sig_key' : 0
                , 'ui_name' : 'Expiration date'
                }
              , { 'name' : 'has_children'
                , 'sig_key' : 1
                , 'ui_name' : 'Has children'
                }
              , { 'name' : 'is_free'
                , 'sig_key' : 1
                , 'ui_name' : 'Is free'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'parent'
                , 'sig_key' : 2
                , 'ui_name' : 'Parent'
                }
              ]
          , 'name' : 'parent'
          , 'sig_key' : 2
          , 'ui_name' : 'Parent'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'cool_down_period'
                , 'sig_key' : 0
                , 'ui_name' : 'Cool down period'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'node'
                , 'sig_key' : 2
                , 'ui_name' : 'Node'
                }
              , { 'attrs' :
                    [ { 'name' : 'lower'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Lower'
                      }
                    , { 'name' : 'upper'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Upper'
                      }
                    , { 'name' : 'center'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Center'
                      }
                    , { 'name' : 'length'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Length'
                      }
                    ]
                , 'name' : 'netmask_interval'
                , 'ui_name' : 'Netmask interval'
                }
              ]
          , 'name' : 'ip_pool'
          , 'sig_key' : 2
          , 'ui_name' : 'Ip pool'
          }
        , { 'Class' : 'Entity'
          , 'name' : 'net_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Net interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'url'
                , 'sig_key' : 3
                , 'ui_name' : 'Url'
                }
              , { 'name' : 'type'
                , 'sig_key' : 3
                , 'ui_name' : 'Type'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              ]
          , 'name' : 'documents'
          , 'sig_key' : 2
          , 'ui_name' : 'Documents'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              ]
          , 'name' : 'wired_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Wired interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'name' : 'mode'
                , 'sig_key' : 0
                , 'ui_name' : 'Mode'
                }
              , { 'name' : 'essid'
                , 'sig_key' : 3
                , 'ui_name' : 'ESSID'
                }
              , { 'name' : 'bssid'
                , 'sig_key' : 3
                , 'ui_name' : 'BSSID'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'bandwidth'
                      , 'sig_key' : 4
                      , 'ui_name' : 'Bandwidth'
                      }
                    ]
                , 'name' : 'standard'
                , 'sig_key' : 2
                , 'ui_name' : 'Wi-Fi Standard'
                }
              , { 'name' : 'txpower'
                , 'sig_key' : 4
                , 'ui_name' : 'TX power'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              ]
          , 'name' : 'wireless_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Wireless interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'model_no'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Model no'
                                  }
                                , { 'name' : 'revision'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Revision'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                ]
                            , 'name' : 'left'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Net device type'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Node'
                            }
                          , { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'my_node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'My node'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device'
                      }
                    , { 'name' : 'mac_address'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Mac address'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'is_active'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Is active'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'name' : 'mode'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Mode'
                      }
                    , { 'name' : 'essid'
                      , 'sig_key' : 3
                      , 'ui_name' : 'ESSID'
                      }
                    , { 'name' : 'bssid'
                      , 'sig_key' : 3
                      , 'ui_name' : 'BSSID'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'bandwidth'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Bandwidth'
                            }
                          ]
                      , 'name' : 'standard'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Wi-Fi Standard'
                      }
                    , { 'name' : 'txpower'
                      , 'sig_key' : 4
                      , 'ui_name' : 'TX power'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'model_no'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Model no'
                                  }
                                , { 'name' : 'revision'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Revision'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                ]
                            , 'name' : 'left'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Net device type'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Node'
                            }
                          , { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'manager'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Manager'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'my_node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'My node'
                            }
                          ]
                      , 'name' : 'my_net_device'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My net device'
                      }
                    ]
                , 'name' : 'hardware'
                , 'sig_key' : 2
                , 'ui_name' : 'Hardware'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'name' : 'mode'
                , 'sig_key' : 0
                , 'ui_name' : 'Mode'
                }
              , { 'name' : 'essid'
                , 'sig_key' : 3
                , 'ui_name' : 'ESSID'
                }
              , { 'name' : 'bssid'
                , 'sig_key' : 3
                , 'ui_name' : 'BSSID'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Manager'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Manager'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'bandwidth'
                      , 'sig_key' : 4
                      , 'ui_name' : 'Bandwidth'
                      }
                    ]
                , 'name' : 'standard'
                , 'sig_key' : 2
                , 'ui_name' : 'Wi-Fi Standard'
                }
              , { 'name' : 'txpower'
                , 'sig_key' : 4
                , 'ui_name' : 'TX power'
                }
              ]
          , 'name' : 'virtual_wireless_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Virtual wireless interface'
          }
        ]
    , 'name_sep' : '__'
    , 'op_map' :
        { 'CONTAINS' :
            { 'desc' : 'Select entities where the attribute contains the specified value'
            , 'sym' : 'contains'
            }
        , 'ENDSWITH' :
            { 'desc' : 'Select entities where the attribute value ends with the specified value'
            , 'sym' : 'ends-with'
            }
        , 'EQ' :
            { 'desc' : 'Select entities where the attribute is equal to the specified value'
            , 'sym' : '=='
            }
        , 'EQS' :
            { 'desc' : 'Select entities where the attribute is equal to the specified string value'
            , 'sym' : 'EQS'
            }
        , 'GE' :
            { 'desc' : 'Select entities where the attribute is greater than, or equal to, the specified value'
            , 'sym' : '>='
            }
        , 'GT' :
            { 'desc' : 'Select entities where the attribute is greater than the specified value'
            , 'sym' : '>'
            }
        , 'IN' :
            { 'desc' : 'Select entities where the attribute is a member of the specified list of values'
            , 'sym' : 'in'
            }
        , 'LE' :
            { 'desc' : 'Select entities where the attribute is less than, or equal to, the specified value'
            , 'sym' : '<='
            }
        , 'LT' :
            { 'desc' : 'Select entities where the attribute is less than the specified value'
            , 'sym' : '<'
            }
        , 'NE' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified value'
            , 'sym' : '!='
            }
        , 'NES' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified string value'
            , 'sym' : 'NES'
            }
        , 'STARTSWITH' :
            { 'desc' : 'Select entities where the attribute value starts with the specified value'
            , 'sym' : 'starts-with'
            }
        }
    , 'op_sep' : '___'
    , 'sig_map' :
        { 0 :
            ( 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            )
        , 1 : ('EQ', )
        , 2 :
            ( 'EQ'
            , 'IN'
            , 'NE'
            )
        , 3 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'STARTSWITH'
            )
        , 4 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'EQS'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'NES'
            , 'STARTSWITH'
            )
        }
    , 'ui_sep' : '/'
    }


    >>> QR  = GTW.RST.TOP.MOM.Query_Restriction
    >>> print (formatted (QR.Filter_Atoms (QR.Filter (CNDB.IP4_Network, "owner"))))
    ( Record
        ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
        , attr = Date `start`
        , attrs =
          [ Record
              ( attr = Int `day`
              , full_name = 'lifetime.start.day'
              , id = 'lifetime__start__day'
              , name = 'day'
              , sig_key = 0
              , ui_name = 'Lifetime/Start/Day'
              )
          , Record
              ( attr = Int `month`
              , full_name = 'lifetime.start.month'
              , id = 'lifetime__start__month'
              , name = 'month'
              , sig_key = 0
              , ui_name = 'Lifetime/Start/Month'
              )
          , Record
              ( attr = Int `year`
              , full_name = 'lifetime.start.year'
              , id = 'lifetime__start__year'
              , name = 'year'
              , sig_key = 0
              , ui_name = 'Lifetime/Start/Year'
              )
          ]
        , edit = None
        , full_name = 'lifetime.start'
        , id = 'lifetime__start___AC'
        , name = 'lifetime__start___AC'
        , op =
          Record
            ( desc = 'Select entities where the attribute is equal to the specified value'
            , label = 'auto-complete'
            )
        , sig_key = 0
        , ui_name = 'Lifetime/Start'
        , value = None
        )
    , Record
        ( AQ = <lifetime.finish.AQ [Attr.Type.Querier Date]>
        , attr = Date `finish`
        , attrs =
          [ Record
              ( attr = Int `day`
              , full_name = 'lifetime.finish.day'
              , id = 'lifetime__finish__day'
              , name = 'day'
              , sig_key = 0
              , ui_name = 'Lifetime/Finish/Day'
              )
          , Record
              ( attr = Int `month`
              , full_name = 'lifetime.finish.month'
              , id = 'lifetime__finish__month'
              , name = 'month'
              , sig_key = 0
              , ui_name = 'Lifetime/Finish/Month'
              )
          , Record
              ( attr = Int `year`
              , full_name = 'lifetime.finish.year'
              , id = 'lifetime__finish__year'
              , name = 'year'
              , sig_key = 0
              , ui_name = 'Lifetime/Finish/Year'
              )
          ]
        , edit = None
        , full_name = 'lifetime.finish'
        , id = 'lifetime__finish___AC'
        , name = 'lifetime__finish___AC'
        , op =
          Record
            ( desc = 'Select entities where the attribute is equal to the specified value'
            , label = 'auto-complete'
            )
        , sig_key = 0
        , ui_name = 'Lifetime/Finish'
        , value = None
        )
    )

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (CNDB.IP4_Network, "parent"))))
    ( Record
        ( AQ = <net_address.AQ [Attr.Type.Querier Ckd]>
        , attr = IP4-network `net_address`
        , edit = None
        , full_name = 'net_address'
        , id = 'net_address___AC'
        , name = 'net_address___AC'
        , op =
          Record
            ( desc = 'Select entities where the attribute is equal to the specified value'
            , label = 'auto-complete'
            )
        , sig_key = 0
        , ui_name = 'Net address'
        , value = None
        )
    ,
    )

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (CNDB.Net_Interface_in_IP4_Network, "right"))))
    ( Record
        ( AQ = <net_address.AQ [Attr.Type.Querier Ckd]>
        , attr = IP4-network `net_address`
        , edit = None
        , full_name = 'net_address'
        , id = 'net_address___AC'
        , name = 'net_address___AC'
        , op =
          Record
            ( desc = 'Select entities where the attribute is equal to the specified value'
            , label = 'auto-complete'
            )
        , sig_key = 0
        , ui_name = 'Net address'
        , value = None
        )
    ,
    )

    >>> for aq in CNDB.Node.E_Type.AQ.Attrs_Transitive :
    ...     print (aq._ui_name_T)
    Name
    Manager
    Address
    Address/Street
    Address/Zip code
    Address/City
    Address/Country
    Address/Description
    Address/Region
    Description
    Owner
    Position
    Position/Latitude
    Position/Longitude
    Position/Height
    Show in map
    Creation
    Creation/C time
    Creation/C user
    Creation/Kind
    Creation/Time
    Creation/User
    Last change
    Last change/C time
    Last change/C user
    Last change/Kind
    Last change/Time
    Last change/User
    Last cid
    Pid
    Type name
    Documents
    Documents/Url
    Documents/Type
    Documents/Description

    >>> for aq in CNDB.Net_Interface.E_Type.AQ.Attrs_Transitive :
    ...     print (aq._ui_name_T)
    Device
    Device/Net device type
    Device/Net device type/Name
    Device/Net device type/Model no
    Device/Net device type/Revision
    Device/Net device type/Description
    Device/Node
    Device/Node/Name
    Device/Node/Manager
    Device/Node/Address
    Device/Node/Address/Street
    Device/Node/Address/Zip code
    Device/Node/Address/City
    Device/Node/Address/Country
    Device/Node/Address/Description
    Device/Node/Address/Region
    Device/Node/Description
    Device/Node/Owner
    Device/Node/Position
    Device/Node/Position/Latitude
    Device/Node/Position/Longitude
    Device/Node/Position/Height
    Device/Node/Show in map
    Device/Name
    Device/Description
    Device/My node
    Device/My node/Name
    Device/My node/Manager
    Device/My node/Address
    Device/My node/Address/Street
    Device/My node/Address/Zip code
    Device/My node/Address/City
    Device/My node/Address/Country
    Device/My node/Address/Description
    Device/My node/Address/Region
    Device/My node/Description
    Device/My node/Owner
    Device/My node/Position
    Device/My node/Position/Latitude
    Device/My node/Position/Longitude
    Device/My node/Position/Height
    Device/My node/Show in map
    Mac address
    Name
    Is active
    Description
    Creation
    Creation/C time
    Creation/C user
    Creation/Kind
    Creation/Time
    Creation/User
    Last change
    Last change/C time
    Last change/C user
    Last change/Kind
    Last change/Time
    Last change/User
    Last cid
    Pid
    Type name
    My node
    My node/Name
    My node/Manager
    My node/Address
    My node/Address/Street
    My node/Address/Zip code
    My node/Address/City
    My node/Address/Country
    My node/Address/Description
    My node/Address/Region
    My node/Description
    My node/Owner
    My node/Position
    My node/Position/Latitude
    My node/Position/Longitude
    My node/Position/Height
    My node/Show in map
    My net device
    My net device/Net device type
    My net device/Net device type/Name
    My net device/Net device type/Model no
    My net device/Net device type/Revision
    My net device/Net device type/Description
    My net device/Node
    My net device/Node/Name
    My net device/Node/Manager
    My net device/Node/Address
    My net device/Node/Address/Street
    My net device/Node/Address/Zip code
    My net device/Node/Address/City
    My net device/Node/Address/Country
    My net device/Node/Address/Description
    My net device/Node/Address/Region
    My net device/Node/Description
    My net device/Node/Owner
    My net device/Node/Position
    My net device/Node/Position/Latitude
    My net device/Node/Position/Longitude
    My net device/Node/Position/Height
    My net device/Node/Show in map
    My net device/Name
    My net device/Description
    My net device/My node
    My net device/My node/Name
    My net device/My node/Manager
    My net device/My node/Address
    My net device/My node/Address/Street
    My net device/My node/Address/Zip code
    My net device/My node/Address/City
    My net device/My node/Address/Country
    My net device/My node/Address/Description
    My net device/My node/Address/Region
    My net device/My node/Description
    My net device/My node/Owner
    My net device/My node/Position
    My net device/My node/Position/Latitude
    My net device/My node/Position/Longitude
    My net device/My node/Position/Height
    My net device/My node/Show in map
    Credentials 1
    Credentials 1/My node
    Credentials 1/My node/Name
    Credentials 1/My node/Manager
    Credentials 1/My node/Address
    Credentials 1/My node/Address/Street
    Credentials 1/My node/Address/Zip code
    Credentials 1/My node/Address/City
    Credentials 1/My node/Address/Country
    Credentials 1/My node/Address/Description
    Credentials 1/My node/Address/Region
    Credentials 1/My node/Description
    Credentials 1/My node/Owner
    Credentials 1/My node/Position
    Credentials 1/My node/Position/Latitude
    Credentials 1/My node/Position/Longitude
    Credentials 1/My node/Position/Height
    Credentials 1/My node/Show in map
    Credentials 1/My net device
    Credentials 1/My net device/Net device type
    Credentials 1/My net device/Net device type/Name
    Credentials 1/My net device/Net device type/Model no
    Credentials 1/My net device/Net device type/Revision
    Credentials 1/My net device/Net device type/Description
    Credentials 1/My net device/Node
    Credentials 1/My net device/Node/Name
    Credentials 1/My net device/Node/Manager
    Credentials 1/My net device/Node/Address
    Credentials 1/My net device/Node/Address/Street
    Credentials 1/My net device/Node/Address/Zip code
    Credentials 1/My net device/Node/Address/City
    Credentials 1/My net device/Node/Address/Country
    Credentials 1/My net device/Node/Address/Description
    Credentials 1/My net device/Node/Address/Region
    Credentials 1/My net device/Node/Description
    Credentials 1/My net device/Node/Owner
    Credentials 1/My net device/Node/Position
    Credentials 1/My net device/Node/Position/Latitude
    Credentials 1/My net device/Node/Position/Longitude
    Credentials 1/My net device/Node/Position/Height
    Credentials 1/My net device/Node/Show in map
    Credentials 1/My net device/Name
    Credentials 1/My net device/Description
    Credentials 1/My net device/My node
    Ip4 networks
    Ip4 networks/Net address
    Ip4 networks/Description
    Ip4 networks/Owner
    Ip4 networks/Pool
    Ip4 networks/Pool/Net address
    Ip4 networks/Pool/Description
    Ip4 networks/Pool/Owner
    Ip4 networks/Pool/Pool
    Ip4 networks/Pool/Expiration date
    Ip4 networks/Pool/Has children
    Ip4 networks/Pool/Is free
    Ip4 networks/Pool/Parent
    Ip4 networks/Expiration date
    Ip4 networks/Has children
    Ip4 networks/Is free
    Ip4 networks/Parent
    Ip6 networks
    Ip6 networks/Net address
    Ip6 networks/Description
    Ip6 networks/Owner
    Ip6 networks/Pool
    Ip6 networks/Pool/Net address
    Ip6 networks/Pool/Description
    Ip6 networks/Pool/Owner
    Ip6 networks/Pool/Pool
    Ip6 networks/Pool/Expiration date
    Ip6 networks/Pool/Has children
    Ip6 networks/Pool/Is free
    Ip6 networks/Pool/Parent
    Ip6 networks/Expiration date
    Ip6 networks/Has children
    Ip6 networks/Is free
    Ip6 networks/Parent
    Documents
    Documents/Url
    Documents/Type
    Documents/Description

"""

_test_net_fixtures = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> net_fixtures (scope)
    >>> scope.commit ()

    >>> show_by_pid (scope.CNDB.Node)
    2   : Node                      nogps
    3   : Node                      node2
    38  : Node                      Node-net1
    39  : Node                      Node-net2
    40  : Node                      Node-net3
    41  : Node                      Node-net4

    >>> show_by_pid (scope.CNDB.Net_Device)
    28  : Net_Device                Generic, node2, dev
    44  : Net_Device                Generic, Node-net1, n1d1
    45  : Net_Device                Generic, Node-net1, n1d2
    46  : Net_Device                Generic, Node-net2, n2d1
    47  : Net_Device                Generic, Node-net2, n2d2
    48  : Net_Device                Generic, Node-net2, n2d3
    49  : Net_Device                Generic, Node-net3, n3d1
    50  : Net_Device                Generic, Node-net4, n4d1
    51  : Net_Device                Generic, Node-net4, n4d2
    52  : Net_Device                Generic, Node-net4, n4d3
    53  : Net_Device                Generic, Node-net4, n4d4
    54  : Net_Device                Generic, Node-net4, n4d5

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.my_node.name == "nogps"))
    2   : Node                      nogps

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.my_node.name == "node2"))
    3   : Node                      node2
    28  : Net_Device                Generic, node2, dev
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl
    31  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.1
    32  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.2
    33  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.3
    34  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.4

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net1"))
    38  : Node                      Node-net1
    44  : Net_Device                Generic, Node-net1, n1d1
    45  : Net_Device                Generic, Node-net1, n1d2

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net2"))
    39  : Node                      Node-net2
    46  : Net_Device                Generic, Node-net2, n2d1
    47  : Net_Device                Generic, Node-net2, n2d2
    48  : Net_Device                Generic, Node-net2, n2d3

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net3"))
    40  : Node                      Node-net3
    49  : Net_Device                Generic, Node-net3, n3d1

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.my_node.name == "node-net4"))
    41  : Node                      Node-net4
    50  : Net_Device                Generic, Node-net4, n4d1
    51  : Net_Device                Generic, Node-net4, n4d2
    52  : Net_Device                Generic, Node-net4, n4d3
    53  : Net_Device                Generic, Node-net4, n4d4
    54  : Net_Device                Generic, Node-net4, n4d5

"""

_test_order_4 = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> I4N = CNDB.IP4_Network

    >>> PAP = scope.PAP
    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)

    >>> _   = I4N ("10.0.0.16/28")
    >>> _   = I4N ("10.0.0.16/29")
    >>> _   = I4N ("10.0.0.24/29")
    >>> _   = I4N ("10.0.0.24/30")
    >>> _   = I4N ("10.0.0.16/30")
    >>> _   = I4N ("10.0.0.30/32")
    >>> _   = I4N ("10.0.0.32/28")
    >>> _   = I4N ("10.0.0.33/32")
    >>> _   = I4N ("10.0.0.40/29")
    >>> _   = I4N ("10.0.0.40/30")
    >>> _   = I4N ("10.0.0.40/31")
    >>> _   = I4N ("10.0.0.40/32")
    >>> _   = I4N ("10.0.0.128/28")
    >>> _   = I4N ("10.0.0.212/28")
    >>> adr = I4N.net_address.P_Type ("10.0.0.0/32")
    >>> _   = I4N (adr, owner = ff, raw = True)

    >>> scope.commit ()

    >>> ETM = scope.CNDB.IP4_Network
    >>> show_networks (scope, ETM)
    10.0.0.0           Funkfeuer                : electric = F, children = F
    10.0.0.16/28                                : electric = F, children = F
    10.0.0.16/29                                : electric = F, children = F
    10.0.0.16/30                                : electric = F, children = F
    10.0.0.24/29                                : electric = F, children = F
    10.0.0.24/30                                : electric = F, children = F
    10.0.0.30                                   : electric = F, children = F
    10.0.0.32/28                                : electric = F, children = F
    10.0.0.33                                   : electric = F, children = F
    10.0.0.40/29                                : electric = F, children = F
    10.0.0.40/30                                : electric = F, children = F
    10.0.0.40/31                                : electric = F, children = F
    10.0.0.40                                   : electric = F, children = F
    10.0.0.128/28                               : electric = F, children = F
    10.0.0.208/28                               : electric = F, children = F

    >>> adr1 = I4N.net_address.P_Type ("192.168.0.112/27")
    >>> adr1
    192.168.0.96/27
    >>> bool (adr1)
    True
    >>> I4N (adr1, owner = ff)
    CNDB.IP4_Network ("192.168.0.96/27")

    >>> adr2 = I4N.net_address.P_Type ("192.168.1.96/27")
    >>> adr2
    192.168.1.96/27
    >>> bool (adr2)
    True
    >>> I4N (adr2, owner = ff, raw = True)
    CNDB.IP4_Network ("192.168.1.96/27")

"""

_test_order_6 = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> I6N = CNDB.IP6_Network

    >>> PAP = scope.PAP
    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)

    >>> _   = I6N ("2001:0db8::10/124")
    >>> _   = I6N ("2001:0db8::10/125")
    >>> _   = I6N ("2001:0db8::18/125")
    >>> _   = I6N ("2001:0db8::18/126")
    >>> _   = I6N ("2001:0db8::10/126")
    >>> _   = I6N ("2001:0db8::1E/128")
    >>> _   = I6N ("2001:0db8::20/124")
    >>> _   = I6N ("2001:0db8::21/128")
    >>> _   = I6N ("2001:0db8::28/125")
    >>> _   = I6N ("2001:0db8::28/126")
    >>> _   = I6N ("2001:0db8::28/127")
    >>> _   = I6N ("2001:0db8::28/128")
    >>> _   = I6N ("2001:0db8::80/124")
    >>> _   = I6N ("2001:0db8::D4/124")
    >>> adr = I6N.net_address.P_Type ("2001:0db8::0/128")
    >>> _   = I6N (adr, owner = ff, raw = True)

    >>> scope.commit ()

    >>> ETM = scope.CNDB.IP6_Network
    >>> show_networks (scope, ETM)
    2001:db8::         Funkfeuer                : electric = F, children = F
    2001:db8::10/124                            : electric = F, children = F
    2001:db8::10/125                            : electric = F, children = F
    2001:db8::10/126                            : electric = F, children = F
    2001:db8::18/125                            : electric = F, children = F
    2001:db8::18/126                            : electric = F, children = F
    2001:db8::1e                                : electric = F, children = F
    2001:db8::20/124                            : electric = F, children = F
    2001:db8::21                                : electric = F, children = F
    2001:db8::28/125                            : electric = F, children = F
    2001:db8::28/126                            : electric = F, children = F
    2001:db8::28/127                            : electric = F, children = F
    2001:db8::28                                : electric = F, children = F
    2001:db8::80/124                            : electric = F, children = F
    2001:db8::d0/124                            : electric = F, children = F

    >>> adr1 = I6N.net_address.P_Type ("2a02:58::/29")
    >>> adr1
    2a02:58::/29
    >>> bool (adr1)
    True
    >>> I6N  (adr1, owner = ff, raw = True)
    CNDB.IP6_Network ("2a02:58::/29")

    >>> adr2 = I6N.net_address.P_Type ("2a02:60::/29")
    >>> adr2
    2a02:60::/29
    >>> bool (adr2)
    True
    >>> I6N  (adr2, owner = ff)
    CNDB.IP6_Network ("2a02:60::/29")

"""

_test_std_fixtures = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> std_fixtures (scope)
    >>> scope.commit ()

    >>> show_by_pid (scope.CNDB.Node)
    2   : Node                      nogps
    3   : Node                      node2

    >>> show_by_pid (scope.CNDB.Net_Device)
    28  : Net_Device                Generic, node2, dev

    >>> show_by_pid (scope.CNDB.Net_Interface)
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl

    >>> show_by_pid (scope.CNDB.Net_Interface_in_IP4_Network)
    31  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.1
    32  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.2
    33  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.3
    34  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.4

    >>> show_by_pid (scope.CNDB.IP4_Network)
    4   : IP4_Network               192.168.23.0/24
    5   : IP4_Network               192.168.23.0/25
    6   : IP4_Network               192.168.23.128/25
    7   : IP4_Network               192.168.23.0/26
    8   : IP4_Network               192.168.23.64/26
    9   : IP4_Network               192.168.23.0/27
    10  : IP4_Network               192.168.23.32/27
    11  : IP4_Network               192.168.23.0/28
    12  : IP4_Network               192.168.23.16/28
    13  : IP4_Network               192.168.23.0/29
    14  : IP4_Network               192.168.23.8/29
    15  : IP4_Network               192.168.23.0/30
    16  : IP4_Network               192.168.23.4/30
    17  : IP4_Network               192.168.23.0/31
    18  : IP4_Network               192.168.23.2/31
    19  : IP4_Network               192.168.23.0
    20  : IP4_Network               192.168.23.1
    21  : IP4_Network               192.168.23.2
    22  : IP4_Network               192.168.23.3
    23  : IP4_Network               192.168.23.4/31
    24  : IP4_Network               192.168.23.6/31
    25  : IP4_Network               192.168.23.4
    26  : IP4_Network               192.168.23.5

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.my_node.name == "nogps"))
    2   : Node                      nogps

    >>> show_query_by_pid (scope.CNDB.Belongs_to_Node.query (Q.my_node.name == "node2"))
    3   : Node                      node2
    28  : Net_Device                Generic, node2, dev
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl
    31  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.1
    32  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.2
    33  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.3
    34  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.4

"""

_test_debug = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> I4N = CNDB.IP4_Network
    >>> Adr = I4N.net_address.P_Type

    >>> _   = I4N ("10.0.0.16/28")
    >>> _   = I4N ("10.0.0.16/29")
    >>> _   = I4N ("10.0.0.24/29")
    >>> _   = I4N ("10.0.0.24/30")
    >>> _   = I4N ("10.0.0.16/30")
    >>> _   = I4N ("10.0.0.30/32")
    >>> _   = I4N ("10.0.0.32/28")
    >>> _   = I4N ("10.0.0.33/32")
    >>> _   = I4N ("10.0.0.40/29")
    >>> _   = I4N ("10.0.0.40/30")
    >>> _   = I4N ("10.0.0.40/31")
    >>> _   = I4N ("10.0.0.40/32")
    >>> _   = I4N ("10.0.0.128/28")
    >>> _   = I4N ("10.0.0.212/28")

    >>> mgr = PAP.Person (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> node1 = CNDB.Node (name = "nogps", manager = mgr, raw = True)
    >>> net = CNDB.IP4_Network ('192.168.23.0/24', raw = True)
    >>> a1  = net.reserve ('192.168.23.1/32')
    >>> a2  = net.reserve (Adr ('192.168.23.2/32'))
    >>> a3  = net.reserve ('192.168.23.3/32')
    >>> a4  = net.reserve (Adr ('192.168.23.4/32'))
    >>> devtype = CNDB.Net_Device_Type.instance_or_new (name = 'Generic', raw = True)
    >>> dev = CNDB.Net_Device (left = devtype, node = node1, name = 'dev', raw = True)
    >>> wr  = CNDB.Wired_Interface (left = dev, name = 'wr', raw = True)
    >>> wl  = CNDB.Wireless_Interface (left = dev, name = 'wl', raw = True)

    >>> ir1 = CNDB.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    >>> il1 = CNDB.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    >>> ir2 = CNDB.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    >>> il2 = CNDB.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)

    >>> il1.right.ETM.query ( (Q.net_address.CONTAINS (il1.right.net_address)) & (Q.electric == False)).attr ("net_address.mask_len").all ()


"""

def show_by_pid (ETM) :
    show_query_by_pid (ETM.query ())
# end def show_by_pid

def show_networks (scope, ETM, * qargs, ** qkw) :
    sk = TFL.Sorted_By ("electric", "-has_children", "net_address")
    pool = qkw.pop ("pool", None)
    if pool is not None :
        qargs += (Q.net_address.IN (pool.net_address), )
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw).distinct () :
        now = datetime.now ()
        exp = ""
        if nw.expiration_date is not None :
            exp = "free" if nw.expiration_date < now else "expiring"
        ood = nw.FO.owner or exp
        print \
            ( "%-18s %-25s: electric = %1.1s, children = %1.1s"
            % (nw.FO.net_address, ood, nw.electric, nw.has_children)
            )
# end def show_networks

def tree_view (net, indent = 0) :
    el = ' E' if net.electric else ''
    print ("%s%s%s" % (' ' * indent, net.net_address, el))
    for n in sorted (net.subnets, key = lambda x : x.net_address) :
        tree_view (n, indent + 1)
# end def tree_view

def show_network_count (scope, ETM) :
    print ("%s count: %s" % (ETM.type_name, ETM.count))
# end def show_network_count

def show_query_by_pid (q) :
    for x in q.order_by (Q.pid) :
        print ("%-3s : %-25s %s" % (x.pid, x.type_base_name, x.ui_display))
# end def show_query_by_pid

__test__ = Scaffold.create_test_dict \
  ( dict
      ( test_alloc         = _test_alloc
      , test_partial       = _test_partial
      , test_AQ            = _test_AQ
      , test_net_fixtures  = _test_net_fixtures
      , test_order_4       = _test_order_4
      , test_order_6       = _test_order_6
      , test_std_fixtures  = _test_std_fixtures
      )
  )

__test__.update \
    ( Scaffold.create_test_dict
        ( dict
            ( test_allow_x = _test_alloc_pg
            )
        , ignore = ("HPS", "MYS", "SQL", "sq")
        )
    )

__test__.update \
    ( Scaffold.create_test_dict
        ( dict
            ( test_allow_x = _test_alloc_sq
            )
        , ignore = ("HPS", "MYS", "POS", "pg")
        )
    )

X__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_debug     = _test_debug
        )
    )

### __END__ CNDB.OMP.__test__.IP_Network
