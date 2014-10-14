# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Wireless_Interface_uses_Antenna
#
# Purpose
#    Model the antenna used by a wireless interface
#
# Revision Dates
#    28-Mar-2012 (CT) Creation
#    10-May-2012 (RS) Allow multiple interfaces to use same antenna
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    15-May-2013 (CT) Replace `auto_cache` by
#                     `rev_ref_attr_name`, `auto_rev_ref`
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node_Left`, not `Belongs_to_Node`
#    14-Apr-2014 (CT) Add mixin `Belongs_to_Net_Device_Left`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

from   _CNDB._OMP.Attr_Type         import *
import _CNDB._OMP.Antenna
import _CNDB._OMP.Wireless_Interface
import _CNDB._OMP.Belongs_to_Net_Device
import _CNDB._OMP.Belongs_to_Node

_Ancestor_Essence = CNDB.OMP.Link2
_Mixin_1 = CNDB.OMP.Belongs_to_Node_Left
_Mixin_2 = CNDB.OMP.Belongs_to_Net_Device_Left

class Wireless_Interface_uses_Antenna (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Antenna used by a wireless interface"""

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Wireless interface."""

            role_type          = CNDB.OMP.Wireless_Interface
            rev_ref_attr_name  = "interface"

        # end class left

        class right (_Ancestor.right) :
            """Antenna."""

            role_type          = CNDB.OMP.Antenna
            auto_rev_ref       = True
            ui_allow_new       = True
            max_links          = 1

        # end class right

        ### Non-primary attributes

        class relative_height (A_Float) :
            """Height relative to device the antenna is connected to."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0

        # end class relative_height

    # end class _Attributes

# end class Wireless_Interface_uses_Antenna

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Wireless_Interface_uses_Antenna
