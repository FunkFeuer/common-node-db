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
#    CNDB.OMP.Node
#
# Purpose
#    Model a node of CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    19-Jul-2012 (RS) Add `position`
#    20-Jul-2012 (RS) `Node` no longer inherits from `PAP.Subject`
#    18-Sep-2012 (RS) Add `owner` and `manager`
#    22-Sep-2012 (RS) make `name` `A_DNS_Label`
#    11-Oct-2012 (RS) `map_p` -> `show_in_map`
#    12-Oct-2012 (RS) Make `Node` a `PAP.Subject` again.
#    16-Oct-2012 (CT) Correct `refuse_links`
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    13-Dec-2012 (CT) Set `owner.P_Type` to `PAP.Person`
#    13-Dec-2012 (CT) Set `owner.ui_allow_new` to `False`
#    14-Dec-2012 (CT) Return `obj`, not `self`, from `belongs_to_node.computed`
#    17-Dec-2012 (CT) Set `manager.ui_allow_new` to `False`
#     4-Apr-2013 (CT) Change `owner.P_Type` back to `PAP.Subject`
#    16-Apr-2013 (CT) Set `owner.refuse_e_types` to `CNDB.OMP.Node`
#    17-Apr-2013 (CT) Use `Computed_Set_Mixin`, not `Computed_Mixin`
#     3-May-2013 (CT) Add attribute `address`,
#                     put `Node_has_Address` into `refuse_links`
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node`,
#                     change `belongs_to_node` to query `Q.SELF`
#     1-Oct-2013 (CT) Set `belongs_to_node.hidden` to `True`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#     5-Jun-2014 (RS) Remove duplicate `my_node`, add `desc`
#    13-Jun-2014 (RS) Add `ui_name` for `desc`
#    13-Jun-2014 (RS) `Node` is no longer a `PAP.Subject`
#     4-Sep-2014 (RS) Change `manager` from `PAP.Person` to `PAP.Subject`
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _MOM._Attr.Position      import A_Position
from   _CNDB                    import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP           import PAP, Person, Subject, Address
from   _GTW._OMP._DNS.Attr_Type import A_DNS_Label

import _CNDB._OMP.Belongs_to_Node

_Ancestor_Essence = CNDB.OMP.Object
_Mixin            = CNDB.OMP.Belongs_to_Node

class Node (_Mixin, _Ancestor_Essence) :
    """Model a node of CNDB"""

    class _Attributes \
              ( _Mixin._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor    = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_DNS_Label) :
            """Name of the node"""

            kind               = Attr.Primary
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class address (A_Id_Entity) :
            """Address of the node (if stationary)."""

            kind               = Attr.Optional
            P_Type             = PAP.Address
            ui_allow_new       = True

        # end class address

        class desc (A_Text) :
            """Description of the node"""

            kind               = Attr.Optional
            ui_name            = "Description"

        # end class desc

        class manager (A_Id_Entity) :
            """Manager of the node"""

            kind               = Attr.Required
            P_Type             = PAP.Subject
            ui_allow_new       = False

        # end class manager

        class my_node (_Mixin._Attributes.my_node) :
            """Node to which this node belongs.

               Just an alias to the node itself to be compatible with all
               other entities belonging to nodes.
            """

            query              = Q.SELF
            hidden             = True

        # end class my_node

        class owner (A_Id_Entity) :
            """Owner of the node, defaults to manager"""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            P_Type             = PAP.Subject
            ui_allow_new       = False

            def computed (self, obj) :
                if obj :
                    return obj.manager
            # end def computed

         # end class owner

        class position (A_Position) :
            """GPS position and optional height of the node"""

            kind               = Attr.Optional

        # end class position

        class show_in_map (A_Boolean) :
            """Show in map."""

            kind               = Attr.Optional
            default            = True

        # end class show_in_map

    # end class _Attributes

# end class Node

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Node
