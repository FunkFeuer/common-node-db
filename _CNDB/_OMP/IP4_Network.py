# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.IP4_Network
#
# Purpose
#    Model IP4 Network of CNDB
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    22-May-2012 (RS) Add `net_mask`
#    13-Aug-2012 (RS) Remove `net_mask` (`IP4_Network` now has `mask_len`)
#    27-Feb-2013 (CT) Add `pool`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#     2-Apr-2014 (CT) Fix bases of `net_address`
#     2-Apr-2014 (CT) Add `pool.rev_ref_attr_name`
#     3-Apr-2014 (CT) Change `pool` to `parent`
#    20-Jun-2014 (RS) Re-add `pool`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

from   _GTW._OMP._NET           import NET
from   _CNDB._OMP.Attr_Type           import *

import _CNDB._OMP.IP_Network

import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = CNDB.OMP.IP_Network

class IP4_Network (_Ancestor_Essence) :
    """IPv4 Network of CNDB"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (NET.A_IP4_Network, _Ancestor.net_address) :
            """IPv4 Network address."""

        # end class net_address

        ### Non-primary attributes

        class parent (_Ancestor.parent) :
            """Parent of the `%(type_name)s`."""

            P_Type             = "CNDB.IP4_Network"
            rev_ref_attr_name  = "subnets"

        # end class parent

        class pool (_Ancestor.pool) :
            """Pool to which this `%(type_name)s` belongs."""

            P_Type             = "CNDB.IP4_Network"

        # end class pool

    # end class _Attributes

# end class IP4_Network

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP4_Network
