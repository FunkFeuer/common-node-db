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
#    CNDB.OMP.Wireless_Mode
#
# Purpose
#    Model the mode a wireless device operates in
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `is_linkable`
#     6-Dec-2012 (RS) Add `belongs_to_node`, add `max_links`
#    17-Dec-2012 (CT) Change from essential type to basis for `A_Wireless_Mode`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _CNDB                    import CNDB
import _CNDB._OMP
from   _TFL                     import TFL

from   _TFL.I18N                import _, _T, _Tn

import _TFL._Meta.Object

class M_Wireless_Mode (TFL.Meta.Object.__class__) :
    """Meta class for wireless-mode classes"""

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "Wireless_Mode" :
            cls._m_add (name, cls.Table)
    # end def __init__

    def __str__ (cls) :
        return cls.__name__
    # end def __str__

    def _m_add (cls, name, Table) :
        name = unicode (name)
        assert name not in Table, "Name clash: `%s` <-> `%s`" % \
            (name, Table [name].__class__)
        Table [name] = cls
    # end def _m_add

# end class M_Wireless_Mode

class Wireless_Mode (TFL.Meta.Object) :

    __metaclass__ = M_Wireless_Mode

# end class Wireless_Mode

class Ad_Hoc (Wireless_Mode) :
    """Ad-Hoc mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is cls
    # end def is_linkable

# end class Ad_Hoc

class AP (Wireless_Mode) :
    """Access point mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is Client
    # end def is_linkable

# end class AP

class Client (Wireless_Mode) :
    """Client mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is AP
    # end def is_linkable

# end class Client

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Wireless_Mode
