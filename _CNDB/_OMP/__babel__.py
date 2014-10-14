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
#    CNDB.OMP.__babel__
#
# Purpose
#    This file is the entry point for the Babel translation extraction
#    process.
#
# Revision Dates
#    28-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM import *
import _MOM.Babel
import _CNDB._OMP.import_CNDB

def main (encoding, config, method) :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
    from   _CNDB import CNDB
    import _CNDB._OMP
    return MOM.Babel.Add_Translations \
        ( encoding, config, method
        , MOM.App_Type ("CNDB", CNDB).Derived (EMS, DBW)
        )
# end def main

### __END__ CNDB.OMP.__babel__
