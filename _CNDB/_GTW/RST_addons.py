# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    RST_addons
#
# Purpose
#    Addons for GTW.RST...
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#     7-Dec-2012 (CT) Continue creation
#    14-Dec-2012 (CT) Factor `Is_Owner_or_Manager`, set `child_permission_map`
#    14-Dec-2012 (CT) Factor `GTW.RST.TOP.MOM.Admin_Restricted`
#    14-Dec-2012 (CT) Factor `User_Entity`
#    17-Dec-2012 (CT) Add `User_Node_Dependent` and descendents
#    24-Apr-2013 (CT) Fix `Is_Owner_or_Manager.predicate`
#    25-Apr-2013 (CT) Add `eligible_objects`, `child_postconditions_map`,
#                     `_pre_commit_entity_check`
#    25-Apr-2013 (CT) Add `eligible_object_restriction`
#    28-Apr-2013 (CT) DRY `User_Node.form_parameters`
#    28-Apr-2013 (CT) Add `Login_has_Person`
#    30-Apr-2013 (CT) Add `Node_Manager_Error`, `_pre_commit_node_check`
#    30-Apr-2013 (CT) Remove `prefilled` from `User_Node.form_parameters` for
#                     `manager`
#     7-Oct-2013 (CT) Simplify `Is_Owner_or_Manager.predicate`
#                     * `belongs_to_node` works now
#                     * remove redefinitions of `query_filters_restricted`
#     7-Oct-2013 (CT) Add `User_Antenna`
#    10-Apr-2014 (CT) Add `Dashboard`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    14-Apr-2014 (CT) Add `devices`, `interfaces` to `Dashboard`;
#                     add `User_Net_Interface`
#    17-Apr-2014 (CT) Add `Dashboard` divisions
#    18-Apr-2014 (CT) Add `person`, `address`, ..., to `Dashboard`
#    18-Apr-2014 (CT) Change `query_filters_restricted` to use `my_person`
#    19-Apr-2014 (CT) Add `_get_child` for `<div_name>`,
#                     `__getattr__` for `db_*`
#    26-Apr-2014 (CT) Add first draft of `_DB_E_Type_.GET` to render `MF3.Form`
#     2-May-2014 (CT) Remove `graphs` from `DB_Device.view_action_names`
#     2-May-2014 (CT) Put `name` in front of `view_field_names` of
#                     `DB_Device` and `DB_Interface`
#     2-May-2014 (CT) Add `skip` for `lifetime` to `DB_Node.form_attr_spec`
#     3-May-2014 (CT) Add and use `_setup_create_form_attr_spec`,
#                     redefine it for `DB_Device` and `DB_Interface`
#     4-May-2014 (CT) Redefine `DB_Interface.Creator` and `.Instance` to do
#                     IP allocation (very hackish for now)
#     4-May-2014 (CT) Add `DB_Interface.xtra_template_macro`
#     5-May-2014 (CT) Add `DB_Node.position`
#    17-Jun-2014 (CT) Add `DB_Person.Form_spec` to test `include_rev_refs`
#    20-Aug-2014 (CT) Adapt to changes of `GTW.RST.TOP.MOM.Admin`
#    29-Aug-2014 (CT) Adapt to changes of `GTW.RST.TOP.MOM.Admin`, again
#     1-Sep-2014 (CT) Add property `_DB_E_Type_.eligible_objects`,
#                     fix property `_DB_E_Type_.child_postconditions_map`
#     2-Sep-2014 (MB) Remove "graphs" action from node
#                     Remove "firmware" action from device
#     2-Sep-2014 (CT) Remove `_setup_create_mf3_attr_spec`
#                     (done by GTW.RST.TOP.MOM.Admin._Changer_, now)
#     3-Sep-2014 (CT) Add properties `_DB_E_Type_.query_filters_restricted`
#                     and `.user_restriction`
#     3-Sep-2014 (CT) Add `restrict_completion` for `DB_Device`, `DB_Interface`
#     3-Sep-2014 (MB) Add owner field to db_node
#     3-Sep-2014 (CT) Add `_get_dash`, `_DB_ETN_map`
#     3-Sep-2014 (CT) Move `_get_child` from `_DB_Div_Base_` to `_DB_Base_`
#     3-Sep-2014 (CT) Add `children_np` for partial `_DB_E_Type_` instances
#     3-Sep-2014 (CT) Add `DB_Wired_Interface`, `DB_Wireless_Interface`
#     5-Sep-2014 (CT) Add `User_Net_Interface_in_IP_Network`
#     5-Sep-2014 (CT) Add `DB_Interface_in_IP_Network`
#     5-Sep-2014 (CT) Remove fake IP allocation
#     5-Sep-2014 (CT) Add `tr_instance_css_class` to
#                     `DB_Interface_in_IP_Network`
#     5-Sep-2014 (CT) Add action `allocate_ip`, factor `create_action_name`
#                     add `_DB_E_Type_` property `is_partial`
#    12-Sep-2014 (CT) Add `PAP.Person_in_Group` to
#                     `User_Node.change_query_filters`
#    12-Sep-2014 (CT) Fix `User_Entity.query_filters_restricted`
#    12-Sep-2014 (CT) Add `User_Person.query_filters_restricted`,
#                     `_User_Person_has_Property_.query_filters_restricted`
#    13-Sep-2014 (CT) Change `change_query_filters` to `change_query_types`
#    16-Sep-2014 (CT) Change `msg` of action to dict-interpolation
#    16-Sep-2014 (CT) Add `_Field_Interface_`,
#                     augment `DB_Interface_in_IP_Network.view_field_names`
#    16-Sep-2014 (CT) Add `DB_Interface_in_IP_Network.Allocate_IP`,
#                     `DB_Interface_in_IP_Network._get_child`
#    24-Sep-2014 (CT) Add `_Action_Override_.set_request_defaults`
#    26-Sep-2014 (CT) Remove action `edit` from `_DB_Person_Property_`
#    26-Sep-2014 (CT) Set `DB_Account.ui_allow_new` to `False`
#    30-Sep-2014 (CT) Change `Allocate_IP` to use `can_allocate`
#     3-Dec-2014 (CT) Adapt to changes in grid of pure-0.5.0
#    16-Jan-2015 (CT) Add property `_DB_E_Type_.button_types`
#    20-Jan-2015 (CT) Factor `_Permission_.Login_has_Person`, `._get_obj`
#    21-Jan-2015 (CT) Add `__getattr__`, `_admin_delegates`, DRY properties
#    27-Jan-2015 (CT) Adapt to changes of `GTW.RST.TOP.MOM.Field`,
#                     DRY field-handling code
#                     * Factor `_Field_Owner_` from home-grown code in
#                       template `html/app.m.jnj`
#    27-Jan-2015 (CT) Add `_admin_func_delegates`
#     6-Apr-2015 (CT) Use `id_entity_select` for `Wireless_Interface.standard`
#     6-Apr-2015 (CT) Use `id_entity_select` for `DB_Device.left`
#     7-Apr-2015 (CT) Add `_DB_Base_.__getitem__`, `._db_etn_map`
#     7-Apr-2015 (CT) Add `Div_Name_T`
#     7-Apr-2015 (CT) Use literal `Div_Name_T` for `DB_Interface_in_IP_Network`
#     8-Jun-2015 (CT) Add `Is_Deleter`, `Undo`, `_DB_E_Type_CNDB_`,
#                     and `_DB_E_Type_CNDB_.child_permission_map`
#     8-Jun-2015 (CT) Add `DB_Node.child_postconditions_map`,
#                     fix `Node_Manager_Error`
#    12-Jun-2015 (CT) Add action `change_email`, remove action `reset_password`
#    24-Jun-2015 (CT) Derive `DB_Wire{d,less}_Interface` from `DB_Interface`,
#                     not `_DB_Interface_`
#    24-Jun-2015 (CT) Add `zero_width_space` to `as_html` (_Field_IP_Address_,
#                     _Field_IP_Addresses_, _Field_IP_Network_)
#    26-Jun-2015 (CT) Add `nested_db_type`, `nested_obj_Q`, `nested_objects`
#    26-Jun-2015 (CT) Change `_Field_Owner_` to `_Field_Role_`
#     1-Jul-2015 (CT) Remove names from `view_field_names`
#     2-Jul-2015 (CT) Add `icon_html`, `icon_name`
#     2-Jul-2015 (CT) Remove `filter` from `_DB_E_Type_.view_action_names`
#     3-Jul-2015 (CT) Redefine `add_css_classes`, `description` for
#                     `_Field_IP_Address_`, `_Field_IP_Network_`
#     3-Jul-2015 (CT) Redefine `description` for `_Field_Role_`
#     3-Jul-2015 (CT) Change `Allocate_IP.POST` to use `e_type_tree_li`, not
#                     `e_type_object`, macro
#     6-Jul-2015 (CT) Redefine `Instance.rendered` to handle `?expand_tree`
#     6-Jul-2015 (CT) Add `DB_View.render_context` to setup `expand_trees`
#     7-Jul-2015 (CT) Add `net_device_type` to `DB_Device.view_field_names`
#     8-Jul-2015 (CT) Remove `filter` from `_action_map`
#    18-Nov-2015 (CT) Pass `abs_href_dynamic`, not `abs_href`, to `pp_join`
#    16-Dec-2015 (CT) Fix ETM-splitting in `User_Entity.__init__`
#    16-Dec-2015 (CT) Use `E_Type.UI_Spec`
#    10-Jun-2016 (CT) Change `_DB_E_Type_.POST` to use `_rendered_post_esf_form`
#    ««revision-date»»···
#--

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

import _CNDB._GTW
import _CNDB._OMP.import_CNDB

from   _GTW._MF3                import Element as MF3
from   _GTW._RST.Permission     import Login_has_Person

import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM
import _GTW._RST._TOP._MOM.Admin_Restricted

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Property      import Alias_Property
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe, Add_New_Method, Decorator
from   _TFL.Dingbats            import zero_width_space
from   _TFL.formatted_repr      import formatted_repr as formatted
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join
from   _TFL.Record              import Record
from   _TFL.update_combined     import update_combined

from   itertools                import chain as ichain
from   posixpath                import join  as pp_join

class Node_Manager_Error (MOM.Error._Invariant_, TypeError) :
    """You are not allowed to change owner or manager unless after the change
       you are still either owner or manager
    """

    class inv :
        name       = "Node_Manager_Error"

    def __init__ (self, obj, changed, user) :
        self.__super.__init__ (obj)
        self.obj          = obj
        self.changed      = tuple \
            ((c, getattr (obj.E_Type, c).ui_name_T) for c in changed)
        self.user         = user
        self.attributes   = ("manager", "owner")
        self.values = vs  = tuple \
            (  (v.ui_display if v is not None else v)
            for v in (getattr (obj, k) for k in self.attributes)
            )
        self.args         = (obj, changed, vs, user)
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        bindings = dict (self.bindings)
        result = \
            ( _T( "You are not allowed to change %s unless afterwards "
                  "you [%s] are still either manager or owner"
                )
            % ( _T (" and ").join
                  ( "'%s' %s '%s'"
                  % (d, _T ("to"), bindings [k]) for k, d in self.changed
                  )
              , self.user
              )
            )
        return result
    # end def as_unicode

    @property
    def bindings (self) :
        return zip (self.attributes, self.values)
    # end def bindings

    @property
    def head (self) :
        return self.as_unicode
    # end def head

# end class Node_Manager_Error

class Is_Deleter (GTW.RST._Permission_) :
    """Permission if user is the deleter of the object"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            try :
                scope    = page.scope
                r_data   = page.request.req_data
                change   = scope.query_changes \
                    (cid = r_data ["cid"], pid = r_data ["pid"]).one ()
                c_user   = scope.pid_query (change.user) \
                    if isinstance (change.user, pyk.int_types) else change.user
                return c_user is user
            except Exception as exc :
                logging.exception \
                    ( "Exception for permission Is_Deleter: "
                      "user = %s, page = %s, request-data =\n     %s"
                    , user, page.abs_href, formatted (r_data)
                    )
    # end def predicate

# end class Is_Deleter

class Is_Owner_or_Manager (GTW.RST._Permission_) :
    """Permission if user is the owner or manager of the object"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            obj = self._get_obj (page, kw)
            if obj is not None :
                try :
                    qf = page.query_filters_restricted ()
                except AttributeError :
                    pass
                else :
                    if qf is not None :
                        return qf (obj)
    # end def predicate

# end class Is_Owner_or_Manager

@Add_New_Method (CNDB.OMP.Net_Device, CNDB.OMP.Wired_Interface, CNDB.OMP.Wireless_Interface)
def _CNDB_User_Entity_PRC (self, resource, request, response, attribute_changes) :
    for eia in self.id_entity_attr :
        if eia.name in attribute_changes or eia.is_primary :
            ET = eia.E_Type
            eligible = resource.eligible_objects (ET.type_name)
            if eligible is not None :
                ent = getattr (self, eia.name)
                if ent not in eligible :
                    err = MOM.Error.Permission (self, eia, ent, eligible)
                    self.add_error (err)
                    raise err
# end def _CNDB_User_Entity_PRC

_pre_commit_entity_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_CNDB_User_Entity_PRC")

@Add_New_Method (CNDB.OMP.Node)
def _CNDB_Node_PRC (self, resource, request, response, attribute_changes) :
    changed = tuple (k for k in ("manager", "owner") if k in attribute_changes)
    if changed :
        user = resource.user_restriction
        if not (self.manager is user or self.owner is user) :
            err = Node_Manager_Error (self, changed, user.ui_display)
            self.add_error (err)
            raise err
# end def _CNDB_Node_PRC

_pre_commit_node_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_CNDB_Node_PRC")

_Ancestor = GTW.RST.TOP.MOM.Admin_Restricted.E_Type

class User_Entity (_Ancestor) :
    """Directory displaying instances of one E_Type owned or managed by """
    """the current user."""

    child_permission_map      = dict \
        ( change              = Is_Owner_or_Manager
        , delete              = Is_Owner_or_Manager
        , undo                = Is_Deleter
        )
    child_postconditions_map  = dict \
        ( create              = (_pre_commit_entity_check, )
        , change              = (_pre_commit_entity_check, )
        )
    et_map_name               = "admin_omu"
    restriction_desc          = _ ("owned/managed by")

    def __init__ (self, ** kw) :
        app_type = self.top.App_Type
        ETM      = kw.pop ("ETM", None) or self._ETM
        E_Type   = app_type.entity_type (ETM)
        xkw      = dict (E_Type.UI_Spec, ETM = ETM, ** kw)
        self.__super.__init__ (** xkw)
    # end def __init__

    @property
    @getattr_safe
    def user_restriction (self) :
        user = self.top.user
        return user.person if user else None
    # end def user_restriction

    def eligible_objects (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.objects
    # end def eligible_objects

    def eligible_object_restriction (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.query_filters_restricted ()
    # end def eligible_object_restriction

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            result = Q.OR \
                ( Q.my_person == person
                , Q.my_group.members == person
                )
            return result
    # end def query_filters_restricted

# end class User_Entity

class User_Node (User_Entity) :
    """Directory displaying the node instances belonging to the current user."""

    _ETM                  = "CNDB.Node"

    child_postconditions_map  = dict \
        ( User_Entity.child_postconditions_map
        , change = (_pre_commit_node_check, _pre_commit_entity_check)
        )

    @Once_Property
    @getattr_safe
    def change_query_types (self) :
        scope  = self.scope
        PiG    = scope.entity_type ("PAP.Person_in_Group")
        result = set  (self.__super.change_query_types)
        result.update (self._change_query_types (PiG))
        return result
    # end def change_query_types

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = self.__super.mf3_attr_spec_d
        u = self.user_restriction
        if u is not None :
            result = update_combined \
                ( result
                , dict
                    ( manager = dict (default = u)
                    )
                )
        return result
    # end def mf3_attr_spec_d

# end class User_Node

class User_Node_Dependent (User_Entity) :
    """Temporary until query attributes with chained Q expressions work"""

    ET_depends            = "CNDB.Node" ### E_Type we depend on

    @Once_Property
    @getattr_safe
    def change_query_types (self) :
        result = set (self.__super.change_query_types)
        ETd    = getattr \
            (self.top.ET_Map [self.ET_depends], self.et_map_name, None)
        if ETd is not None :
            result.update (ETd.change_query_types)
        return result
    # end def change_query_types

# end class User_Node_Dependent

class User_Antenna (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface_uses_Antenna"
    _ETM                  = "CNDB.Antenna"

# end class User_Antenna

class User_Net_Device (User_Node_Dependent) :

    _ETM                  = "CNDB.Net_Device"

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = self.__super.mf3_attr_spec_d
        u = self.top.user
        if u :
            u = u.person
            if u :
                result = update_combined \
                    ( result
                    , { "node.manager" : dict
                          ( default     = u
                          , prefilled   = True
                          )
                      }
                    )
        return result
    # end def mf3_attr_spec_d

# end class User_Net_Device

class User_Net_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Net_Interface"

# end class User_Net_Interface

class User_Net_Interface_in_IP_Network (User_Node_Dependent) :

    _ETM                  = "CNDB.Net_Interface_in_IP_Network"

# end class User_Net_Interface

class User_Person (User_Entity) :

    _ETM                  = "PAP.Person"

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            result = Q.pid == person.pid
            return result
    # end def query_filters_restricted

# end class User_Person

class _User_Person_has_Property_ (User_Entity) :

    ET_depends            = "PAP.Person"

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            result = Q.left == person
            return result
    # end def query_filters_restricted

# end class _User_Person_has_Property_

class User_Person_has_Account (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Account"

# end class User_Person_has_Account

class User_Person_has_Address (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Address"

# end class User_Person_has_Address

class User_Person_has_Email (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Email"

# end class User_Person_has_Email

class User_Person_has_IM_Handle (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_IM_Handle"

# end class User_Person_has_IM_Handle

class User_Person_has_Phone (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Phone"

# end class User_Person_has_Phone

class User_Wired_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Wired_Interface"

# end class User_Wired_Interface

class User_Wireless_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Wireless_Interface"

# end class User_Wireless_Interface

class User_Virtual_Wireless_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Virtual_Wireless_Interface"

# end class User_Virtual_Wireless_Interface

class User_Wireless_Interface_uses_Antenna (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface"
    _ETM                  = "CNDB.Wireless_Interface_uses_Antenna"

# end class User_Wireless_Interface_uses_Antenna

class User_Wireless_Interface_uses_Wireless_Channel (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface"
    _ETM                  = "CNDB.Wireless_Interface_uses_Wireless_Channel"

# end class User_Wireless_Interface_uses_Wireless_Channel

##### Dashboard ###############################################################

_Ancestor = GTW.RST.TOP.Dir

class _Meta_DB_Div_ (_Ancestor.__class__) :
    """Meta class of _DB_Div_"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name.startswith ("DB_") :
            cls.Div_Name   = name [3:]
            cls.div_name   = dn = cls.Div_Name.lower ()
            cls.app_div_id = cls.app_div_prefix + dn
            cls._entry_type_names = set \
                (et.type_name for et in cls._entry_types if et.type_name)
            if cls.type_name :
                cls._DB_ETN_map [cls.type_name]  = cls
            setattr (cls, "fill_%s" % dn, True)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        name   = cls.__name__
        if name.startswith ("DB_") :
            cls._db_name_map [name.lower ()] = result
            if result.type_name :
                dnm = result.parent._div_name_map
                dnm [result.div_name] = dnm [result.Div_Name] = result
                cls._db_etn_map [result.type_name] = result
        return result
    # end def __call__

# end class _Meta_DB_Div_

class _DB_Base_ (_Ancestor, metaclass = _Meta_DB_Div_) :
    """Base class of dashboard classes"""

    app_div_class         = "pure-u-1"
    app_div_prefix        = "app-D:"
    app_typ_prefix        = "app-T:"
    skip_etag             = True
    type_name             = None
    _DB_ETN_map           = {}
    _db_etn_map           = {}
    _DB_icon_map          = {}
    _DB_icon_name         = None
    _db_name_map          = {}
    _entry_types          = ()
    _exclude_robots       = True

    def __init__ (self, ** kw) :
        self.__super.__init__ (** self._init_kw (** kw))
    # end def __init__

    @property
    @getattr_safe
    def entries (self) :
        result = self._entries
        if not result :
            entries = tuple  (T (parent = self) for T in self._entry_types)
            self.add_entries (* entries)
        return self._entries
    # end def entries

    def icon_html (self, o) :
        name = self.icon_name (o)
        if name :
            return """<i class="fa fa-%s fa-fw"></i>""" % (name, )
    # end def icon_html

    def icon_name (self, o) :
        tn = o.type_name
        db = self._DB_ETN_map.get (tn)
        if db is not None :
            return db._DB_icon_name
        else :
            return self._DB_icon_map.get (tn)
    # end def icon_name

    def tr_instance_css_class (self, o) :
        return "%s-%d-" % (self.div_name, o.pid)
    # end def tr_instance_css_class

    def _get_child (self, child, * grandchildren) :
        self._populate_db_entries ()
        result = self.__super._get_child (child, * grandchildren)
        if result is None and child in self._div_name_map :
            result = self._div_name_map [child]
            if grandchildren :
                result = result._get_child (* grandchildren)
        return result
    # end def _get_child

    def _get_dash (self, tn) :
        et     = self.top.ET_Map [tn]
        result = getattr (et, _DB_E_Type_.et_map_name, None)
        if result is None :
            RT = self._DB_ETN_map.get (tn)
            if RT is not None :
                result = RT (parent = self)
        return result
    # end def _get_dash

    def _get_omu_admin (self, tn) :
        et     = self.top.ET_Map [tn]
        result = getattr (et, User_Entity.et_map_name, None)
        return result
    # end def _get_omu_admin

    def _init_kw (self, ** kw) :
        dkw = dict \
            ( name            = self.div_name
            , short_title     = self.Div_Name
            , title           = ": ".join ((self.parent.title, self.Div_Name))
            )
        result = dict (dkw, ** kw)
        return result
    # end def _init_kw

    def __getattr__ (self, name) :
        if name.startswith ("db_") :
            self._populate_db_entries ()
            dn_map = self._db_name_map
            if name in dn_map :
                result = dn_map [name]
                setattr (self, name, result)
                return result
        return self.__super.__getattr__ (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        try :
            return self._db_etn_map  [key]
        except KeyError :
            return self._db_name_map [key]
    # end def __getitem__

# end class _DB_Base_

class _DB_Div_Base_ (_DB_Base_) :

    _div_name_map         = {}

# end class _DB_Div_Base_

class _DB_Div_ (_DB_Div_Base_) :
    """Division of dashboard"""

    dir_template_name     = "html/dashboard/app.jnj"

# end class _DB_Div_

_Ancestor  = _DB_Base_
_MF3_Mixin = GTW.RST.TOP.MOM.Admin.E_Type_Mixin

class _DB_E_Type_ (_MF3_Mixin, _Ancestor) :
    """E_Type displayed by, and managed via, dashboard."""

    add_css_classes          = []
    app_div_prefix           = _Ancestor.app_typ_prefix
    et_map_name              = "dash"
    create_action_name       = "create"
    fill_edit                = True
    fill_user                = False
    fill_view                = False
    hidden                   = True
    nested_db_type           = None
    nested_obj_Q             = None
    ui_allow_new             = True
    view_action_names        = ("edit", "delete")
    view_field_names         = ()       ### to be defined by subclass
    type_name                = None     ### to be defined by subclass

    _admin_delegates         = set \
        ( ( "button_types"
          , "change_query_filters"
          , "change_query_types"
          , "child_permission_map"
          , "child_postconditions_map"
          , "eligible_objects"
          , "eligible_object_restriction"
          , "query_filters_restricted"
          , "user_restriction"
          , "_field_type_attr_names"
          , "_field_class_map"
          , "_field_pred_map"
          )
        )

    _admin_func_delegates    = set \
          ( ( "add_field_classes"
            , "_fields"
            , "_field"
            , "_field_type"
            , "_field_type_by_attr"
            , "_field_type_callable"
            )
          )

    class _Action_Override_ (GTW.RST.TOP._Base_) :

        fill_edit          = True
        name_postfix       = "FF"
        page_template_name = "html/dashboard/app.jnj"

        _name_map          = dict \
            ( device       = "net_device"
            , interface    = "net_interface"
            )

        def set_request_defaults (self, form, req_data, scope) :
            def _fixed (self, req_data) :
                map = self._name_map
                for k, v in pyk.iteritems (req_data) :
                    yield map.get (k, k), v
            req_data_x = dict (_fixed (self, req_data))
            self.__super.set_request_defaults (form, req_data_x, scope)
        # end def set_request_defaults

    # end class _Action_Override_

    class _FF_Creator_ (_Action_Override_, _MF3_Mixin.Creator) :

        _real_name         = "Creator"

    Creator = _FF_Creator_ # end class

    class _FF_Instance_ (_Action_Override_, _MF3_Mixin.Instance) :

        _real_name         = "Instance"

        def rendered (self, context, template = None) :
            request = context ["request"]
            expand  = request.req_data.get ("expand_tree")
            if expand is not None :
                db_type  = self.parent
                obj      = self.obj
                template = self.top.Templateer.get_template \
                    ("html/dashboard/app.m.jnj")
                result = dict \
                    ( html = template.call_macro
                        ( "e_type_tree"
                        , db_type.nested_db_type
                        , obj
                        , db_type.nested_objects (obj)
                        , expand == "transitive"
                        )
                    )
            else :
                result = self.__super.rendered (context, template)
            return result
        # end def rendered

        def _rendered_delete (self, request, response, obj) :
            result = self.__super._rendered_delete (request, response, obj)
            if result.get ("undo") :
                scope  = self.top.scope
                change = scope.uncommitted_changes [-1]
                result ["undo"] ["url"] = pp_join \
                    (self.parent.abs_href_dynamic, "undo")
            return result
        # end def _rendered_delete

    Instance = _FF_Instance_ # end class

    class _FF_Undoer_ (_MF3_Mixin.Undoer) :

        _real_name        = "Undoer"

    Undoer = _FF_Undoer_ # end class

    class _DB_E_Type_GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def __call__ (self, resource, request, response) :
            req_data = request.req_data
            if "create" in req_data :
                creator = resource._get_child ("create")
                return creator.GET () (creator, request, response)
            else :
                return self.__super.__call__ (resource, request, response)
        # end def __call__

    GET =  _DB_E_Type_GET_ # end class

    class _DB_E_Type_POST_ (_Ancestor.POST or GTW.RST.POST) :

        _real_name             = "POST"

        def __call__ (self, resource, request, response) :
            if "qx_esf" in request.req_data :
                return resource._rendered_post_esf_form (request, response)
            else :
                return self.__super.__call__  (resource, request, response)
        # end def __call__

    POST =  _DB_E_Type_POST_ # end class

    _action_map           = dict \
        ( (r.name, r) for r in
            ( Record
                ( name = "allocate_ip"
                , msg  = _ ("Allocate an IP address for interface %(obj)s")
                , icon = "plus-circle"
                )
            , Record
                ( name = "change_email"
                , msg  = _ ("Change email of %(tn)s %(obj)s")
                , icon = "at"
                )
            , Record
                ( name = "change_password"
                , msg  = _ ("Change password of %(tn)s %(obj)s")
                , icon = "key"
                )
            , Record
                ( name = "create"
                , msg  = _ ("Create a new %(tn)s %(obj)s")
                , icon = "plus-circle"
                )
            , Record
                ( name = "delete"
                , msg  = _ ("Delete %(tn)s %(obj)s")
                , icon = "trash-o"
                )
            , Record
                ( name = "edit"
                , msg  = _ ("Edit %(tn)s %(obj)s")
                , icon = "pencil"
                )
            , Record
                ( name = "firmware"
                , msg  = _ ("Generate firmware for %(tn)s %(obj)s")
                , icon = "magic"
                )
            , Record
                ( name = "graphs"
                , msg  = _ ("Show graphs and statistics about %(tn)s %(obj)s")
                , icon = "bar-chart-o"
                )
            )
        )

    class _DB_Field_ (GTW.RST.TOP.MOM.Field.AQ) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return [self.field_name]
        # end def add_css_classes

        @Once_Property
        @getattr_safe
        def css_classes (self) :
            return self.__super.css_classes + self.add_css_classes
        # end def css_classes

    Field = _DB_Field_ # end class

    class _Field_Ref_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return [self.ref_name] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T (self.ref_name.capitalize ())
        # end def ui_name

    # end class _Field_Device_

    _Field_Created_ = GTW.RST.TOP.MOM.Field.Created

    class _Field_Device_ (_Field_Ref_) :

        ref_name          = _ ("Device")

    # end class _Field_Device_

    class _Field_Interface_ (_Field_Ref_) :

        ref_name          = _ ("Interface")

    # end class _Field_Interface_

    class _Field_IP_Address_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return ["ip-address"] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T ("IP address assigned to interface")
        # end def description

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T ("IP address")
        # end def ui_name

        def as_html (self, o, renderer) :
            result = self.__super.as_html (o, renderer)
            result = result.replace (".", zero_width_space + ".")
            return result
        # end def as_html

    # end class _Field_IP_Address_

    class _Field_IP_Addresses_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return ["ip-addresses"] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T ("IP addresses assigned to interface")
        # end def description

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T ("IP addresses")
        # end def ui_name

        def as_html (self, o, renderer) :
            v = self.value (o, renderer)
            return "<br>".join (v.split (", "))
        # end def as_thml

        def value (self, o, renderer) :
            return ", ".join \
                (   str (nw.net_address).replace (".", zero_width_space + ".")
                for nw in ichain (o.ip4_networks, o.ip6_networks)
                )
        # end def value

    # end class _Field_IP_Addresses_

    class _Field_IP_Network_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return ["ip-network"] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T ("IP network the address belongs to")
        # end def description

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T ("IP network")
        # end def ui_name

        def as_html (self, o, renderer) :
            result = self.__super.as_html (o, renderer)
            result = result.replace (".", zero_width_space + ".")
            return result
        # end def as_html

    # end class _Field_IP_Network_

    class _Field_Node_ (_Field_Ref_) :

        ref_name          = _ ("Node")

    # end class _Field_Node_

    class _Field_No_ (Field, GTW.RST.TOP.MOM.Field.Id_Entity_Collection_Size) :
        """Number-of field"""

    # end class _Field_No_

    class _Field_Device_No_ (_Field_No_) :

        attr_name = "net_devices"

    # end class _Field_Device_No_

    class _Field_Interface_No_ (_Field_No_) :

        attr_name = "net_interfaces"

    # end class _Field_Interface_No_

    class _Field_Role_ (Field) :

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T ("Indicates if you are owner or manager of the node")
        # end def description

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T ("Role")
        # end def ui_name

        def as_html (self, o, renderer) :
            owner   = o.owner
            person  = self.resource.user_restriction
            members = getattr (owner, "members", ())
            if owner == person or person in members :
                result = _T ("Owner")
            else :
                result = _T ("Manager")
            return result
        # end def as_thml

    # end class _Field_Role_

    class _Field_Type_ (_Field_Ref_) :

        icon_map = dict \
            ( W  = """<i class="fa fa-wifi"></i>"""
            , L  = """<i class="fa fa-sitemap"></i>"""
            )

        ref_name = _ ("type")

        typ_map  = \
            { "CNDB.Virtual_Wireless_Interface" : "V"
            , "CNDB.Wired_Interface"            : "L"
            , "CNDB.Wireless_Interface"         : "W"
            }

        def value (self, o, renderer) :
            code = self.typ_map.get (o.type_name, o.ui_name_T)
            if code in self.icon_map :
                code = self.icon_map [code]
            result = """<span title="%s">%s</span""" % (o.ui_name_T, code)
            return result
        # end def value

    # end class _Field_Type_

    _field_type_map       = dict \
        ( { "my_net_device.name"    : _Field_Device_
          , "my_node.name"          : _Field_Node_
          , "net_interface.name"    : _Field_Interface_
          }
        , created         = _Field_Created_
        , devices         = _Field_Device_No_
        , interfaces      = _Field_Interface_No_
        , owner           = _Field_Role_
        , type_name       = _Field_Type_
        )

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        if self.ETM.is_partial :
            self.children_np ### materialize
    # end def __init__

    @Once_Property
    @getattr_safe
    def admin (self) :
        return self._get_omu_admin (self.type_name)
    # end def admin

    @Once_Property
    @getattr_safe
    def children_np (self) :
        E_Type = self.E_Type
        result = ()
        if E_Type.is_partial :
            def _gen (self, E_Type, dn_map) :
                for k in E_Type.children_np :
                    c = self._get_dash (k)
                    if c is not None :
                        yield c
            result = sorted \
                ( _gen (self, E_Type, self._db_name_map)
                , key = Q.E_Type.i_rank
                )
        return tuple (result)
    # end def children_np

    @property ### depends on currently selected language (I18N/L10N)
    def Div_Name_T (self) :
        return _T (self.Div_Name)
    # end def Div_Name_T

    @Once_Property
    @getattr_safe
    def create_action (self) :
        if self.ui_allow_new :
            return self._action_map [self.create_action_name]
    # end def create_action

    @Once_Property
    @getattr_safe
    def ETM (self) :
        return self.admin.ETM
    # end def ETM

    @Once_Property
    @getattr_safe
    def E_Type (self) :
        return self.admin.E_Type
    # end def E_Type

    @Once_Property
    @getattr_safe
    def is_partial (self) :
        return self.E_Type.is_partial
    # end def is_partial

    @property
    @getattr_safe
    def objects (self) :
        return self.admin.objects
    # end def objects

    @property
    @getattr_safe
    def pid_query_request (self):
        return self.admin.pid_query_request
    # end def pid_query_request

    @Once_Property
    @getattr_safe
    def QR (self) :
        return self.admin.QR
    # end def QR

    @Once_Property
    @getattr_safe
    def view_actions (self) :
        map = self._action_map
        return tuple (map [k] for k in self.view_action_names)
    # end def view_actions

    @Once_Property
    @getattr_safe
    def view_fields (self) :
        return self._fields (self.view_field_names)
    # end def view_fields

    @property
    @getattr_safe
    def view_title (self) :
        TN = self.Div_Name_T
        return _T ("%ss managed/owned by %s") % (TN, self.user.FO.person)
    # end def view_title

    @Once_Property
    @getattr_safe
    def _ETM (self) :
        return self.admin._ETM
    # end def _ETM

    def href_anchor_pid (self, obj) :
        return "#%s-%s" % (self.div_name, obj.pid) if obj else ""
    # end def href_anchor_pid

    def nested_objects (self, obj) :
        q = self.nested_obj_Q
        if q is not None :
            sk = self.nested_db_type.E_Type.sorted_by
            return sorted (q (obj), key = sk)
        return ()
    # end def nested_objects

    def view_name_instance (self, o) :
        return o.FO.name
    # end def view_name_instance

    def _init_kw (self, ** kw) :
        ### keep our `_field_map` separate from `self.admin._field_map`
        return self.__super._init_kw (_field_map = {}, ** kw)
    # end def _init_kw

    def __getattr__ (self, name) :
        if name in self._admin_delegates :
            return getattr (self.admin, name)
        elif name in self._admin_func_delegates :
            result = getattr (self.admin, name)
            return lambda * args, ** kw : result.__func__ (self, * args, ** kw)
        else :
            return self.__super.__getattr__ (name)
    # end def __getattr__

# end class _DB_E_Type_

class _DB_E_Type_CNDB_ (_DB_E_Type_) :
    """CNDB specific E_Type displayed by, and managed via, dashboard."""

    child_permission_map      = dict \
        ( change              = Is_Owner_or_Manager
        , delete              = Is_Owner_or_Manager
        , undo                = Is_Deleter
        )
    child_postconditions_map  = dict \
        ( create              = (_pre_commit_entity_check, )
        , change              = (_pre_commit_entity_check, )
        )

# end class _DB_E_Type_CNDB_

class _DB_Person_Property_ (_DB_E_Type_) :

    view_action_names     = ("delete", )
    view_field_names      = \
        ( "desc"
        , "right"
        , "created"
        )

    @property
    @getattr_safe
    def mf3_attr_spec (self) :
        result = self.__super.mf3_attr_spec
        u = self.admin.user_restriction
        if u is not None :
            result = dict \
                ( result
                , left = dict (default = u, prefilled = "True")
                )
        return result
    # end def mf3_attr_spec

    @property
    @getattr_safe
    def view_title (self) :
        TN = self.Div_Name_T
        return _T ("%ss used by %s") % (TN, self.user.FO.person)
    # end def view_title

    def view_name_instance (self, o) :
        return o.right.FO
    # end def view_name_instance

# end class _DB_Person_Property_

class DB_Account (_DB_Person_Property_) :
    """PAP.Person_has_Account displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Account"
    ui_allow_new          = False
    view_action_names     = ("change_email", "change_password")

    view_field_names      = \
        ( "right"
        , "created"
        )

# end class DB_Account

class DB_Address (_DB_Person_Property_) :
    """PAP.Person_has_Address displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Address"

    @property
    @getattr_safe
    def view_title (self) :
        return _T ("Addresses used by %s") % (self.user.FO.person, )
    # end def view_title

# end class DB_Address

class DB_Device (_DB_E_Type_CNDB_) :
    """CNDB.Net_Device displayed by, and managed via, dashboard."""

    nested_db_type            = Alias_Property ("db_interface")
    nested_obj_Q              = Q.net_interfaces
    type_name                 = "CNDB.Net_Device"

    view_action_names         = _DB_E_Type_CNDB_.view_action_names
    view_field_names          = \
        ( "name"
        , "net_device_type"
        )

    _DB_icon_name             = "cube"

    _MF3_Attr_Spec            = dict \
        ( node                = dict (restrict_completion = True)
        , left                = dict
            (input_widget = "mf3_input, id_entity_select")
        )

    def tr_instance_css_class (self, o) :
        return "node-%d- device-%d-" % (o.my_node.pid, o.pid)
    # end def tr_instance_css_class

# end class DB_Device

class DB_Edit (_DB_Div_) :
    """Edit division of dashboard"""

    hidden                = True

# end class DB_Edit

class DB_Email (_DB_Person_Property_) :
    """PAP.Person_has_Email displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Email"

# end class DB_Email

class DB_IM_Handle (_DB_Person_Property_) :
    """PAP.Person_has_IM_Handle displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_IM_Handle"

# end class DB_IM_Handle

_Ancestor = _DB_E_Type_CNDB_

class _DB_Interface_ (_Ancestor) :

    _MF3_Attr_Spec        = dict \
        ( left            = dict (restrict_completion = True)
        )

    class _DBI_Action_Override_ (_Ancestor._Action_Override_) :

        def _commit_scope_fv (self, scope, form_value, request, response) :
            ### Here, one could do special actions like automatically
            ### allocation an IP address for the interface
            self.__super._commit_scope_fv (scope, form_value, request, response)
        # end def _commit_scope_fv

    # end class _DBI_Action_Override_

    class _DBI_Creator (_DBI_Action_Override_, _Ancestor.Creator) :

        _real_name         = "Creator"

    Creator = _DBI_Creator # end class

    class _DBI_Instance_ (_DBI_Action_Override_, _Ancestor.Instance) :

        _real_name         = "Instance"

    Instance = _DBI_Instance_ # end class

# end class _DB_Interface_

_Ancestor = _DB_Interface_

class DB_Interface (_Ancestor) :
    """CNDB.Net_Interface displayed by, and managed via, dashboard."""

    app_div_class             = "pure-u-1"
    nested_db_type            = Alias_Property ("db_interface_in_ip_network")
    type_name                 = "CNDB.Net_Interface"
    xtra_template_macro       = "html/dashboard/app.m.jnj, db_graph"

    view_field_names          = \
        ( "name"
        ,
        )

    _field_type_map           = dict \
        ( _DB_E_Type_CNDB_._field_type_map
        , ip4_networks        = _DB_E_Type_CNDB_._Field_IP_Addresses_
        )

    def nested_obj_Q (self, interface) :
        return ichain \
            (interface.ip4_network_links, interface.ip6_network_links)
    # end def nested_obj_Q

    def tr_instance_css_class (self, o) :
        return "node-%d- device-%d- interface-%d-" % \
            (o.my_node.pid, o.my_net_device.pid, o.pid)
    # end def tr_instance_css_class

# end class DB_Interface

_Ancestor = DB_Interface

class DB_Wired_Interface (_Ancestor) :
    """CNDB.Wired_Interface displayed by, and managed via, dashboard."""

    type_name                 = "CNDB.Wired_Interface"
    _DB_icon_name             = "sitemap"

# end class DB_Wired_Interface

class DB_Wireless_Interface (_Ancestor) :
    """CNDB.Wireless_Interface displayed by, and managed via, dashboard."""

    type_name                 = "CNDB.Wireless_Interface"

    _DB_icon_name             = "wifi"

    _MF3_Attr_Spec            = dict \
        ( standard            = dict
            (input_widget = "mf3_input, id_entity_select")
        )

# end class DB_Wireless_Interface

if 0 : ### Add this when there is an instance of User_Virtual_Wireless_Interface
    class DB_Virtual_Wireless_Interface (_Ancestor) :
        """CNDB.Virtual_Wireless_Interface displayed by, and managed via, dashboard."""

        type_name                 = "CNDB.Virtual_Wireless_Interface"

        _DB_icon_name             = "plug"

    # end class DB_Virtual_Wireless_Interface

_Ancestor = _DB_E_Type_CNDB_

class DB_Interface_in_IP_Network (_Ancestor) :
    """CNDB.Net_Interface_in_IP_Network links for a single Net_Interface
       displayed by, and managed via, dashboard.
    """

    create_action_name        = "allocate_ip"
    view_action_names         = ("delete", )
    type_name                 = "CNDB.Net_Interface_in_IP_Network"

    view_field_names          = \
        ( "right.net_address"
        , "right.pool.net_address"
        )

    _field_type_map           = dict \
        ( _Ancestor._field_type_map
        , ** { "right.net_address"      : _Ancestor._Field_IP_Address_
             , "right.pool.net_address" : _Ancestor._Field_IP_Network_
             }
        )

    class Allocate_IP (GTW.RST.TOP.Page) :
        """Resource to allocate a single IP address for the selected
           interface.
        """

        class _AIP_POST_ (GTW.RST.POST) :

            _real_name             = "POST"
            _renderers             = (GTW.RST.Mime_Type.JSON, )

            def _response_body (self, resource, request, response) :
                Bad_Req   = resource.Status.Bad_Request
                req_data  = request.req_data
                result    = {}
                user      = resource.user_restriction
                scope     = resource.scope
                CNDB      = scope.CNDB
                ipid      = req_data.get ("interface")
                ppid      = req_data.get ("pool")
                if ipid is None :
                    raise Bad_Req (_T ("Request must include interface pid"))
                try :
                    iface = scope.pid_query (ipid)
                except LookupError as exc :
                    raise (Bad_Req (str (exc)))
                node      = iface.my_node
                if ppid is not None :
                    try :
                        pool = scope.pid_query (ppid)
                    except LookupError as exc :
                        raise (Bad_Req (str (exc)))
                    else :
                        pools = [pool]
                else :
                    def _query (ETM, node, user) :
                        bitlen = ETM.left.net_address.P_Type.bitlen
                        return ETM.query \
                            ( Q.OR
                                ( Q.right.node == node
                                , Q.AND
                                    ( ~ Q.right.node
                                    , Q.right.group_links.right.member_links
                                        .left == user
                                    # possibly,
                                    # a Q-expression checking various quotas
                                    )
                                )
                            & Q.OR
                                ( ~ Q.right.netmask_interval.upper
                                , Q.right.netmask_interval.upper == bitlen
                                )
                            ).attr (Q.right).distinct ()
                    pools = list \
                        ( p for p in ichain
                            ( _query (CNDB.IP4_Network_in_IP4_Pool, node, user)
                            , _query (CNDB.IP6_Network_in_IP6_Pool, node, user)
                            )
                        if p.can_allocate ()
                        )
                n_pools   = len (pools)
                ### XXX
                ### filter pools by quota
                ### if none remain
                ###   --> send feedback about the full pools available
                template = resource.top.Templateer.get_template \
                    ("html/dashboard/app.m.jnj")
                if not n_pools :
                    result ["feedback"] = _T \
                        ( "No pools available that allow allocation "
                          "by user %(user)s and node %(node)s"
                        % dict (user = user, node = node)
                        )
                elif n_pools == 1 :
                    pool = TFL.first (pools)
                    nw0  = TFL.first (pool.ip_networks)
                    try :
                        ipa  = pool.allocate (nw0.net_address.bitlen, user)
                    except Exception as exc :
                        result ["feedback"] = str (exc)
                    else :
                        iii  = scope.CNDB.Net_Interface_in_IP_Network \
                            (iface, ipa, mask_len = ipa.pool.net_address.mask)
                        result ["row"] = template.call_macro \
                            ("e_type_tree_li", resource, iii, False)
                else :
                    result ["menu"] = template.call_macro \
                        ("action_button_allocate_ip_pool_menu", resource, pools)
                return result
            # end def _response_body

        POST = _AIP_POST_ # end class

    # end class Allocate_IP

    @property ### depends on currently selected language (I18N/L10N)
    def Div_Name_T (self) :
        return "IP " + _T ("Address")
    # end def Div_Name_T

    @Once_Property
    @getattr_safe
    def is_partial (self) :
        return False
    # end def is_partial

    def tr_instance_css_class (self, o) :
        fmt = " ".join \
            ( (x + "-%d-") for x in
                ["node", "device", "interface", "interface_in_ip_network"]
            )
        return fmt % (o.my_node.pid, o.my_net_device.pid, o.left.pid, o.pid)
    # end def tr_instance_css_class

    def _get_child (self, child, * grandchildren) :
        if child == "allocate_ip" :
            result = self.Allocate_IP \
                ( name   = child
                , parent = self
                , hidden = True
                )
            if grandchildren :
                result = result._get_child \
                    (grandchildren [0], * grandchildren [1:])
        else :
            result = self.__super._get_child (child, * grandchildren)
        return result
    # end def _get_child

# end class DB_Interface_in_IP_Network

class DB_Node (_DB_E_Type_CNDB_) :
    """CNDB.Node displayed by, and managed via, dashboard."""

    app_div_class             = "pure-u-1 pure-u-md-1-2"

    child_postconditions_map  = dict \
        ( _DB_E_Type_CNDB_.child_postconditions_map
        , change = (_pre_commit_node_check, _pre_commit_entity_check)
        )

    nested_db_type            = Alias_Property ("db_device")
    nested_obj_Q              = Q.net_devices
    type_name                 = "CNDB.Node"
    xtra_template_macro       = "html/dashboard/app.m.jnj, db_node_map"

    view_field_names          = \
        ( "name"
        , "owner"
        )

    _DB_icon_name             = "cubes"

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = {}
        u = self.admin.user_restriction
        if u is not None :
            result = dict \
                ( result
                , manager = dict (default = u)
                , owner   = dict (default = u)
                )
        result = dict \
            ( result
            # address  = dict (skip = True)
            , lifetime = dict (skip = True)
            )
        return result
    # end def mf3_attr_spec_d

    @property
    @getattr_safe
    def position (self) :
        lat, lon = (0, 0)
        n = 0
        for node in self.objects :
            if node.position.lat and node.position.lon :
                lat += node.position.lat
                lon += node.position.lon
                n += 1
        if n :
            lat /= n
            lon /= n
            result = self.E_Type.position.P_Type (lat, lon)
        else :
            result = self.E_Type.position.P_Type ()
        return result
    # end def position

# end class DB_Node

class DB_Person (_DB_E_Type_) :
    """PAP.Person displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person"

    ui_allow_new          = False
    view_action_names     = ("edit", )
    view_field_names      = \
        ( "ui_display"
        , "created"
        )

    @property
    @getattr_safe
    def MF3_Form_Spec (self) :
        result = dict \
            ( include_rev_refs = ("addresses", "emails", "phones")
            )
        return result
    # end def MF3_Form_Spec

    @property
    @getattr_safe
    def view_title (self) :
        return _T ("Personal data of %s") % (self.user.FO.person, )
    # end def view_title

    def view_name_instance (self, o) :
        return o.FO
    # end def view_name_instance

# end class DB_Person

class DB_Phone (_DB_Person_Property_) :
    """PAP.Person_has_Phone displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Phone"

# end class DB_Phone

class DB_User (_DB_Div_) :
    """User division of dashboard"""

    _entry_types          = \
        ( DB_Person
        , DB_Account
        , DB_Address
        , DB_Email
        , DB_IM_Handle
        , DB_Phone
        )

# end class DB_User

class DB_View (_DB_Div_) :
    """View division of dashboard"""

    _entry_types          = \
        ( DB_Node
        , DB_Device
        , DB_Interface
        , DB_Interface_in_IP_Network
        )

    def render_context (self, resource = None, ** kw) :
        if resource is None :
            resource = self
        def _gen (req_data) :
            for i in req_data.get ("expand_trees", "").split (",") :
                try :
                    x = i.strip ()
                    if x :
                        yield int (x)
                except Exception as exc :
                    logging.exception \
                        ( "Exception for query argument expand_trees: "
                          "`%s`, value `%s`"
                        % (q_expand_trees, i)
                        )
        kw ["expand_trees"] = set (_gen (resource.request.req_data))
        return self.__super.render_context (resource, ** kw)
    # end def render_context

# end class DB_View

_Ancestor = _DB_Div_Base_

class Dashboard (_Ancestor) :
    """CNDB dashboard"""

    pid                   = "Dashboard"

    _entry_types          = \
        ( DB_View
        , DB_User
        , DB_Edit
        )
    _entry_type_names     = \
        DB_View._entry_type_names | DB_User._entry_type_names

    def _init_kw (self, ** kw) :
        dkw = dict \
            ( name            = "dashboard"
            , short_title     = "Dashboard"
            , title           = "Funkfeuer Dashboard"
            , auth_required   = True
            , permission      = Login_has_Person
            )
        result = dict (dkw, ** kw)
        return result
    # end def _init_kw

    def _populate_db_entries (self) :
        ### populate `entries`, `entry_map`, `_div_name_map`
        for e in self.entries :
            e.entries
    # end def _populate_db_entries

# end class Dashboard

### __END__ RST_addons
