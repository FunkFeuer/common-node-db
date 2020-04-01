# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP__init__
#
# Purpose
#    Package defining the common node database model for Community Networks.
#
# Revision Dates
#    07-Jul-2014 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                 import MOM
from   _CNDB                import CNDB
import _MOM.Derived_PNS

_desc_ = """
Object model defining the common node database model for Community Networks.
"""

OMP = MOM.Derived_PNS (parent = MOM, pns_alias = "CNDB")
CNDB._Export ("OMP")

### __END__ CNDB.OMP__init__
