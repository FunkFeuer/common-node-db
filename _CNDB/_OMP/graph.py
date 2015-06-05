# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SRM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.graph
#
# Purpose
#    Graph describing CNDB (partial) object model
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
#    18-Oct-2012 (RS) Add `Wired_Interface` and associations
#    18-Oct-2012 (RS) Add `Node` `IS_A` `Subject`
#    22-Nov-2012 (CT) Add `Role.left` to `Wireless_Channel`
#    22-Nov-2012 (RS) Move `Net_Interface_in_IP_Network.right` to South
#     8-Dec-2012 (RS) Add `Antenna_Band`
#    17-Dec-2012 (CT) Remove `Wireless_Mode`
#    17-Dec-2012 (RS) Skip explicit links from children of `Net_Interface`
#    26-Feb-2013 (CT) Remove `Wired_Link` and `Wireless_Link`
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    11-Dec-2014 (CT) Fix geometry attributes of `Node.manager`
#     5-Jun-2015 (CT) Remove obsolete link `Node-is_a-Subject`
#     5-Jun-2015 (CT) Simplify layout to prepare for future additions
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW._OMP._PAP         import PAP

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip

import _MOM._Graph.Command
import _MOM._Graph.Entity

from   _TFL                   import sos
from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.I18N              import _, _T

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.CNDB.Device
            ( Role.left
                ( ET.CNDB.Device_Type_made_by_Company
                    ( Role.right
                        ( IS_A.PAP.Group
                            ( IS_A.PAP.Subject
                                ( offset = CD.S
                                )
                            , offset = CD.S
                            )
                        , offset = CD.NE
                        )
                    , offset = CD.E
                    )
                , offset       = CD.E
                )
            , Child.CNDB.Antenna
                ( Role.left
                    ( IS_A.CNDB.Device_Type
                    , ET.CNDB.Antenna_Band (offset = CD.E)
                    , offset = CD.E
                    )
                , offset = CD.N
                )
            , Child.CNDB.Net_Device
                ( Role.left
                    ( IS_A.CNDB.Device_Type
                    , offset       = CD.N
                    )
                , Attr.node
                    ( Attr.manager
                        ( guide_offset = 0.75
                        , source_side = "E"
                        , target_side = "W"
                        )
                    , Attr.owner
                        ( guide_offset = 0.5
                        , source_side  = "E"
                        , target_side  = "W"
                        )
                    , offset = CD.N + CD.E
                    )
                , ET.CNDB.Net_Interface (offset = CD.S + CD.E)
                , offset = CD.E + CD.S * 2
                )
            )
        , ET.CNDB.Net_Interface
            ( Role.left (guide_offset = 1.0)
            , ET.CNDB.Net_Link (offset = CD.S)
            , ET.CNDB._Net_Credentials_
                ( Role.left (guide_offset = 1.0)
                , offset = CD.N
                )
            , ET.CNDB.Net_Interface_in_IP_Network
                ( Role.right
                    ( Child.CNDB.IP4_Network (offset = CD.SW)
                    , Child.CNDB.IP6_Network (offset = CD.S)
                    , offset = CD.E
                    )
                , Role.left
                    ( guide_offset = 0.5
                    )
                , offset = CD.E
                )
            , Child.CNDB.Wireless_Interface
                ( Skip.left
                , ET.CNDB.Wireless_Interface_uses_Antenna
                    ( Role.left
                        ( guide_offset = 1.5
                        )
                    , Role.right
                        ( anchor      = False
                        , source_side = "W"
                        , target_side = "W"
                        )
                    , offset = CD.N + CD.W
                    )
                , ET.CNDB.Wireless_Interface_uses_Wireless_Channel
                    ( Role.right
                        ( Role.left
                            ( offset = CD.S
                            )
                        , offset = CD.S
                        )
                    , offset = CD.W
                    )
                , offset = CD.W
                )
            , Child.CNDB.Wired_Interface
                ( Skip.left
                , offset = CD.SW
                )
            )
        , desc  = _T ("Graph displaying Funkfeuer object model")
        , title = _T ("CNDB graph")
        )
# end def graph

class Command (MOM.Graph.Command) :

    PNS                   = CNDB

    _defaults             = dict \
        ( name            = "nodedb"
        )

    def _app_dir_default (self) :
        return sos.path.normpath (sos.path.join (self.app_dir, "../..", "doc"))
    # end def _app_dir_default

# end class Command

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
else :
    import _GTW._OMP._PAP.import_PAP
    import _GTW._OMP._Auth.import_Auth
    import _CNDB._OMP.import_CNDB
    Command () ()
### __END__ CNDB.OMP.graph
