# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Belongs_to_Net_Device
#
# Purpose
#    Mixin for computed `my_net_device` attribute
#
# Revision Dates
#    14-Apr-2014 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Id_Entity

class Belongs_to_Net_Device (_Ancestor_Essence) :
    """Mixin for the query attribute `my_net_device`"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class my_net_device (A_Id_Entity) :
            """Net_Device this %(ui_type_name)s belongs to."""

            kind               = Attr.Query
            P_Type              = "CNDB.Net_Device"
            is_partial          = True ### `query` is defined by descendents

        # end class my_net_device

    # end class _Attributes

# end class Belongs_to_Net_Device

_Ancestor_Essence = CNDB.OMP.Link
_Mixin            = Belongs_to_Net_Device

class Belongs_to_Net_Device_Left (_Mixin, _Ancestor_Essence) :
    """Mixin for the query attribute `my_net_device`, delegated to
       `left.my_net_device`.
    """

    is_partial = True

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class my_net_device (_Mixin._Attributes.my_net_device) :

            query               = Q.left.my_net_device
            query_preconditions = (Q.left, )
            is_partial          = False

        # end class my_net_device

    # end class _Attributes

# end class Belongs_to_Net_Device_Left

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Belongs_to_Net_Device
