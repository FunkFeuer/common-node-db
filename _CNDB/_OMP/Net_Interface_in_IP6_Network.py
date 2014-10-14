# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Dr. Ralf Schlatterbeck All rights reserved
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
#    CNDB.OMP.Net_Interface_in_IP6_Network
#
# Purpose
#    Model a Net interface in an IPv6 network
#
# Revision Dates
#    22-May-2012 (RS) Creation
#    21-Sep-2012 (RS) set `is_partial`
#     5-Mar-2013 (CT) Remove redefinition of `ip_address` (gone from parent)
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

from   _CNDB._OMP.Attr_Type           import *
import _CNDB._OMP.Net_Interface_in_IP_Network

_Ancestor_Essence = CNDB.OMP.Net_Interface_in_IP_Network

class Net_Interface_in_IP6_Network (_Ancestor_Essence) :
    """Net interface in IPv6 network"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class right (_Ancestor.right) :
            """IP Network."""

            role_type          = CNDB.OMP.IP6_Network
            auto_rev_ref       = True

        # end class right

        ### Non-primary attributes

    # end class _Attributes

# end class Net_Interface_in_IP6_Network

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Interface_in_IP6_Network
