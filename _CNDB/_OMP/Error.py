# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.Error
#
# Purpose
#    Provide exception classes for package CNDB
#
# Revision Dates
#     1-Mar-2013 (CT) Creation
#    20-Jun-2014 (RS) Add `Cannot_Expire_Network`
#    16-Sep-2014 (CT) Add `No_Network_in_Pool`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CNDB                    import CNDB
import _CNDB._OMP
from   _TFL                     import TFL
from   _MOM                     import MOM

import _MOM.Error

from   _TFL.I18N                import _, _T, _Tn

class _CNDB_Error_ (MOM.Error.Error) :
    """Root class of CNDB exceptions"""

    _real_name = "Error"

Error = _CNDB_Error_ # end class

class Address_Already_Used (Error, ValueError) :
    """Address is already in use"""

    def __init__ (self, address, owner, requester, msg) :
        self.__super.__init__ (msg)
        self.address     = address
        self.owner       = owner
        self.requester   = requester
    # end def __init__

# end class Address_Already_Used

class Address_not_in_Network (Error, ValueError) :
    """Address is not in Network"""

    def __init__ (self, address, net_address, msg) :
        self.__super.__init__ (msg)
        self.address     = address
        self.net_address = net_address
    # end def __init__

# end class Address_not_in_Network

class No_Free_Address_Range (Error, ValueError) :
    """There is no free subrange available"""

    def __init__ (self, net_address, mask_len, message) :
        self.__super.__init__ (message)
        self.net_address = net_address
        self.mask_len    = mask_len
    # end def __init__

# end class No_Free_Address_Range

class No_Network_in_Pool (Error, ValueError) :
    """Pool doesn't have any networks."""

    def __init__ (self, pool) :
        self.__super.__init__ \
            ( _T ("Pool %(pool)s doesn't have any networks")
            % dict (pool = pool)
            )
        self.pool = pool
    # end def __init__

# end class No_Network_in_Pool

class Cannot_Free_Network (Error, ValueError) :
    """Can't free IP_Network object"""

    def __init__ (self, net_address, message) :
        self.__super.__init__ (message)
        self.net_address = net_address
    # end def __init__

# end class Cannot_Free_Network

if __name__ != "__main__" :
    CNDB.OMP._Export_Module ()
### __END__ CNDB.OMP.Error
