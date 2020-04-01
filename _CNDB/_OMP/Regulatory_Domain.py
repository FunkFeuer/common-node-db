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
#    CNDB.OMP.Regulatory_Domain
#
# Purpose
#    Model a wireless regulatory domain
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Object

class Regulatory_Domain (_Ancestor_Essence) :
    """Wireless Regulatory Domain"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class countrycode (A_String) :
            """Two-letter country-code"""

            kind               = Attr.Primary
            max_length         = 2
            ignore_case        = True

        # end class countrycode

    # end class _Attributes

# end class Regulatory_Domain

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Regulatory_Domain
