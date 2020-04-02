# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.Command
#
# Purpose
#    Base class for application and command handler for CNDB based applications
#
# Revision Dates
#     5-Sep-2014 (CT) Creation (factored from FFW)
#     5-Sep-2014 (MB) Added garbage collect command
#    16-Dec-2015 (CT) Change to `UI_Spec`
#    11-Oct-2016 (CT) Change `GTW.HTML` to `TFL.HTML`
#    ««revision-date»»···
#--

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _ReST                    import ReST
from   _TFL                     import TFL

import _CNDB._Base_Command_
import _CNDB._OMP.import_CNDB

import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._RST._MOM.Doc
import _GTW._RST._MOM.Scope
import _GTW._RST._TOP._MOM.Doc
import _GTW._RST._TOP.ReST

import _GTW._Werkzeug.Command

import _GTW._OMP._Auth.UI_Spec
import _GTW._OMP._PAP.UI_Spec

import _CNDB._JNJ
import _CNDB._OMP.UI_Spec
import _CNDB._OMP.RST_Api_addons

import _TFL.HTML
import _ReST.To_Html

from   _TFL                     import sos
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Re_Replacer
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property

import _TFL.CAO

from   _CNDB._GTW               import RST_addons

class _CNDB_Sub_Command_ (TFL.Command.Sub_Command) :

    _rn_prefix              = "_CNDB"

_Sub_Command_ = _CNDB_Sub_Command_ # end class

class CNDB_Command (CNDB._Base_Command_, GTW.Werkzeug.Command) :

    _rn_prefix              = "CNDB_"

    _opts                   = \
        ( "-auth_required:B=True?Is authorization required?"
        ,
        )
    _template_prefixes      = dict \
        ( CNDB              = sos.path.dirname (_CNDB._JNJ.__file__)
        )

    class _CNDB_Collect_Garbage_ (_Sub_Command_) :
        """Collect freed IP addresses out of cooldown"""

    _Collect_Garbage_ = _CNDB_Collect_Garbage_ # end class

    def _handle_collect_garbage (self, cmd) :
        scope = self._handle_load (cmd)
        for ipn in scope.CNDB.IP_Network.query (~MOM.Q.parent) :
            ipn.collect_garbage ()
    # end def _handle_collect_garbage

Command = CNDB_Command # end class

if __name__ != "__main__" :
    CNDB._Export ("*")
### __END__ CNDB.Command
