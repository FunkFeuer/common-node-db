# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.Net_Interface_in_IP_Network
#
# Purpose
#    Model a Net interface in an IP network
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    23-May-2012 (RS) Use `_A_IP_Address_` for `ip_address`
#    20-Sep-2012 (RS) Add `auto_cache_np`, `auto_derive_np` to `left`
#                     remove `auto_cache` from `right`
#     5-Mar-2013 (CT) Set `right.max_links = 1`
#     5-Mar-2013 (CT) Replace `ip_address` by `mask_len`
#     5-Mar-2013 (CT) Add predicates `network_not_split` and `valid_network`
#    15-May-2013 (CT) Rename `auto_cache_np` to `auto_rev_ref_np`
#    13-Aug-2013 (CT) Set `Net_Interface_in_IP_Network.is_relevant` to `True`
#     7-Apr-2014 (CT) Remove `~ electric` from `valid_mask_len` query
#    13-Jun-2014 (RS) Add `name`
#     5-Sep-2014 (CT) Mixin `Belongs_to_Node_Left`, `Belongs_to_Net_Device_Left`
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _CNDB                    import CNDB
import _CNDB._OMP

from   _CNDB._OMP.Attr_Type           import *
from   _GTW._OMP._DNS.Attr_Type import A_DNS_Label

import _CNDB._OMP.Net_Interface
import _CNDB._OMP.IP_Network

_Mixin_1 = CNDB.OMP.Belongs_to_Node_Left
_Mixin_2 = CNDB.OMP.Belongs_to_Net_Device_Left
_Ancestor_Essence = CNDB.OMP.Link2

class Net_Interface_in_IP_Network (_Mixin_1, _Mixin_2, _Ancestor_Essence) :
    """Net interface in IP network"""

    is_partial  = True
    is_relevant = True

    class _Attributes \
              ( _Mixin_1._Attributes
              , _Mixin_2._Attributes
              , _Ancestor_Essence._Attributes
              ) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Network interface."""

            role_type          = CNDB.OMP.Net_Interface
            auto_derive_np     = True
            auto_rev_ref       = True
            auto_rev_ref_np    = True

        # end class left

        class right (_Ancestor.right) :
            """IP Network."""

            role_type          = CNDB.OMP.IP_Network
            max_links          = 1

        # end class right

        ### Non-primary attributes

        class mask_len (A_Int) :
            """Network mask used for this IP Network."""

            kind               = Attr.Required

        # end class mask_len

        class name (A_DNS_Label) :
            """DNS name for this IP Network."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                if obj and obj.left :
                    return obj.left.name
            # end def computed

        # end class name

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class network_not_split (Pred.Condition) :
            """To be eligible to be assigned to the
               `%(type_base_name.lower ())s` `left`, the network `right` must
               not be split into sub-networks.
            """

            kind               = Pred.Object
            assertion          = "not right.has_children"
            attributes         = ("left", "right.has_children")

        # end class network_not_split

        class valid_mask_len (Pred.Condition) :
            """The `mask_len` must match the one of `right` or of any
               network containing `right`.
            """

            kind               = Pred.Object
            assertion          = "mask_len in possible_mask_lens"
            attributes         = ("mask_len", "right.net_address")
            bindings           = dict \
                ( possible_mask_lens =
                    """sorted """
                      """( right.ETM.query """
                            """( (Q.net_address.CONTAINS (right.net_address))"""
                            """).attr ("net_address.mask_len")"""
                      """)"""
                )

        # end class valid_mask_len

        class valid_network (Pred.Condition) :
            """To be eligible to be assigned to the
               `%(type_base_name.lower ())s` `left`, the network `right` must
               have been explicitly allocated to an `owner`.
            """

            kind               = Pred.Object
            assertion          = \
                "right.owner is not None and not right.electric"
            attributes         = ("left", "right.owner", "right.electric")

        # end class valid_network

    # end class _Predicates

# end class Net_Interface_in_IP_Network

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Net_Interface_in_IP_Network
