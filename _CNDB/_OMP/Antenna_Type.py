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
#    CNDB.OMP.Antenna_Type
#
# Purpose
#    Model the type of antennas in CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    28-Mar-2012 (CT) Use `Frequency_Interval` instead of `Float_Interval`
#                     for `frequency`
#    10-May-2012 (RS) fix typo, make frequency and gain necessary
#     5-Dec-2012 (RS) Add `polarization`
#     7-Dec-2012 (RS) Remove `frequency`, add predicate `band_exists`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _CNDB                      import CNDB
import _CNDB._OMP
import _CNDB._OMP.Device_Type
from   _CNDB._OMP.Attr_Type             import A_Polarization

_Ancestor_Essence = CNDB.OMP.Device_Type

class Antenna_Type (_Ancestor_Essence) :
    """Model the type of antennas in CNDB.OMP."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class gain (A_Float) :
            """Describes how well the antenna converts input power into radio
               waves headed in a specified direction (in dBi).
            """

            kind               = Attr.Necessary

        # end class gain

        class polarization (A_Polarization) :
            """Antenna polarization."""

            kind               = Attr.Necessary

        # end class polarization

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class band_exists (Pred.Condition) :
            """There must be at least one frequency band for the antenna."""

            kind               = Pred.Region
            assertion          = "number_of_bands >= 1"
            attributes         = ("bands", )
            bindings           = dict \
                ( number_of_bands = "len (this.bands)"
                )

        # end class band_exists

    # end class _Predicates

# end class Antenna_Type

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Antenna_Type
