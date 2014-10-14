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
#    CNDB.OMP.Net_Device
#
# Purpose
#    Model a network device of CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    30-Aug-2012 (CT) Add `primary` attribute `node`
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    26-Jan-2013 (CT) Define `belongs_to_node.query`, not `.query_fct`
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node`
#    10-Apr-2014 (CT) Set `node.rev_ref_attr_name` to `net_devices`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    14-Apr-2014 (CT) Add `my_net_device`
#    26-Apr-2014 (CT) Set `node.ui_allow_new` to `False`
#    30-Apr-2014 (CT) Set `node.Kind_Mixins` to `Attr.Init_Only_Mixin`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
import _CNDB._OMP.Device
import _CNDB._OMP.Net_Device_Type
import _CNDB._OMP.Node
import _CNDB._OMP.Belongs_to_Node
import _CNDB._OMP.Belongs_to_Net_Device

_Ancestor_Essence = CNDB.OMP.Device
_Mixin_1            = CNDB.OMP.Belongs_to_Node
_Mixin_2            = CNDB.OMP.Belongs_to_Net_Device

class Net_Device (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Model a network device of CNDB.OMP."""

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

            role_type          = CNDB.OMP.Net_Device_Type
            show_in_ui_selector= False

        # end class left

        class node (A_Id_Entity) :
            """`Node` to which the `net_device` is connected."""

            kind               = Attr.Primary
            P_Type             = CNDB.OMP.Node
            rev_ref_attr_name  = "net_devices"
            ui_allow_new       = False
            Kind_Mixins        = (Attr.Init_Only_Mixin, )

        # end class node

        class my_net_device (_Mixin_2._Attributes.my_net_device) :
            """Net_Device to which this net_device belongs.

               Just an alias to the net_device itself to be compatible with all
               other entities belonging to net_devices.
            """

            query              = Q.SELF
            hidden             = True

        # end class my_net_device

        class my_node (_Mixin_1._Attributes.my_node) :

            query              = Q.node

        # end class my_node

    # end class _Attributes

# end class Net_Device

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Device
