# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Dr. Ralf Schlatterbeck All rights reserved
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
#    CNDB.OMP.IP6_Network
#
# Purpose
#    Model IP6 Network of CNDB
#
# Revision Dates
#    22-May-2012 (RS) Creation
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

from   _CNDB._OMP.Attr_Type           import *
from   _GTW._OMP._NET           import NET

import _CNDB._OMP.IP_Network

import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = CNDB.OMP.IP_Network

class IP6_Network (_Ancestor_Essence) :
    """IPv6 Network of CNDB"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (NET.A_IP6_Network, _Ancestor.net_address) :
            """IPv6 Network address."""

        # end class net_address

        ### Non-primary attributes

        class parent (_Ancestor.parent) :
            """Parent of the `%(ui_type_name)s`."""

            P_Type             = "CNDB.IP6_Network"
            rev_ref_attr_name  = "subnets"

        # end class parent

        class pool (_Ancestor.pool) :
            """Pool to which this `%(ui_type_name)s` belongs."""

            P_Type             = "CNDB.IP6_Network"

        # end class pool

    # end class _Attributes

# end class IP6_Network

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP6_Network
