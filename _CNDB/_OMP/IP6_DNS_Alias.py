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
#    CNDB.OMP.IP_DNS_Alias
#
# Purpose
#    Model a DNS alias for a Network_Interface_in_IP_Network
#
# Revision Dates
#     1-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

import _CNDB._OMP.IP_DNS_Alias

_Ancestor_Essence = CNDB.OMP.IP_DNS_Alias

class IP6_DNS_Alias (_Ancestor_Essence) :
    """DNS alias for IPv6 address"""

    class _Predicates (_Ancestor_Essence._Predicates) :

        unique_name = Pred.Unique.New_Pred \
            (  * _Ancestor_Essence._unique_name_vars
            , ** _Ancestor_Essence._unique_name_dict
            )

    # end class _Predicates

# end class IP6_DNS_Alias

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP6_DNS_Alias
