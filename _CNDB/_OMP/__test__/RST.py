# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.__test__.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CNDB.OMP.__test__.RST
#
# Purpose
#    Test RESTful api for CNDB
#
# Revision Dates
#     9-Jan-2013 (CT) Creation
#     1-Feb-2013 (RS) Fix rounding error with python2.6
#     5-Mar-2013 (CT) Adapt to changes in `Net_Interface_in_IP4_Network`
#    28-Mar-2013 (CT) Factor `_test_limit` from `_test_get`
#     3-May-2013 (CT) Add test for `META` query argument
#     8-May-2013 (CT) Remove `.pid`, `.url` from `attribute_names`, unless CSV
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    29-Jul-2013 (CT) Add `test_put`
#     4-Oct-2013 (CT) Add tests for query arguments `fields` and `add_fields`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    14-Jun-2014 (RS) Add `name` to `Net_Interface_in_IP_Network`, add
#                     `desc` to `Node`, `Node` no longer derived from `Subject`
#    20-Jun-2014 (RS) Re-add `IP_Network.pool`
#    23-Jun-2014 (RS) Make tests run after model changes
#     4-Jul-2014 (RS) Added `Id_Entity_permits_Group`
#    ««revision-date»»···
#--

from   _CNDB                      import CNDB
import _CNDB._OMP
from   _GTW.__test__.rst_harness  import *
from   _GTW.__test__              import rst_harness

import _CNDB._OMP.import_CNDB
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._RST._MOM.Client

import json

def run_server (db_url = "hps://", db_name = None) :
    return rst_harness.run_server ("_CNDB._OMP.__test__.RST", db_url, db_name)
# end def run_server

class CNDB_RST_Test_Command (GTW_RST_Test_Command) :

    ANS                     = CNDB

    def fixtures (self, scope) :
        from _CNDB._OMP.__test__.fixtures import create
        create (scope)
        PAP = scope.PAP
        nod = scope.CNDB.Node.query (name = "node2").one ()
        nod.address = PAP.Address \
            ( street  = 'Beispiel 23'
            , zip     = '1010'
            , city    = 'Wien'
            , country = 'Austria'
            )
    # end def fixtures

# end class CNDB_RST_Test_Command

Scaffold   = CNDB_RST_Test_Command ()

### «text» ### The doctest follows::

_test_get = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> CC = GTW.RST.MOM.Client.Requester (R.prefix, verify = False)
    >>> r = CC.get ("")
    >>> prepr (r._url)
    'http://localhost:9999/'

    >>> r = show (R.get ("/v1/CNDB-Node"))
    { 'json' :
        { 'entries' :
            [ '/v1/CNDB-Node/2'
            , '/v1/CNDB-Node/3'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node'
    }

    >>> r = show (R.get ("/v1/CNDB-Node?verbose&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'name'
            , 'manager'
            , 'address'
            , 'desc'
            , 'owner'
            , 'position.lat'
            , 'position.lon'
            , 'position.height'
            , 'show_in_map'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'manager' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'name' : 'nogps'
                  , 'owner' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'CNDB.Node'
              , 'url' : '/v1/CNDB-Node/2'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node?verbose&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Node?verbose&closure&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'name'
            , 'manager'
            , 'address'
            , 'desc'
            , 'owner'
            , 'position.lat'
            , 'position.lon'
            , 'position.height'
            , 'show_in_map'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'manager' :
                      { 'attributes' :
                          { 'first_name' : 'ralf'
                          , 'last_name' : 'schlatterbeck'
                          , 'middle_name' : ''
                          , 'title' : ''
                          }
                      , 'cid' : 1
                      , 'pid' : 1
                      , 'type_name' : 'PAP.Person'
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'name' : 'nogps'
                  , 'owner' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'CNDB.Node'
              , 'url' : '/v1/CNDB-Node/2'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node?verbose&closure&order_by=pid&limit=1'
    }


    >>> r = show (R.get ("/v1/CNDB-Net_Interface_in_IP4_Network?brief"))
    { 'json' :
        { 'entries' :
            [ 31
            , 32
            , 33
            , 34
            ]
        , 'url_template' : '/v1/CNDB-Net_Interface_in_IP4_Network/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Net_Interface_in_IP4_Network?brief'
    }

"""

_test_limit = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> r = show (R.get ("/v1/CNDB-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'right'
            , 'mask_len'
            , 'name'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'left' :
                                      { 'attributes' :
                                          { 'model_no' : ''
                                          , 'name' : 'generic'
                                          , 'revision' : ''
                                          }
                                      , 'cid' : 34
                                      , 'pid' : 27
                                      , 'type_name' : 'CNDB.Net_Device_Type'
                                      , 'url' : '/v1/CNDB-Net_Device_Type/27'
                                      }
                                  , 'name' : 'dev'
                                  , 'node' :
                                      { 'attributes' :
                                          { 'address' :
                                              { 'attributes' :
                                                  { 'city' : 'wien'
                                                  , 'country' : 'austria'
                                                  , 'street' : 'beispiel 23'
                                                  , 'zip' : '1010'
                                                  }
                                              , 'cid' : 42
                                              , 'pid' : 35
                                              , 'type_name' : 'PAP.Address'
                                              , 'url' : '/v1/PAP-Address/35'
                                              }
                                          , 'manager' :
                                              { 'attributes' :
                                                  { 'first_name' : 'ralf'
                                                  , 'last_name' : 'schlatterbeck'
                                                  , 'middle_name' : ''
                                                  , 'title' : ''
                                                  }
                                              , 'cid' : 1
                                              , 'pid' : 1
                                              , 'type_name' : 'PAP.Person'
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'name' : 'node2'
                                          , 'owner' :
                                              { 'pid' : 1
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'position' :
                                              { 'lat' : 48.25
                                              , 'lon' : 15.8744
                                              }
                                          }
                                      , 'cid' : 43
                                      , 'pid' : 3
                                      , 'type_name' : 'CNDB.Node'
                                      , 'url' : '/v1/CNDB-Node/3'
                                      }
                                  }
                              , 'cid' : 35
                              , 'pid' : 28
                              , 'type_name' : 'CNDB.Net_Device'
                              , 'url' : '/v1/CNDB-Net_Device/28'
                              }
                          , 'mac_address' : ''
                          , 'name' : 'wr'
                          }
                      , 'cid' : 36
                      , 'pid' : 29
                      , 'type_name' : 'CNDB.Wired_Interface'
                      , 'url' : '/v1/CNDB-Wired_Interface/29'
                      }
                  , 'mask_len' : 24
                  , 'name' : 'wr'
                  , 'right' :
                      { 'attributes' :
                          { 'net_address' : '192.168.23.1'
                          , 'pool' :
                              { 'attributes' :
                                  { 'net_address' : '192.168.23.0/24'
                                  , 'pool' :
                                      { 'pid' : 4
                                      , 'url' : '/v1/CNDB-IP4_Network/4'
                                      }
                                  }
                              , 'cid' : 4
                              , 'pid' : 4
                              , 'type_name' : 'CNDB.IP4_Network'
                              , 'url' : '/v1/CNDB-IP4_Network/4'
                              }
                          }
                      , 'cid' : 21
                      , 'pid' : 20
                      , 'type_name' : 'CNDB.IP4_Network'
                      , 'url' : '/v1/CNDB-IP4_Network/20'
                      }
                  }
              , 'cid' : 38
              , 'pid' : 31
              , 'type_name' : 'CNDB.Wired_Interface_in_IP4_Network'
              , 'url' : '/v1/CNDB-Net_Interface_in_IP4_Network/31'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1&META"), cleaner = date_cleaner)
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'right'
            , 'mask_len'
            , 'name'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'left' :
                                      { 'attributes' :
                                          { 'model_no' : ''
                                          , 'name' : 'generic'
                                          , 'revision' : ''
                                          }
                                      , 'cid' : 34
                                      , 'creation' : {'date' : <datetime>}
                                      , 'last_change' : {'date' : <datetime>}
                                      , 'pid' : 27
                                      , 'type_name' : 'CNDB.Net_Device_Type'
                                      , 'url' : '/v1/CNDB-Net_Device_Type/27'
                                      }
                                  , 'name' : 'dev'
                                  , 'node' :
                                      { 'attributes' :
                                          { 'address' :
                                              { 'attributes' :
                                                  { 'city' : 'wien'
                                                  , 'country' : 'austria'
                                                  , 'street' : 'beispiel 23'
                                                  , 'zip' : '1010'
                                                  }
                                              , 'cid' : 42
                                              , 'creation' : {'date' : <datetime>}
                                              , 'last_change' : {'date' : <datetime>}
                                              , 'pid' : 35
                                              , 'type_name' : 'PAP.Address'
                                              , 'url' : '/v1/PAP-Address/35'
                                              }
                                          , 'manager' :
                                              { 'attributes' :
                                                  { 'first_name' : 'ralf'
                                                  , 'last_name' : 'schlatterbeck'
                                                  , 'middle_name' : ''
                                                  , 'title' : ''
                                                  }
                                              , 'cid' : 1
                                              , 'creation' : {'date' : <datetime>}
                                              , 'last_change' : {'date' : <datetime>}
                                              , 'pid' : 1
                                              , 'type_name' : 'PAP.Person'
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'name' : 'node2'
                                          , 'owner' :
                                              { 'pid' : 1
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'position' :
                                              { 'lat' : 48.25
                                              , 'lon' : 15.8744
                                              }
                                          }
                                      , 'cid' : 43
                                      , 'creation' : {'date' : <datetime>}
                                      , 'last_change' : {'date' : <datetime>}
                                      , 'pid' : 3
                                      , 'type_name' : 'CNDB.Node'
                                      , 'url' : '/v1/CNDB-Node/3'
                                      }
                                  }
                              , 'cid' : 35
                              , 'creation' : {'date' : <datetime>}
                              , 'last_change' : {'date' : <datetime>}
                              , 'pid' : 28
                              , 'type_name' : 'CNDB.Net_Device'
                              , 'url' : '/v1/CNDB-Net_Device/28'
                              }
                          , 'mac_address' : ''
                          , 'name' : 'wr'
                          }
                      , 'cid' : 36
                      , 'creation' : {'date' : <datetime>}
                      , 'last_change' : {'date' : <datetime>}
                      , 'pid' : 29
                      , 'type_name' : 'CNDB.Wired_Interface'
                      , 'url' : '/v1/CNDB-Wired_Interface/29'
                      }
                  , 'mask_len' : 24
                  , 'name' : 'wr'
                  , 'right' :
                      { 'attributes' :
                          { 'net_address' : '192.168.23.1'
                          , 'pool' :
                              { 'attributes' :
                                  { 'net_address' : '192.168.23.0/24'
                                  , 'pool' :
                                      { 'pid' : 4
                                      , 'url' : '/v1/CNDB-IP4_Network/4'
                                      }
                                  }
                              , 'cid' : 4
                              , 'creation' : {'date' : <datetime>}
                              , 'last_change' : {'date' : <datetime>}
                              , 'pid' : 4
                              , 'type_name' : 'CNDB.IP4_Network'
                              , 'url' : '/v1/CNDB-IP4_Network/4'
                              }
                          }
                      , 'cid' : 21
                      , 'creation' : {'date' : <datetime>}
                      , 'last_change' : {'date' : <datetime>}
                      , 'pid' : 20
                      , 'type_name' : 'CNDB.IP4_Network'
                      , 'url' : '/v1/CNDB-IP4_Network/20'
                      }
                  }
              , 'cid' : 38
              , 'creation' : {'date' : <datetime>}
              , 'last_change' : {'date' : <datetime>}
              , 'pid' : 31
              , 'type_name' : 'CNDB.Wired_Interface_in_IP4_Network'
              , 'url' : '/v1/CNDB-Net_Interface_in_IP4_Network/31'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1&META'
    }

    >>> r = show (R.get ("/v1/CNDB-Wired_Interface/29?verbose&order_by=pid&limit=1"), cleaner = date_cleaner)
    { 'json' :
        { 'attributes' :
            { 'left' :
                { 'pid' : 28
                , 'url' : '/v1/CNDB-Net_Device/28'
                }
            , 'mac_address' : ''
            , 'name' : 'wr'
            }
        , 'cid' : 36
        , 'pid' : 29
        , 'rels' :
            [ '/v1/CNDB-Wired_Interface/29/documents'
            , '/v1/CNDB-Wired_Interface/29/group_links'
            , '/v1/CNDB-Wired_Interface/29/ip4_network_links'
            , '/v1/CNDB-Wired_Interface/29/ip6_network_links'
            , '/v1/CNDB-Wired_Interface/29/left_net_links'
            , '/v1/CNDB-Wired_Interface/29/right_net_links'
            ]
        , 'type_name' : 'CNDB.Wired_Interface'
        , 'url' : '/v1/CNDB-Wired_Interface/29'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Wired_Interface/29?verbose&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Wired_Interface/29?verbose&fields=name&order_by=pid&limit=1"), cleaner = date_cleaner)
    { 'json' :
        { 'attributes' : {'name' : 'wr'}
        , 'cid' : 36
        , 'pid' : 29
        , 'rels' :
            [ '/v1/CNDB-Wired_Interface/29/documents'
            , '/v1/CNDB-Wired_Interface/29/group_links'
            , '/v1/CNDB-Wired_Interface/29/ip4_network_links'
            , '/v1/CNDB-Wired_Interface/29/ip6_network_links'
            , '/v1/CNDB-Wired_Interface/29/left_net_links'
            , '/v1/CNDB-Wired_Interface/29/right_net_links'
            ]
        , 'type_name' : 'CNDB.Wired_Interface'
        , 'url' : '/v1/CNDB-Wired_Interface/29'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Wired_Interface/29?verbose&fields=name&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Wired_Interface/29?verbose&fields=left,name&order_by=pid&limit=1"), cleaner = date_cleaner)
    { 'json' :
        { 'attributes' :
            { 'left' :
                { 'pid' : 28
                , 'url' : '/v1/CNDB-Net_Device/28'
                }
            , 'name' : 'wr'
            }
        , 'cid' : 36
        , 'pid' : 29
        , 'rels' :
            [ '/v1/CNDB-Wired_Interface/29/documents'
            , '/v1/CNDB-Wired_Interface/29/group_links'
            , '/v1/CNDB-Wired_Interface/29/ip4_network_links'
            , '/v1/CNDB-Wired_Interface/29/ip6_network_links'
            , '/v1/CNDB-Wired_Interface/29/left_net_links'
            , '/v1/CNDB-Wired_Interface/29/right_net_links'
            ]
        , 'type_name' : 'CNDB.Wired_Interface'
        , 'url' : '/v1/CNDB-Wired_Interface/29'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Wired_Interface/29?verbose&fields=left,name&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Wired_Interface/29?verbose&add_fields=my_node&order_by=pid&limit=1"), cleaner = date_cleaner)
    { 'json' :
        { 'attributes' :
            { 'left' :
                { 'pid' : 28
                , 'url' : '/v1/CNDB-Net_Device/28'
                }
            , 'mac_address' : ''
            , 'my_node' :
                { 'pid' : 3
                , 'url' : '/v1/CNDB-Node/3'
                }
            , 'name' : 'wr'
            }
        , 'cid' : 36
        , 'pid' : 29
        , 'rels' :
            [ '/v1/CNDB-Wired_Interface/29/documents'
            , '/v1/CNDB-Wired_Interface/29/group_links'
            , '/v1/CNDB-Wired_Interface/29/ip4_network_links'
            , '/v1/CNDB-Wired_Interface/29/ip6_network_links'
            , '/v1/CNDB-Wired_Interface/29/left_net_links'
            , '/v1/CNDB-Wired_Interface/29/right_net_links'
            ]
        , 'type_name' : 'CNDB.Wired_Interface'
        , 'url' : '/v1/CNDB-Wired_Interface/29'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Wired_Interface/29?verbose&add_fields=my_node&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/CNDB-Wired_Interface?verbose&add_fields=my_node&order_by=pid&limit=1"), cleaner = date_cleaner)
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'mac_address'
            , 'name'
            , 'is_active'
            , 'desc'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'left' :
                      { 'pid' : 28
                      , 'url' : '/v1/CNDB-Net_Device/28'
                      }
                  , 'mac_address' : ''
                  , 'my_node' :
                      { 'pid' : 3
                      , 'url' : '/v1/CNDB-Node/3'
                      }
                  , 'name' : 'wr'
                  }
              , 'cid' : 36
              , 'pid' : 29
              , 'type_name' : 'CNDB.Wired_Interface'
              , 'url' : '/v1/CNDB-Wired_Interface/29'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Wired_Interface?verbose&add_fields=my_node&order_by=pid&limit=1'
    }

"""

def show_by_pid (ETM) :
    for x in ETM.query ().order_by (Q.pid) :
        print ("%-3s : %s" % (x.pid, x.ui_display))
# end def show_by_pid

_test_local_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> CNDB = scope.CNDB
    >>> PAP = scope.PAP

    >>> show_by_pid (scope.CNDB.Node)
    2   : nogps
    3   : node2

    >>> show_by_pid (scope.CNDB.Net_Device)
    28  : Generic, node2, dev

    >>> show_by_pid (scope.CNDB.Net_Interface)
    29  : Generic, node2, dev, wr
    30  : Generic, node2, dev, wl

    >>> show_by_pid (scope.CNDB.Net_Interface_in_IP4_Network)
    31  : Generic, node2, dev, wr, 192.168.23.1
    32  : Generic, node2, dev, wl, 192.168.23.2
    33  : Generic, node2, dev, wr, 192.168.23.3
    34  : Generic, node2, dev, wl, 192.168.23.4

    >>> show_by_pid (scope.CNDB.IP4_Network)
    4   : 192.168.23.0/24
    5   : 192.168.23.0/25
    6   : 192.168.23.128/25
    7   : 192.168.23.0/26
    8   : 192.168.23.64/26
    9   : 192.168.23.0/27
    10  : 192.168.23.32/27
    11  : 192.168.23.0/28
    12  : 192.168.23.16/28
    13  : 192.168.23.0/29
    14  : 192.168.23.8/29
    15  : 192.168.23.0/30
    16  : 192.168.23.4/30
    17  : 192.168.23.0/31
    18  : 192.168.23.2/31
    19  : 192.168.23.0
    20  : 192.168.23.1
    21  : 192.168.23.2
    22  : 192.168.23.3
    23  : 192.168.23.4/31
    24  : 192.168.23.6/31
    25  : 192.168.23.4
    26  : 192.168.23.5

    >>> for i in range (1, 36) :
    ...     x = scope.pid_query (i)
    ...     print ("%%-3s %%s" %% (i, x.ui_display if x is not None else x))
    1   Schlatterbeck Ralf
    2   nogps
    3   node2
    4   192.168.23.0/24
    5   192.168.23.0/25
    6   192.168.23.128/25
    7   192.168.23.0/26
    8   192.168.23.64/26
    9   192.168.23.0/27
    10  192.168.23.32/27
    11  192.168.23.0/28
    12  192.168.23.16/28
    13  192.168.23.0/29
    14  192.168.23.8/29
    15  192.168.23.0/30
    16  192.168.23.4/30
    17  192.168.23.0/31
    18  192.168.23.2/31
    19  192.168.23.0
    20  192.168.23.1
    21  192.168.23.2
    22  192.168.23.3
    23  192.168.23.4/31
    24  192.168.23.6/31
    25  192.168.23.4
    26  192.168.23.5
    27  Generic
    28  Generic, node2, dev
    29  Generic, node2, dev, wr
    30  Generic, node2, dev, wl
    31  Generic, node2, dev, wr, 192.168.23.1
    32  Generic, node2, dev, wl, 192.168.23.2
    33  Generic, node2, dev, wr, 192.168.23.3
    34  Generic, node2, dev, wl, 192.168.23.4
    35  Beispiel 23, 1010, Wien, Austria

"""

_test_put = r"""
    >>> server  = run_server (%(p1)s, %(n1)s)
    >>> headers = { "Content-Type": "application/json" }

    >>> r = show (R.get ("/v1/CNDB-Node/2?raw"))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            , 'name' : 'nogps'
            , 'owner' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            }
        , 'cid' : 2
        , 'pid' : 2
        , 'rels' :
            [ '/v1/CNDB-Node/2/documents'
            , '/v1/CNDB-Node/2/group_links'
            ]
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2?raw'
    }

    >>> rj = req_json (r)
    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = rj ["attributes_raw"]
    ...     , cid            = rj ["cid"]
    ...     )
    ... )
    >>> ru = requests.utils.urlparse (r.url)
    >>> p  = "%%s://%%s%%s" %% (ru.scheme, ru.netloc, req_json (r) ["url"])
    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            , 'name' : 'nogps'
            , 'owner' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            }
        , 'cid' : 44
        , 'pid' : 2
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2'
    }

    >>> r = show (R.get ("/v1/CNDB-Node/2?raw&brief"))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' : 1
            , 'name' : 'nogps'
            , 'owner' : 1
            }
        , 'cid' : 44
        , 'pid' : 2
        , 'rels' :
            [ '/v1/CNDB-Node/2/documents'
            , '/v1/CNDB-Node/2/group_links'
            ]
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2?raw&brief'
    }

    >>> rj = req_json (r)
    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = rj ["attributes_raw"]
    ...     , cid            = rj ["cid"]
    ...     )
    ... )
    >>> ru = requests.utils.urlparse (r.url)
    >>> p  = "%%s://%%s%%s" %% (ru.scheme, ru.netloc, req_json (r) ["url"])
    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            , 'name' : 'nogps'
            , 'owner' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            }
        , 'cid' : 45
        , 'pid' : 2
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2'
    }

    >>> snoopy_cargo = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict
    ...         ( last_name   = "Dog"
    ...         , first_name  = "Snoopy"
    ...         , middle_name = "the"
    ...         , lifetime    = dict (start = "20001122")
    ...         )
    ...     )
    ... )
    >>> t = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'first_name' : 'Snoopy'
            , 'last_name' : 'Dog'
            , 'lifetime' : {'start' : '2000-11-22'}
            , 'middle_name' : 'The'
            , 'title' : ''
            }
        , 'cid' : 46
        , 'pid' : 36
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/36'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> sj = req_json (s)
    >>> tj = req_json (t)
    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict (sj ["attributes_raw"], manager = tj ["pid"])
    ...     , cid            = sj ["cid"]
    ...     )
    ... )
    >>> s3 = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' :
                { 'pid' : 36
                , 'url' : '/v1/PAP-Person/36'
                }
            , 'name' : 'nogps'
            , 'owner' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            }
        , 'cid' : 47
        , 'pid' : 2
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2'
    }

    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict (sj ["attributes_raw"], manager = 1, owner = 36)
    ...     , cid            = sj ["cid"]
    ...     )
    ... )
    >>> s4 = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' : {'error' : 'Cid mismatch: requested cid = 45, current cid = 47'}
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2'
    }

    >>> sj3 = req_json (s3)
    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes_raw = dict (name = "wrzlbrmft", manager = 1, owner = 36)
    ...     , cid            = sj3 ["cid"]
    ...     )
    ... )
    >>> s5 = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes_raw' :
            { 'manager' :
                { 'pid' : 1
                , 'url' : '/v1/PAP-Person/1'
                }
            , 'name' : 'wrzlbrmft'
            , 'owner' :
                { 'pid' : 36
                , 'url' : '/v1/PAP-Person/36'
                }
            }
        , 'cid' : 48
        , 'pid' : 2
        , 'type_name' : 'CNDB.Node'
        , 'url' : '/v1/CNDB-Node/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/CNDB-Node/2'
    }

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_get         = _test_get
        , test_limit       = _test_limit
        , test_local_query = _test_local_query
        , test_put         = _test_put
        )
    )

if __name__ == "__main__" :
    rst_harness._main (Scaffold)
### __END__ CNDB.OMP.__test__.RST
