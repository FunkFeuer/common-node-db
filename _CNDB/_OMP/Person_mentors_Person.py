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
#    CNDB.OMP.Person_mentors_Person
#
# Purpose
#    Model mentor relationship between persons
#
# Revision Dates
#    12-Sep-2012 (RS) Creation
#    13-Sep-2012 (RS) Mentored person is `apprentice`
#    19-Sep-2012 (CT) Derive `right` from `_Ancestor.right`, not `.left`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Person

_Ancestor_Essence = CNDB.OMP.Link2

class Person_mentors_Person (_Ancestor_Essence) :
    """Person is the mentor of another person."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The Person mentoring another person."""

            role_type          = PAP.Person
            role_name          = "mentor"

        # end class left

        class right (_Ancestor.right) :
            """The Person being mentored."""

            role_type          = PAP.Person
            role_name          = "apprentice"

        # end class right

    # end class _Attributes

# end class Person_mentors_Person

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Person_mentors_Person
