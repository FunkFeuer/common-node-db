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
#    CNDB.OMP.Antenna_Band
#
# Purpose
#    Model a supported frequency band of an Antenna_Type
#
# Revision Dates
#     7-Dec-2012 (RS) Creation
#    15-May-2013 (CT) Replace `auto_cache` by `link_ref_attr_name`
#    ««revision-date»»···
#--

from   _MOM.import_MOM            import *
from   _CNDB                      import CNDB
import _CNDB._OMP
from   _MOM._Attr.Number_Interval import *

_Ancestor_Essence = CNDB.OMP.Link1

class Antenna_Band (_Ancestor_Essence) :
    """Frequency Band of an antenna type"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """The antenna type for this band"""

            role_type          = CNDB.OMP.Antenna_Type
            ui_allow_new       = False
            link_ref_attr_name = "band"

        # end class left

        class band (A_Frequency_Interval) :
            """Frequency range an antenna type supports."""

            kind               = Attr.Primary

        # end class frequency


    # end class _Attributes

# end class Antenna_Band

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Antenna_Band
