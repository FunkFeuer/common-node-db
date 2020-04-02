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
#    CNDB.OMP.Net_Credentials
#
# Purpose
#    Model credentials for a network interface
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#     6-Dec-2012 (RS) Add `belongs_to_node`, add `max_links`
#    15-May-2013 (CT) Replace `auto_cache` by `link_ref_attr_name`
#    20-May-2013 (CT) Set `_Net_Credentials_.left.link_ref_suffix` to `None`
#    13-Aug-2013 (CT) Add `key.typ`
#    30-Sep-2013 (CT) Mixin `Belongs_to_Node_Left`, not `Belongs_to_Node`
#    14-Apr-2014 (CT) Add mixin `Belongs_to_Net_Device_Left`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _MOM.import_MOM        import _A_String_Ascii_
from   _CNDB                  import CNDB
import _CNDB._OMP

import _CNDB._OMP.Net_Interface
import _CNDB._OMP.Belongs_to_Net_Device
import _CNDB._OMP.Belongs_to_Node

from   _TFL.Regexp            import Regexp, re

_Ancestor_Essence = CNDB.OMP.Link1
_Mixin_1 = CNDB.OMP.Belongs_to_Node_Left
_Mixin_2 = CNDB.OMP.Belongs_to_Net_Device_Left

class _Net_Credentials_ (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Model credentials used by a Net_Interface, e.g., `802.1x`
       authentication for a wired interface, or WPA authentication for a WiFi
       interface.
    """

    is_partial = True

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The network interface using these credentials."""

            role_type          = CNDB.OMP.Net_Interface
            role_name          = "interface"
            link_ref_attr_name = "credentials"
            link_ref_suffix    = None
            max_links          = 1

        # end class left

        ### *** BEWARE ***
        ### To ensure that a `Net_Interface` has only one `credentials`, no
        ### other essential primary key attributes must be defined here or by
        ### derived classes

    # end class _Attributes

# end class _Net_Credentials_

_Ancestor_Essence = _Net_Credentials_

class WPA_Credentials (_Ancestor_Essence) :
    """Model credentials necessary for WPA authentication."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class key (Eval_Mixin, _A_String_Ascii_) :
            """Key used for WPA authentication."""

            kind               = Attr.Required
            max_length         = 32
            typ                = "Key"

            ### allow characters up to "\xFF"
            _cooked_re        = Regexp \
                ( "^[\x00-\xFF]*$"
                , re.VERBOSE
                )

        # end class key

    # end class _Attributes

# end class WPA2

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Credentials
