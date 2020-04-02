# -*- coding: utf-8 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck All rights reserved
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
#    CNDB.OMP.IP_Pool_permits_Group
#
# Purpose
#    Model permission for IP_Network reservation from an IP_Pool
#
# Revision Dates
#     3-Jul-2014 (RS) Creation
#     4-Sep-2014 (RS) `_Mixin` `CNDB.OMP.Entity` (tnx CT)
#    16-Sep-2014 (CT) Add `left.rev_ref_attr_name`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP         import PAP

from   _CNDB._OMP.Attr_Type         import *

import _CNDB._OMP.IP_Network
import _GTW._OMP._PAP.Id_Entity_permits_Group

_Mixin            = CNDB.OMP.Entity
_Ancestor_Essence = PAP.Id_Entity_permits_Group

class IP_Pool_permits_Group (_Mixin, _Ancestor_Essence) :
    """Permission to reserve IP_Network from IP_Pool"""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP Pool."""

            role_type          = CNDB.OMP.IP_Pool
            rev_ref_attr_name  = "group"

        # end class left

        ### Non-primary attributes

        class user_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool per user."""

            kind = Attr.Optional

        # end class user_quota

        class node_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool per node."""

            kind = Attr.Optional

        # end class user_quota

        class iface_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool for a single
               network interface.
            """

            kind = Attr.Optional

        # end class iface_quota

    # end class _Attributes

# end class IP_Pool_permits_Group

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP_Pool_permits_Group
