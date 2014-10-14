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
#    CNDB.OMP.IP6_Pool_permits_Group
#
# Purpose
#    Model permission for IP6_Network reservation from an IP6_Pool
#
# Revision Dates
#     3-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP         import PAP

from   _CNDB._OMP.Attr_Type         import *

import _CNDB._OMP.IP_Pool_permits_Group

_Ancestor_Essence = CNDB.OMP.IP_Pool_permits_Group

class IP6_Pool_permits_Group (_Ancestor_Essence) :
    """Permission to reserve IP6_Network from IP6_Pool"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP Pool."""

            role_type          = CNDB.OMP.IP6_Pool

        # end class left

        ### Non-primary attributes

        class user_quota (A_IP6_Quota, _Ancestor.user_quota)   : pass

        class node_quota (A_IP6_Quota, _Ancestor.node_quota)   : pass

        class iface_quota (A_IP6_Quota, _Ancestor.iface_quota) : pass

    # end class _Attributes

# end class IP6_Pool_permits_Group

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP6_Pool_permits_Group
