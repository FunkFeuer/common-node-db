# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SRM.
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
#    FFM.Graph
#
# Purpose
#    Graph describing FFM (partial) object model
#
# Revision Dates
#    27-Aug-2012 (RS) Creation
#    30-Aug-2012 (CT) Rearrange graph, add more nodes/links
#    31-Aug-2012 (CT) Adapt to MOM.Graph.Spec API change
#     6-Sep-2012 (CT) Add lots more nodes/links, rearrange graph
#    18-Sep-2012 (RS) Put `Node` and `Subject` and descendants in the middle
#                     for new Id_Entities of `Node`, fixes tanzer constraint
#    19-Sep-2012 (CT) Disentangle links, remove whitespace
#    24-Sep-2012 (CT) Add `Command`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _FFM

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.FFM.Device
            ( Role.left
                ( ET.FFM.Device_Type_made_by_Company
                    ( Role.right
                        ( IS_A.PAP.Subject
                            ( Child.PAP.Person (offset = CD.N)
                            , offset = CD.W
                            )
                        , offset = CD.S
                        )
                    , offset = CD.W
                    )
                , offset       = CD.E * 4
                , guide_offset = 1.0
                , source_side  = "N"
                , target_side  = "N"
                )
            , Child.FFM.Antenna
                ( Role.left
                    ( IS_A.FFM.Device_Type
                    , offset = CD.E * 4
                    )
                , offset = CD.N
                )
            , Child.FFM.Net_Device
                ( Role.left
                    ( IS_A.FFM.Device_Type
                    , guide_offset = 1.0
                    , offset       = CD.E * 3
                    , source_side  = "S"
                    , target_side  = "S"
                    )
                , Attr.node
                    ( Attr.manager
                    , Attr.owner
                        ( guide_offset = 0.75
                        , source_side  = "E"
                        , target_side  = "W"
                        )
                    , offset = CD.N
                    )
                , ET.FFM.Net_Interface (offset = CD.S + CD.E * 2)
                , offset = CD.E + CD.S
                )
            )
        , ET.FFM.Net_Interface
            ( Role.left (guide_offset = 0.75)
            , ET.FFM._Net_Credentials_ (offset = CD.SE)
            , ET.FFM.Net_Interface_in_IP_Network
                ( Role.right
                    ( Child.FFM.IP4_Network (offset = CD.S)
                    , Child.FFM.IP6_Network (offset = CD.N)
                    , offset = CD.E
                    )
                , offset = CD.E
                )
            , Child.FFM.Wireless_Interface
                ( ET.FFM.Wireless_Link
                    ( Child.FFM.Net_Link (offset = CD.E)
                    , offset = CD.S
                    )
                , ET.FFM._Wireless_Mode_
                    ( Child.FFM.Ad_Hoc_Mode
                        ( offset = CD.SW
                        )
                    , Child.FFM.AP_Mode
                        ( offset = CD.S
                        )
                    , Child.FFM.Client_Mode
                        ( offset = CD.SE
                        )
                    , offset = CD.SW
                    )
                , ET.FFM.Wireless_Interface_uses_Antenna
                    ( Role.left (guide_offset = 1.5)
                    , Role.right
                        ( anchor      = False
                        , source_side = "W"
                        , target_side = "W"
                        )
                    , offset = CD.N + CD.W * 2
                    )
                , ET.FFM.Wireless_Interface_uses_Wireless_Channel
                    ( Role.right (offset = CD.W)
                    , offset = CD.W
                    )
                , offset = CD.W
                )
            )
        )
# end def graph

if __name__ != "__main__" :
    FFM._Export ("*")
else :
    import _GTW._OMP._PAP.import_PAP
    import _GTW._OMP._Auth.import_Auth
    import _FFM.import_FFM
    import _MOM._Graph.Command
    from   _TFL import sos

    class Command (MOM.Graph.Command) :

        PNS                   = FFM

        PNS_Aliases           = dict \
            ( Auth            = GTW.OMP.Auth
            , PAP             = GTW.OMP.PAP
            )

        _defaults             = dict \
            ( name            = "nodedb"
            )

        def _app_dir_default (self) :
            return sos.path.normpath (sos.path.join (self.app_dir, "..", "doc"))
        # end def _app_dir_default

    # end class Command

    command = Command ()
    command ()
### __END__ FFM.Graph
