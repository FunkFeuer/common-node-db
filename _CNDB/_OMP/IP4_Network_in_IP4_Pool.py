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
#    CNDB.OMP.IP4_Network_in_IP4_Pool
#
# Purpose
#    Model IPv4 networks in an IPv4 pool
#
# Revision Dates
#     3-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

import _CNDB._OMP.IP4_Network
import _CNDB._OMP.IP4_Pool
import _CNDB._OMP.IP_Network_in_IP_Pool

_Ancestor_Essence = CNDB.OMP.IP_Network_in_IP_Pool

class IP4_Network_in_IP4_Pool (_Ancestor_Essence) :
    """IPv4 networks in an IPv4 pool."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP network."""

            role_type          = CNDB.OMP.IP4_Network
            link_ref_attr_name = "ip_pool"

        # end class left

        class right (_Ancestor.right) :
            """IP pool."""

            role_type          = CNDB.OMP.IP4_Pool
            auto_rev_ref       = "ip_pool"
            link_ref_attr_name = "ip_network"

        # end class right

    # end class _Attributes

# end class IP4_Network_in_IP4_Pool

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP4_Network_in_IP4_Pool
