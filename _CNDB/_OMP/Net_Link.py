# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Net_Link
#
# Purpose
#    Model a link between two network interfaces
#
# Revision Dates
#    10-May-2012 (CT) Creation
#    18-May-2012 (CT) Change `not_inverse` to use `count`, not `one`
#    19-Sep-2012 (CT) Use `force_role_name`, not `role_name`
#    26-Feb-2013 (CT) Remove `is_partial = True`,
#                     i.e., allow links between different `Net_Interface`
#    20-May-2013 (CT) Add `link_ref_suffix` to `left` and `right`
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

import _CNDB._OMP.Net_Interface

_Ancestor_Essence = CNDB.OMP.Link2

class Net_Link (_Ancestor_Essence) :
    """Link between two network interfaces."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Left network interface"""

            role_type          = CNDB.OMP.Net_Interface
            force_role_name    = "left"
            link_ref_suffix    = "_net_link"

        # end class left

        class right (_Ancestor.right) :
            """Right network interface"""

            role_type          = CNDB.OMP.Net_Interface
            force_role_name    = "right"
            link_ref_suffix    = "_net_link"

        # end class right

        ### Non-primary attributes

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class left_not_right (Pred.Condition) :
            """`left` and `right` must be different objects!"""

            kind               = Pred.Object
            assertion          = "left != right"
            attributes         = ("left", "right")

        # end class left_not_right

        class not_inverse (Pred.Condition) :
            """There must not be a second link with `left` and `right`
               swapped.
            """

            kind               = Pred.Region
            assertion          = "inverse_count == 0"
            attributes         = ("left", "right")
            bindings           = dict \
                ( inverse_count  =
                    "this.ETM.query (left = right, right = left).count ()"
                )

        # end class not_inverse

    # end class _Predicates

# end class Net_Link

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Link
