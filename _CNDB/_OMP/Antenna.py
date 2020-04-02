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
#    CNDB.OMP.Antenna
#
# Purpose
#    Model an antenna in CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `azimuth` and `orientation` to `A_Angle`
#    30-Aug-2012 (CT) Add `gain`
#    08-Oct-2012 (RS) `inclination` -> `elevation`
#    05-Dec-2012 (RS) Remove `orientation`, add `polarization`
#    06-Dec-2012 (RS) Add `belongs_to_node`
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    25-Feb-2013 (CT) Add `belongs_to_node.query_preconditions`
#    26-Feb-2013 (CT) Disable `belongs_to_node`
#    17-Apr-2013 (CT) Use `Computed_Set_Mixin`, not `Computed_Mixin`
#    14-Aug-2013 (CT) Re-enable `belongs_to_node`
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node`
#    27-Feb-2014 (CT) Rename `elevation` to `elevation_angle`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    14-Apr-2014 (CT) Add `my_net_device`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

import _CNDB._OMP.Antenna_Type
import _CNDB._OMP.Device
import _CNDB._OMP.Node
from   _CNDB._OMP.Attr_Type         import A_Polarization
import _CNDB._OMP.Belongs_to_Node
import _CNDB._OMP.Belongs_to_Net_Device

_Ancestor_Essence = CNDB.OMP.Device
_Mixin_1            = CNDB.OMP.Belongs_to_Node
_Mixin_2            = CNDB.OMP.Belongs_to_Net_Device

class Antenna (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Model an antenna used by a CNDB node."""

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Type of antenna"""

            role_type          = CNDB.OMP.Antenna_Type

        # end class left

        ### Non-primary attributes

        class azimuth (A_Angle) :
            """Azimuth of antenna orientation (in degrees)."""

            kind               = Attr.Required
            explanation        = """
              Azimuth is measured clockwise from north, i.e.,
              N <-> 0, E <-> 90, S <-> 180, W <-> 270.
              """

        # end class azimuth

        class elevation_angle (A_Int) :
            """ Elevation angle of the beam from the horizontal plane
                (in degrees).
            """

            example            = "42"
            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0
            max_value          = 90
            min_value          = -90

        # end class elevation_angle

        class gain (A_Float) :
            """Describes how well the antenna converts input power into radio
               waves headed in a specified direction (in dBi). Per default,
               `antenna_type.gain` is used, but can be overriden here.
            """

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                if obj.left :
                    return obj.left.gain
            # end def computed

        # end class gain

        class my_net_device (_Mixin_2._Attributes.my_net_device) :

            query               = Q.interface.my_net_device
            query_preconditions = (Q.interface, )

        # end class my_net_device

        class my_node (_Mixin_1._Attributes.my_node) :

            query               = Q.interface.my_node
            query_preconditions = (Q.interface, )

        # end class my_node

        class polarization (A_Polarization) :
            """Antenna polarization. Per default,
               `antenna_type.polarization` is used, but can be overriden here.
            """

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                if obj.left :
                    return obj.left.polarization
            # end def computed

        # end class polarization

    # end class _Attributes

# end class Antenna

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Antenna
