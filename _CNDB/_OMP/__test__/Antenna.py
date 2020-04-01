# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.__test__.Antenna
#
# Purpose
#    Test Antenna and associations
#
# Revision Dates
#     5-Dec-2012 (RS) Creation
#     7-Dec-2012 (RS) Test predicate `band_exists` of `Antenna_Type`
#    17-Dec-2012 (RS) Add tests for attributes of `belongs_to_node`
#    26-Feb-2013 (CT) Disable tests `belongs_to_node`
#    14-Aug-2013 (CT) Reenable tests for `belongs_to_node`
#    27-Jan-2014 (CT) Add tests for `polarization` vs. `raw_query_attrs`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    ««revision-date»»···
#--

from   _CNDB._OMP.__test__.model      import *
from   datetime                       import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> at1 = CNDB.Antenna_Type \\
    ...     ( name         = "Yagi1"
    ...     , desc         = "A Yagi"
    ...     , gain         = 17.5
    ...     , polarization = "vertical"
    ...     , raw          = True
    ...     )
    >>> b1 = CNDB.Antenna_Band (at1, band = ("2.4 GHz", "3 GHz"), raw = True)
    >>> at2 = CNDB.Antenna_Type \\
    ...     ( name         = "Yagi2"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> b2 = CNDB.Antenna_Band (at2, band = ("5 GHz", "6 GHz"), raw = True)
    >>> scope.commit ()

    >>> at3 = CNDB.Antenna_Type \\
    ...     ( name         = "Yagi3"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> with expect_except (MOM.Error.Invariants) :
    ...     scope.commit ()
    Invariants: Condition `band_exists` : There must be at least one frequency band for the antenna. (number_of_bands >= 1)
        bands = ()
        number_of_bands = 0 << len (bands)

    >>> args = dict (left = at1, azimuth = "180", elevation_angle = 0, raw = True)
    >>> a = CNDB.Antenna (name = "1", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 1)
    >>> a = CNDB.Antenna (name = "2", gain = 11, ** args)
    >>> (a.gain, a.polarization)
    (11.0, 1)
    >>> a = CNDB.Antenna (name = "3", polarization = "horizontal", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 0)
    >>> args = dict (left = at2, azimuth = "90", elevation_angle = 0, raw = True)
    >>> b = CNDB.Antenna (name = "4", ** args)
    >>> (b.gain, b.polarization)
    (11.5, 0)
    >>> b = CNDB.Antenna (name = "5", polarization = 'left circular', ** args)
    >>> (b.gain, b.polarization)
    (11.5, 2)
    >>> b = CNDB.Antenna (name = "6", gain = 22, ** args)
    >>> (b.gain, b.polarization)
    (22.0, 0)

    >>> akw = dict (polarization = "horizontal")
    >>> CNDB.Antenna.query_s (* CNDB.Antenna.raw_query_attrs (akw, akw)).all ()
    [CNDB.Antenna (('yagi1', '', ''), '3'), CNDB.Antenna (('yagi2', '', ''), '4'), CNDB.Antenna (('yagi2', '', ''), '6')]

    >>> akw = dict (polarization = "vertical")
    >>> CNDB.Antenna.query_s (* CNDB.Antenna.raw_query_attrs (akw, akw)).all ()
    [CNDB.Antenna (('yagi1', '', ''), '1'), CNDB.Antenna (('yagi1', '', ''), '2')]

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> owner = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> node = CNDB.Node \\
    ...     (name = "nogps", manager = mgr, position = None, raw = True)
    >>> nod2 = CNDB.Node \\
    ...     (name = "node2", manager = mgr, owner = owner, raw = True)
    >>> devtype = CNDB.Net_Device_Type.instance_or_new \\
    ...     (name = 'Generic', raw = True)
    >>> dev = CNDB.Net_Device \\
    ...     (left = devtype, node = node, name = 'dev', raw = True)
    >>> dev2 = CNDB.Net_Device \\
    ...     (left = devtype, node = nod2, name = 'dev2', raw = True)
    >>> wl  = CNDB.Wireless_Interface (left = dev, name = 'wl', raw = True)
    >>> wia = CNDB.Wireless_Interface_uses_Antenna (wl, b)

    >>> b.__class__.my_node
    Entity `my_node`

    >>> a.my_node is None
    True

    >>> b.my_node
    CNDB.Node ('nogps')

    >>> b.my_node.manager is b.my_node.owner
    True

    >>> CNDB.Antenna.query (Q.interface == wl).count ()
    1
    >>> CNDB.Antenna.query (Q.my_node.manager == mgr).count ()
    1
    >>> CNDB.Wireless_Interface.query (Q.my_node.manager == mgr).count ()
    1
    >>> CNDB.Wireless_Interface.query (Q.my_node.owner == mgr).count ()
    1

    >>> for x in scope.CNDB.Net_Interface.query (Q.my_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Wireless_Interface ((('generic', '', ''), ('nogps', ), 'dev'), '', 'wl')

    >>> for x in scope.CNDB.Wireless_Interface_uses_Antenna.query (Q.my_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Wireless_Interface_uses_Antenna (((('generic', '', ''), ('nogps', ), 'dev'), '', 'wl'), (('yagi2', '', ''), '6'))

    >>> for x in scope.CNDB.Net_Device.query (Q.my_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Net_Device (('generic', '', ''), ('nogps', ), 'dev')
    CNDB.Net_Device (('generic', '', ''), ('node2', ), 'dev2')

    >>> for x in scope.CNDB.Net_Device.query (Q.my_node.owner == owner, sort_key = Q.pid) :
    ...     x
    CNDB.Net_Device (('generic', '', ''), ('node2', ), 'dev2')

    >>> for x in scope.CNDB.Antenna.query (Q.my_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Antenna (('yagi2', '', ''), '6')

    >>> for x in scope.CNDB.Node.query (Q.manager == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Node ('nogps')
    CNDB.Node ('node2')

    >>> for x in scope.CNDB.Node.query (Q.owner == mgr, sort_key = Q.pid) :
    ...     x
    CNDB.Node ('nogps')

    >>> for x in scope.CNDB.Node.query (Q.owner == owner, sort_key = Q.pid) :
    ...     x
    CNDB.Node ('node2')

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main_test  = _test_code
      )
  )

### __END__ CNDB.OMP.__test__.Antenna
