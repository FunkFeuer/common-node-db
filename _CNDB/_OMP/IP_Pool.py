# -*- coding: utf-8 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
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
#    CNDB.OMP.IP_Pool
#
# Purpose
#    Model Attributes of an IP network pool
#
# Revision Dates
#    20-Jun-2014 (RS) Creation
#    23-Jun-2014 (RS) Add `cool_down_period`, rename `left.link_ref_attr_name`
#     3-Jul-2014 (RS) `IP_Pool` no longer `Link1`, rename
#                     `_A_IP_Netmask_Interval_`
#    16-Sep-2014 (CT) Add `allocate` method
#    23-Sep-2014 (CT) Add `ui_display_x`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _CNDB                      import CNDB
import _CNDB._OMP
from   _CNDB._OMP.Attr_Type             import _A_IP_Netmask_Interval_

from   _MOM._Attr.Date_Time_Delta import A_Date_Time_Delta

import _CNDB._OMP.IP_Network

_Ancestor_Essence = CNDB.OMP.Object

class IP_Pool (_Ancestor_Essence) :
    """Attributes of an IP network pool."""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Name of IP_Pool"""

            kind               = Attr.Primary
            max_length         = 40
            ignore_case        = True

        # end class left

        ### Non-primary attributes

        class cool_down_period (A_Date_Time_Delta) :
            """Cool down period for this %(type_name)s."""

            kind               = Attr.Optional

        # end class cool_down_period

        class netmask_interval (_A_IP_Netmask_Interval_) :
            """Limit netmasks to allocate from this %(type_name)s."""

            kind               = Attr.Optional

        # end class netmask_interval

        class node (A_Id_Entity) :
            """Node for which this `%(type_name)s` is reserved."""

            kind               = Attr.Optional
            P_Type             = CNDB.OMP.Node
            ui_allow_new       = False

        # end class node

        class ui_display_x (A_String) :
            """Extended display in user interface: includes IP_Networks"""

            kind               = Attr.Computed
            max_length         = 0

            def computed (self, obj) :
                result = obj.ui_display
                nws    = obj.ip_networks
                if nws :
                    result += " [%s]" % \
                        (", ".join (sorted (n.ui_display for n in nws)), )
                return result
            # end def computed

        # end class ui_display_x

    # end class _Attributes

    def allocate (self, mask_len, owner) :
        errors   = []
        networks = self.ip_networks
        if networks :
            for nw in sorted (networks, key = Q.net_address) :
                try :
                    return nw.allocate (mask_len, owner)
                except CNDB.OMP.Error.No_Free_Address_Range as exc :
                    errors.append (exc)
            raise errors [-1]
        else :
            raise CNDB.OMP.Error.No_Network_in_Pool (self)
    # end def allocate

# end class IP_Pool

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP_Pool
