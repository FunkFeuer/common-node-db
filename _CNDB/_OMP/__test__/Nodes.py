# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.__test__.Nodes
#
# Purpose
#    Test Node and associations
#
# Revision Dates
#    19-Sep-2012 (RS) Creation
#    24-Sep-2012 (RS) More tests, up to `Net_Interface_in_IP4_Network`
#    11-Oct-2012 (RS) Fix missing `raw` parameter
#    12-Oct-2012 (RS) Add tests for `Node` in role `Subject`
#    16-Oct-2012 (CT) Add tracebacks triggered by `CNDB.Node.refuse_links`
#    17-Dec-2012 (RS) Add tests for attributes of `belongs_to_node`
#     5-Mar-2013 (CT) Adapt to changes in `Net_Interface_in_IP4_Network`
#     7-Mar-2013 (RS) Add test for duplicate network allocation
#    16-Apr-2013 (CT) Add test `auto_children`,
#                     remove `Node_has_Phone`, `Node_has_Email`
#    17-Apr-2013 (CT) Add tests `owner` and `refuse_e_types`
#    18-Apr-2013 (CT) Add test for `eligible_e_types`,
#                     `selectable_e_types_unique_epk`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    30-Sep-2013 (CT) Adapt to uplift of `belongs_to_node`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    13-Jun-2014 (RS) Fixes for new `PAP` objects, `Node` no longer derived
#                     from `Subject`, addition of `Node.desc`, `ui_name`
#                     for `desc`
#    24-Feb-2017 (CT) Import `MOM.Inspect`, not `MOM.inspect`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CNDB._OMP.__test__.model      import *
from   _MOM.Inspect                   import children_trans_iter

from   datetime                 import datetime
from   rsclib.IP_Address        import IP4_Address as R_IP4_Address
from   rsclib.IP_Address        import IP6_Address as R_IP6_Address

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> Adr = str ### XXX CNDB.IP4_Network.net_address.P_Type

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)

    >>> comp = PAP.Company (name = "Open Source Consulting", raw = True)
    >>> node1 = CNDB.Node \\
    ...     (name = "nogps", manager = mgr, position = None, raw = True)
    >>> gps1 = dict (lat = "48 d 17 m 9.64 s", lon = "15 d 52 m 27.84 s")
    >>> node2 = CNDB.Node \\
    ...     (name = "node2", manager = mgr, position = gps1, raw = True)

    >>> adr = PAP.Address \\
    ...     ( street  = 'Example 23'
    ...     , zip     = '1010'
    ...     , city    = 'Wien'
    ...     , country = 'Austria'
    ...     )
    >>> node1.address = adr
    >>> node1.address
    PAP.Address ('example 23', '1010', 'wien', 'austria')

    >>> gps2 = dict (lat = "48.367088", lon = "16.187672")
    >>> node3 = CNDB.Node \\
    ...    (name = "node3", manager = mgr, owner = comp, position = gps2)
    >>> fmt = '%%Y-%%m-%%d %%H:%%M:%%S'
    >>> t1 = datetime.strptime ("2009-05-05 17:17:17", fmt)
    >>> t2 = datetime.strptime ("2010-05-05 23:23:23", fmt)
    >>> scope.ems.convert_creation_change (node3.pid, c_time = t1, time = t2)
    >>> node3.creation_date
    datetime.datetime(2009, 5, 5, 17, 17, 17)
    >>> node3.last_changed
    datetime.datetime(2010, 5, 5, 23, 23, 23)

    >>> net = CNDB.IP4_Network ('192.168.23.0/24', owner = mgr, raw = True)
    >>> a1  = net.reserve (Adr ('192.168.23.1/32'))
    >>> a2  = net.reserve (Adr ('192.168.23.2/32'))
    >>> a3  = net.reserve (Adr ('192.168.23.3/32'))
    >>> a4  = net.reserve (Adr ('192.168.23.4/32'))
    >>> ax  = net.reserve ('192.168.23.42/32')
    >>> ax
    CNDB.IP4_Network ("192.168.23.42")

    >>> devtype = CNDB.Net_Device_Type.instance_or_new \\
    ...     (name = 'Generic', raw = True)
    >>> dev = CNDB.Net_Device \\
    ...     (left = devtype, node = node3, name = 'dev', raw = True)
    >>> wr  = CNDB.Wired_Interface (left = dev, name = 'wr', raw = True)
    >>> wl  = CNDB.Wireless_Interface (left = dev, name = 'wl', raw = True)
    >>> ir1 = CNDB.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    >>> il1 = CNDB.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    >>> ir2 = CNDB.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    >>> il2 = CNDB.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)

    >>> with expect_except (MOM.Error.Invariants) :
    ...     irx = CNDB.Net_Interface_in_IP4_Network (wr, ax, mask_len = 22) # doctest:+ELLIPSIS
    Invariants: Condition `valid_mask_len` : The `mask_len` must match the one of `right` or of any
    network containing `right`. (mask_len in possible_mask_lens)
        mask_len = 22
        possible_mask_lens = [24, 25, 26, 27, 28, 29, 30, 31, 32] << sorted ( right.ETM.query ( (Q.net_address.CONTAINS (right.net_address))).attr ("net_address.mask_len"))
        right = 192.168.23.42
        right.net_address = ...

    >>> net2 = CNDB.IP4_Network (net_address = '10.0.0.0/8', owner = mgr, raw = True)
    >>> a2_1 = net2.reserve (Adr ('10.139.187.0/27'))
    >>> a2_2 = net2.reserve (Adr ('10.139.187.2'))
    >>> with expect_except (CNDB.OMP.Error.Address_Already_Used) :
    ...     a2_f = net2.reserve (Adr ('10.139.187.0/27'))
    Address_Already_Used: Address 10.139.187.0/27 already in use by 'Schlatterbeck Ralf'

    >>> at1 = CNDB.Antenna_Type \\
    ...     ( name         = "Yagi1"
    ...     , desc         = "A Yagi"
    ...     , gain         = 17.5
    ...     , polarization = "vertical"
    ...     , raw          = True
    ...     )
    >>> args = dict (left = at1, azimuth = "180", elevation_angle = 0, raw = True)
    >>> a = CNDB.Antenna (name = "1", ** args)
    >>> wia = CNDB.Wireless_Interface_uses_Antenna (wl, a)

    >>> CNDB.Antenna.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Belongs_to_Node.query (Q.my_node == node3).count ()
    10

    >>> CNDB.Net_Device.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Net_Interface.query (Q.my_node == node3).count ()
    2

    >>> CNDB.Node.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Wired_Interface.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Wireless_Interface.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Wireless_Interface_uses_Antenna.query (Q.my_node == node3).count ()
    1

    >>> CNDB.Net_Device.query (Q.my_node.manager == mgr).count ()
    1

    >>> CNDB.Net_Device.query (Q.my_node != node3).count ()
    0

"""

_test_auto_children = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     print ("%%-30s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), sorted (T.children_np_transitive)))
    PAP.Subject_has_Property       ['PAP.Association_has_Address', 'PAP.Association_has_Email', 'PAP.Association_has_IM_Handle', 'PAP.Association_has_Nickname', 'PAP.Association_has_Phone', 'PAP.Association_has_Url', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_IM_Handle', 'PAP.Company_has_Nickname', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_IM_Handle', 'PAP.Person_has_Nickname', 'PAP.Person_has_Phone', 'PAP.Person_has_Url']
      PAP.Subject_has_IM_Handle    ['PAP.Association_has_IM_Handle', 'PAP.Company_has_IM_Handle', 'PAP.Person_has_IM_Handle']
        PAP.Association_has_IM_Handle ['PAP.Association_has_IM_Handle']
        PAP.Person_has_IM_Handle   ['PAP.Person_has_IM_Handle']
        PAP.Company_has_IM_Handle  ['PAP.Company_has_IM_Handle']
      PAP.Subject_has_Nickname     ['PAP.Association_has_Nickname', 'PAP.Company_has_Nickname', 'PAP.Person_has_Nickname']
        PAP.Association_has_Nickname ['PAP.Association_has_Nickname']
        PAP.Person_has_Nickname    ['PAP.Person_has_Nickname']
        PAP.Company_has_Nickname   ['PAP.Company_has_Nickname']
      PAP.Subject_has_Address      ['PAP.Association_has_Address', 'PAP.Company_has_Address', 'PAP.Person_has_Address']
        PAP.Association_has_Address ['PAP.Association_has_Address']
        PAP.Person_has_Address     ['PAP.Person_has_Address']
        PAP.Company_has_Address    ['PAP.Company_has_Address']
      PAP.Subject_has_Email        ['PAP.Association_has_Email', 'PAP.Company_has_Email', 'PAP.Person_has_Email']
        PAP.Association_has_Email  ['PAP.Association_has_Email']
        PAP.Person_has_Email       ['PAP.Person_has_Email']
        PAP.Company_has_Email      ['PAP.Company_has_Email']
      PAP.Subject_has_Phone        ['PAP.Association_has_Phone', 'PAP.Company_has_Phone', 'PAP.Person_has_Phone']
        PAP.Association_has_Phone  ['PAP.Association_has_Phone']
        PAP.Person_has_Phone       ['PAP.Person_has_Phone']
        PAP.Company_has_Phone      ['PAP.Company_has_Phone']
      PAP.Subject_has_Url          ['PAP.Association_has_Url', 'PAP.Company_has_Url', 'PAP.Person_has_Url']
        PAP.Association_has_Url    ['PAP.Association_has_Url']
        PAP.Person_has_Url         ['PAP.Person_has_Url']
        PAP.Company_has_Url        ['PAP.Company_has_Url']

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     rr = T.relevant_root.type_name if T.relevant_root else sorted (T.relevant_roots)
    ...     print ("%%-30s %%-5s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), T.is_partial, rr))
    PAP.Subject_has_Property       True  PAP.Subject_has_Property
      PAP.Subject_has_IM_Handle    True  PAP.Subject_has_Property
        PAP.Association_has_IM_Handle False PAP.Subject_has_Property
        PAP.Person_has_IM_Handle   False PAP.Subject_has_Property
        PAP.Company_has_IM_Handle  False PAP.Subject_has_Property
      PAP.Subject_has_Nickname     True  PAP.Subject_has_Property
        PAP.Association_has_Nickname False PAP.Subject_has_Property
        PAP.Person_has_Nickname    False PAP.Subject_has_Property
        PAP.Company_has_Nickname   False PAP.Subject_has_Property
      PAP.Subject_has_Address      True  PAP.Subject_has_Property
        PAP.Association_has_Address False PAP.Subject_has_Property
        PAP.Person_has_Address     False PAP.Subject_has_Property
        PAP.Company_has_Address    False PAP.Subject_has_Property
      PAP.Subject_has_Email        True  PAP.Subject_has_Property
        PAP.Association_has_Email  False PAP.Subject_has_Property
        PAP.Person_has_Email       False PAP.Subject_has_Property
        PAP.Company_has_Email      False PAP.Subject_has_Property
      PAP.Subject_has_Phone        True  PAP.Subject_has_Property
        PAP.Association_has_Phone  False PAP.Subject_has_Property
        PAP.Person_has_Phone       False PAP.Subject_has_Property
        PAP.Company_has_Phone      False PAP.Subject_has_Property
      PAP.Subject_has_Url          True  PAP.Subject_has_Property
        PAP.Association_has_Url    False PAP.Subject_has_Property
        PAP.Person_has_Url         False PAP.Subject_has_Property
        PAP.Company_has_Url        False PAP.Subject_has_Property

"""

_test_owner = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> Adr = CNDB.IP4_Network.net_address.P_Type

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)

    >>> node1 = CNDB.Node (name = "nogps", manager = mgr, position = None, raw = True)
    >>> node1.owner
    PAP.Person ('schlatterbeck', 'ralf', '', '')

    >>> with expect_except (MOM.Error.Wrong_Type) :
    ...     node4 = CNDB.Node (name = "node4", manager = mgr, owner = node1)
    Wrong_Type: Node 'nogps' not eligible for attribute owner,
        must be instance of Subject

"""

_test_refuse_e_types = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP

    >>> for ET in scope.app_type._T_Extension :
    ...     for a in ET.id_entity_attr :
    ...         if getattr (a, "refuse_e_types", None) :
    ...             print (ET.type_name, a.name, sorted (a.refuse_e_types))
    PAP.Subject_has_Property left [u'PAP.Adhoc_Group']
    PAP.Subject_has_IM_Handle left [u'PAP.Adhoc_Group']
    PAP.Subject_has_Nickname left [u'PAP.Adhoc_Group']
    PAP.Subject_has_Address left [u'PAP.Adhoc_Group']
    PAP.Subject_has_Email left [u'PAP.Adhoc_Group']
    PAP.Subject_has_Phone left [u'PAP.Adhoc_Group']
    PAP.Subject_has_Url left [u'PAP.Adhoc_Group']
    PAP.Association_has_Url left [u'PAP.Adhoc_Group']
    PAP.Person_has_Url left [u'PAP.Adhoc_Group']
    PAP.Company_has_Url left [u'PAP.Adhoc_Group']
    PAP.Association_has_Phone left [u'PAP.Adhoc_Group']
    PAP.Person_has_Phone left [u'PAP.Adhoc_Group']
    PAP.Company_has_Phone left [u'PAP.Adhoc_Group']
    PAP.Association_has_Email left [u'PAP.Adhoc_Group']
    PAP.Person_has_Email left [u'PAP.Adhoc_Group']
    PAP.Company_has_Email left [u'PAP.Adhoc_Group']
    PAP.Association_has_Address left [u'PAP.Adhoc_Group']
    PAP.Person_has_Address left [u'PAP.Adhoc_Group']
    PAP.Company_has_Address left [u'PAP.Adhoc_Group']
    PAP.Association_has_Nickname left [u'PAP.Adhoc_Group']
    PAP.Person_has_Nickname left [u'PAP.Adhoc_Group']
    PAP.Company_has_Nickname left [u'PAP.Adhoc_Group']
    PAP.Association_has_IM_Handle left [u'PAP.Adhoc_Group']
    PAP.Person_has_IM_Handle left [u'PAP.Adhoc_Group']
    PAP.Company_has_IM_Handle left [u'PAP.Adhoc_Group']

    >>> for ET in scope.app_type._T_Extension :
    ...     for a in ET.id_entity_attr :
    ...         if getattr (a, "refuse_e_types", None) :
    ...             print (ET.type_name, a.name, sorted (a.refuse_e_types_transitive))
    PAP.Subject_has_Property left ['PAP.Adhoc_Group']
    PAP.Subject_has_IM_Handle left ['PAP.Adhoc_Group']
    PAP.Subject_has_Nickname left ['PAP.Adhoc_Group']
    PAP.Subject_has_Address left ['PAP.Adhoc_Group']
    PAP.Subject_has_Email left ['PAP.Adhoc_Group']
    PAP.Subject_has_Phone left ['PAP.Adhoc_Group']
    PAP.Subject_has_Url left ['PAP.Adhoc_Group']
    PAP.Association_has_Url left ['PAP.Adhoc_Group']
    PAP.Person_has_Url left ['PAP.Adhoc_Group']
    PAP.Company_has_Url left ['PAP.Adhoc_Group']
    PAP.Association_has_Phone left ['PAP.Adhoc_Group']
    PAP.Person_has_Phone left ['PAP.Adhoc_Group']
    PAP.Company_has_Phone left ['PAP.Adhoc_Group']
    PAP.Association_has_Email left ['PAP.Adhoc_Group']
    PAP.Person_has_Email left ['PAP.Adhoc_Group']
    PAP.Company_has_Email left ['PAP.Adhoc_Group']
    PAP.Association_has_Address left ['PAP.Adhoc_Group']
    PAP.Person_has_Address left ['PAP.Adhoc_Group']
    PAP.Company_has_Address left ['PAP.Adhoc_Group']
    PAP.Association_has_Nickname left ['PAP.Adhoc_Group']
    PAP.Person_has_Nickname left ['PAP.Adhoc_Group']
    PAP.Company_has_Nickname left ['PAP.Adhoc_Group']
    PAP.Association_has_IM_Handle left ['PAP.Adhoc_Group']
    PAP.Person_has_IM_Handle left ['PAP.Adhoc_Group']
    PAP.Company_has_IM_Handle left ['PAP.Adhoc_Group']

    >>> sorted (CNDB.Node.manager.eligible_e_types)
    ['PAP.Adhoc_Group', 'PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (CNDB.Node.owner.eligible_e_types)
    ['PAP.Adhoc_Group', 'PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (CNDB.Node.owner.selectable_e_types)
    ['PAP.Adhoc_Group', 'PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (PAP.Subject_has_Property.left.eligible_e_types)
    ['PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (PAP.Subject_has_Phone.left.eligible_e_types)
    ['PAP.Association', 'PAP.Company', 'PAP.Person']

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main            = _test_code
      , auto_children   = _test_auto_children
      , owner           = _test_owner
      , refuse_e_types  = _test_refuse_e_types
      )
  )

### __END__ CNDB.OMP.__test__.Nodes
