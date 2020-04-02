# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.Routing_Zone
#
# Purpose
#    Model the routing of a zone of CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
import _CNDB._OMP.Zone

_Ancestor_Essence = CNDB.OMP.Link1

class Routing_Zone (_Ancestor_Essence) :
    """Model the routing of a zone of CNDB.OMP."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The zone that's routed for."""

            role_type          = CNDB.OMP.Zone
            ui_allow_new       = True

        # end class left

    # end class _Attributes

# end class Routing_Zone

_Ancestor_Essence = Routing_Zone

class Routing_Zone_OLSR (_Ancestor_Essence) :
    """Routing zone using the OLSR routing protocol."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### XXX define the attributes necessary to parameterize the routing
        ### for `zone`

    # end class _Attributes

# end class Routing_Zone_OLSR

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Routing_Zone
