# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.__test__.Regulatory
#
# Purpose
#    Test Regulatory data structures from fixtures
#    Also test dB conversion and queries
#
# Revision Dates
#    17-Dec-2012 (RS) Creation
#     6-Mar-2013 (CT) Fix tests for `Q.RAW.frequency`
#     7-Mar-2013 (CT) Add tests for `Q.frequency` and `...AQ.frequency`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CNDB._OMP.__test__.model      import *
from   _CNDB._OMP.fixtures            import create as fixtures

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> fixtures (scope)

    >>> CNDB = scope.CNDB
    >>> WLC = CNDB.Wireless_Channel

    >>> prepr (CNDB.Regulatory_Permission.E_Type.attr_prop ("eirp").attr._default_unit)
    'dBm'
    >>> CNDB.Regulatory_Permission.query (Q.RAW.band.lower > '28 MHz').count ()
    3
    >>> CNDB.Regulatory_Permission.query (Q.RAW.band.lower < '28 MHz').count ()
    1
    >>> CNDB.Regulatory_Permission.query (Q.eirp <= 25).count ()
    3
    >>> CNDB.Regulatory_Permission.query (Q.eirp >= 26.5).count ()
    1
    >>> CNDB.Regulatory_Permission.query (Q.eirp > 27.5).count ()
    0

    #>>> CNDB.Regulatory_Permission.query (Q.eirp <= '110 mW').count ()
    #3
    #>>> CNDB.Regulatory_Permission.query (Q.eirp <= '21 dBm').count ()
    #3
    #>>> CNDB.Regulatory_Permission.query (Q.eirp <= '21 dBmW').count ()
    #3
    #>>> CNDB.Regulatory_Permission.query (Q.eirp <= '21 xyzzy').count ()
    #3

    #>>> CNDB.Regulatory_Permission.query (Q.RAW.eirp <= '110 mW').count ()
    #3
    #>>> CNDB.Regulatory_Permission.query (Q.RAW.eirp > '0.11 W').count ()
    #1
    #>>> CNDB.Regulatory_Permission.query (Q.RAW.eirp > '110 mW').count ()
    #1

    >>> WLC.query ().count ()
    86

    >>> WLC.query (Q.frequency == 5.7e9).count ()
    1
    >>> WLC.query (Q.frequency  > 5.7e9).count ()
    21
    >>> WLC.query (Q.frequency  < 5.7e9).count ()
    64


    `...AQ` converts raw values to cooked (`Q` cannot do that):
    >>> WLC.query (WLC.AQ.frequency.EQ ("5.7 GHz")).count ()
    1
    >>> WLC.query (WLC.AQ.frequency.GT ("5.7 GHz")).count ()
    21
    >>> WLC.query (WLC.AQ.frequency.LT ("5.7 GHz")).count ()
    64

    `...AQ...EQS` compares raw values, needs exact match,
    "5.7 GHz" doesn't --> no match:
    >>> WLC.query (WLC.AQ.frequency.EQS ("5.7 GHz")).count ()
    0
    >>> WLC.query (WLC.AQ.frequency.EQS ("5700 MHz")).count ()
    1

    >>> WLC.query (Q.RAW.frequency == "5700 MHz").count ()
    1
    >>> WLC.query (Q.RAW.frequency  > "5700 MHz").count ()
    21
    >>> WLC.query (Q.RAW.frequency  < "5700 MHz").count ()
    64

    `Q.RAW` must match raw value exactly, "5.7 GHz" doesn't --> no match:
    >>> WLC.query (Q.RAW.frequency == "5.7 GHz").count ()
    0
    >>> WLC.query (Q.RAW.frequency == "5700 MHz").count ()
    1

    >>> dom   = CNDB.Regulatory_Domain.instance (countrycode = "AT", raw = True)
    >>> band1 = dict (lower = "1 THz", upper = "2 THz")
    >>> rp1   = CNDB.Regulatory_Permission \\
    ...    (dom, band1, bandwidth = "40MHz", eirp = "100mW", raw = True)
    >>> round (rp1.eirp, 2)
    20.0
    >>> prepr (rp1.raw_attr ('eirp'))
    '100mW'
    >>> band2 = dict (lower = "2 THz", upper = "3 THz")
    >>> rp2    = CNDB.Regulatory_Permission \\
    ...    (dom, band2, bandwidth = "40MHz", eirp = "1W", raw = True)
    >>> round (rp2.eirp, 2)
    30.0
    >>> prepr (rp2.raw_attr ('eirp'))
    '1W'
    >>> band3 = dict (lower = "3 THz", upper = "4 THz")
    >>> rp3    = CNDB.Regulatory_Permission \\
    ...    (dom, band3, bandwidth = "40MHz", eirp = "10dBmW", raw = True)
    >>> round (rp3.eirp, 2)
    10.0
    >>> prepr (rp3.raw_attr ('eirp'))
    '10dBmW'
    >>> band4 = dict (lower = "4 THz", upper = "5 THz")
    >>> rp4    = CNDB.Regulatory_Permission \\
    ...    (dom, band4, bandwidth = "40MHz", eirp = "10dBW", raw = True)
    >>> round (rp4.eirp, 2)
    40.0
    >>> prepr (rp4.raw_attr ('eirp'))
    '10dBW'

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ CNDB.OMP.__test__.Regulatory
