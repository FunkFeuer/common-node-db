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
#    CNDB.OMP.Belongs_to_Node
#
# Purpose
#    Mixin for computed `my_node` attribute
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    26-Jan-2013 (CT) Define `belongs_to_node.query`, not `.query_fct`
#    25-Feb-2013 (CT) Add `belongs_to_node.query_preconditions`
#    26-Feb-2013 (CT) Disable `belongs_to_node`
#    14-Aug-2013 (CT) Re-enable `belongs_to_node`
#    14-Aug-2013 (CT) Add `is_partial = True`,
#                     derive from `CNDB.OMP.Id_Entity`, not `CNDB.OMP.Entity`
#     4-Sep-2013 (CT) Derive from `CNDB.OMP.Link`, not `CNDB.OMP.Id_Entity`
#    30-Sep-2013 (CT) Split into partial `Belongs_to_Node`, non-partial
#                     `Belongs_to_Node_Left`
#     1-Oct-2013 (CT) Rename from `_Belongs_to_Node_` to `Belongs_to_Node`
#     1-Oct-2013 (CT) Remove `belongs_to_node.hidden = True`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#     4-Sep-2014 (CT) Add query attribute `my_group`
#    12-Sep-2014 (CT) Simplify `my_group.query`, `my_person.query`
#                     (use type restriction in `query`)
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Id_Entity

class Belongs_to_Node (_Ancestor_Essence) :
    """Mixin for the query attribute `my_node`"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class my_group (A_Id_Entity) :
            """Group this %(ui_type_name)s is managed or owned by."""

            kind                = Attr.Query
            P_Type              = "PAP.Group"
            query               = \
                Q.my_node.OR (Q.manager, Q.owner) ["PAP.Group"]
            hidden              = True

        # end class my_group

        class my_node (A_Id_Entity) :
            """Node this %(ui_type_name)s belongs to."""

            kind                = Attr.Query
            P_Type              = "CNDB.Node"
            is_partial          = True ### `query` is defined by descendents

        # end class my_node

        class my_person (A_Id_Entity) :
            """Person this %(ui_type_name)s is managed or owned by."""

            kind                = Attr.Query
            P_Type              = "PAP.Person"
            query               = \
                Q.my_node.OR (Q.manager, Q.owner) ["PAP.Person"]
            hidden              = True

        # end class my_person

    # end class _Attributes

# end class Belongs_to_Node

_Ancestor_Essence = CNDB.OMP.Link
_Mixin            = Belongs_to_Node

class Belongs_to_Node_Left (_Mixin, _Ancestor_Essence) :
    """Mixin for the query attribute `my_node`, delegated to
       `left.my_node`.
    """

    is_partial = True

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class my_node (_Mixin._Attributes.my_node) :

            query               = Q.left.my_node
            query_preconditions = (Q.left, )
            is_partial          = False

        # end class my_node

    # end class _Attributes

# end class Belongs_to_Node_Left

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Belongs_to_Node
