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
#    CNDB.OMP.__test__.Persons
#
# Purpose
#    Test Person and associations
#
# Revision Dates
#    19-Sep-2012 (RS) Creation
#    11-Oct-2012 (RS) Fix missing `raw` parameter
#    11-Oct-2012 (RS) `Nickname` test
#    14-Jun-2014 (RS) `PAP.Adhoc_Group`, `PAP.Person_in_Group`
#    ««revision-date»»···
#--

from   _CNDB._OMP.__test__.model      import *
from   datetime                 import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP
    >>> p1  = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> p2  = PAP.Person \\
    ...     (first_name = 'Hans', last_name = 'Schlatterbeck', raw = True)
    >>> pmp = CNDB.Person_mentors_Person (p1, p2)
    >>> nic = PAP.Nickname ('runtux', raw = True)
    >>> phn = PAP.Person_has_Nickname (p1, nic)
    >>> c1  = PAP.Company ("Open Source Consulting")
    >>> pg1 = PAP.Person_in_Group (p1, c1)

    >>> g   = PAP.Adhoc_Group ("New Adhoc Group")
    >>> pg2 = PAP.Person_in_Group (p1, g)


"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ CNDB.OMP.__test__.Nodes
