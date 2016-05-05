// Copyright (C) 2014-2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    html/dashboard/app.js
//
// Purpose
//    Javascript code for CNDB dashboard
//
// Revision Dates
//    15-Apr-2014 (CT) Creation
//     2-May-2014 (CT) Add `graph_cb`
//     3-May-2014 (CT) Add `active_filters`; pass contents to `?create`
//     4-May-2014 (CT) Add `filter_typ_cb ["interface"]`, `graph_interface_cb`
//     1-Sep-2014 (CT) Change `url` of `create_cb`
//     2-Sep-2014 (CT) Fix change of `url` of `create_cb` (active_filters)
//     2-Sep-2014 (MB) Remove Graph action from filter button for interface
//     3-Sep-2014 (MB) Focus map to filtered node - added focus_map_cb
//                     Move Map to JS
//                     Map now filters nodes and vice versa
//     3-Sep-2014 (CT) Add `create_p_cb` and `create_t_cb`
//     3-Sep-2014 (MB) Added map to edit of node
//     4-Sep-2014 (MB) Allow setting and dragging of markers
//     4-Sep-2014 (MB) Add geolocate button
//                     Remove Zip code from fields - seems to mess with
//                     geolocation some times
//     5-Sep-2015 (MB) toggle visibility of interface ip list
//    16-Sep-2014 (CT) Remove action `manage_ip`, use `filter` instead;
//                     add `filter_typ_remove_cb`, `ip_hide_cb`, `ip_show_cb`
//    16-Sep-2014 (CT) Add action `allocate_ip`
//    23-Sep-2014 (CT) Factor `setup_buttons`, use it in `allocate_ip_cb`
//    23-Sep-2014 (CT) Fix `menu` in `allocate_ip_cb`
//     3-Dec-2014 (CT) Adapt to changes in grid of pure-0.5.0
//    16-Dec-2014 (CT) Change `initialize_map` to allow `data ("markers")`
//                     returning a string
//     7-Apr-2015 (CT) Add `data-etn` to `.url` of `obj_of_row`
//     1-Jun-2015 (CT) Add `action_cb_wrapper` to guard `.deleted`;
//                     use `ev.currentTarget`, not `ev.delegateTarget`
//     1-Jun-2015 (CT) Add `undo_cb`, add `undo` to `delete_cb`
//    12-Jun-2015 (CT) Add `change_email_cb`, `change_password_cb`
//    29-Jun-2015 (CT) Add `hide_map_cb`, `show_map_cb`
//     3-Jul-2015 (CT) Add `expand_collapse_cb`
//     3-Jul-2015 (CT) Adapt `allocate_ip_cb` response `row` to tree structure
//     6-Jul-2015 (CT) Add AJAX call for `expand_tree` to `expand_collapse_cb`
//     6-Jul-2015 (CT) Add `fix_history_xc`, `ids_of_expanded_objs`
//     7-Jul-2015 (CT) Change `create_cb` to consider `outer_ids` stored in
//                     `class` of closest `obj_row`
//     7-Jul-2015 (CT) Use `dialog` for `partial-type-menu`
//     8-Jul-2015 (CT) Adapt `delete_cb` to tree structure
//     8-Jul-2015 (CT) Fix interaction between node-tree and node-map
//     8-Jul-2015 (CT) Add `instance_spans` to make entity-instance fields
//                     clickable to expand/collapse the nested tree
//     9-Jul-2015 (CT) Make map resizable
//     5-May-2016 (CT) Use `$V5a.new_window`, not homegrown code
//    ««revision-date»»···
//--

;( function ($) {
    "use strict";
    $.fn.cndb_dashboard = function cndb_dashboard (opts) {
        var selectors = $.extend
            ( { app_div                : "[id^=\"app-D:\"]"
              , app_div_edit           : "[id=\"app-D:edit\"]"
              , app_div_id             : "[id=\"app-T:interface_in_ip_network\"]"
              , allocate_ip_button     : "[href=#allocate_ip]"
              , change_email_button    : "[href=#change_email]"
              , change_password_button : "[href=#change_password]"
              , create_button          : "[href=#create]"
              , create_button_p        : "[href=#create-partial]"
              , create_button_t        : "[href=#create-type]"
              , delete_button          : "[href=#delete]"
              , edit_button            : "[href=#edit]"
              , firmware_button        : "[href=#firmware]"
              , hide_map_button        : "[data-action=\"hide-map\"]"
              , href_action            : "li [href^=#], .action [href^=#]"
              , obj_row                : "li[id]"
              , partial_type_menu      : ".partial-type-menu"
              , root                   : "#app"
              , show_map_button        : "[data-action=\"show-map\"]"
              , undo_button            : "[data-action=\"undo\"]"
              , xc_button              : "[href=#XC]"
              }
            , opts && opts ["selectors"] || {}
            );
        var page_url  =
            (opts ["urls"] && opts ["urls"] ["page"]) || "/dashboard/";
        var urls      = $.extend
            ( { page             : page_url
              , pid              : page_url + "pid/"
              }
            , opts && opts ["urls"] || {}
            );
        var options   = $.extend
            ( { active_button_class   : "pure-button-active"
              , app_div_prefix        : "app-D:"
              , app_typ_prefix        : "app-T:"
              , e_type_class          : "ET"
              , e_type_instance_class : "ETI"
              , e_type_tree_class     : "ETT"
              , icon_collapse         : "fa-minus-square-o"
              , icon_expand           : "fa-plus-square-o"
              , xc_class_collapse     : "collapse"
              , xc_class_expand       : "expand"
              }
            , opts || {}
            , { selectors : selectors
              , urls      : urls
              }
            );
        var nodes           = {};
        var pat_div_name    = new RegExp (options.app_div_prefix + "(\\w+)$");
        var pat_pid         = new RegExp ("^([^-]+)-(\\d+)-?$");
        var pat_typ_name    = new RegExp
            (options.app_typ_prefix + "(\\w+)@?(\\d+)?$");
        var q_xc_pat        = new RegExp ("([?&]expand_trees=)[^&]*");
        var action_cb_wrapper = function action_cb_wrapper (ev) {
            var target$     = $(ev.currentTarget);
            var action_cb   = target$.data ("act_cb");
            var row$        = closest_el   (target$, selectors.obj_row);
            if (row$.hasClass ("deleted")) {
                return false;
            } else {
                return action_cb.call (target$, ev);
            };
        };
        var allocate_ip_cb  = function allocate_ip_cb (ev) {
            var ev_target$  = $(ev.currentTarget);
            var pool_pid    = ev_target$.data ("pool-pid");
            var target$     = ev_target$.closest
                (selectors.partial_type_menu).data ("button") || ev_target$;
            var t_row$      = target$.closest (selectors.obj_row);
            var sid         = closest_el_id (target$, "section");
            var sid_match   = sid.match (pat_typ_name);
            var typ         = sid_match [1];
            var pid         = sid_match [2];
            var url         = options.urls.page + typ + "/allocate_ip";
            var success_cb  = function success_cb (response, status) {
                var row$, menu$, ul$;
                if (! response ["error"]) {
                    if ("row" in response) {
                        row$ = $(response.row);
                        ul$  = t_row$.find     ("> section > ul")
                        ul$.append             (row$);
                        setup_buttons          (row$);
                        row$.addClass          ("feedback");
                        menu$ = target$.data   ("menu");
                        if (menu$) {
                            menu$.dialog       ("destroy");
                            target$.removeData ("menu");
                        };
                    } else if ("menu" in response) {
                        setup_menu
                            ( target$, $(response.menu)
                            , { autoOpen : true
                              , position :
                                  { my   : "right top"
                                  , at   : "right bottom"
                                  , of   : target$
                                  }
                              }
                            );
                        setup_buttons (target$.data ("menu"))
                    } else if ("feedback" in response) {
                        $GTW.show_message
                            ("Feedback from server: " + response.feedback);
                    } else {
                        $GTW.show_message
                            ("Unknown response", response);
                    };
                } else {
                    $GTW.show_message
                        ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "POST"
                  , data        :
                      { "interface" : pid
                      , "pool"      : pool_pid
                      }
                  , url         : url
                  , success     : success_cb
                  }
                , "Allocate IP"
                );
            return false;
        };
        var change_email_cb = function change_email_cb (ev) {
            var obj  = obj_of_row (this);
            var url  = "/Auth/change_email?p=" + obj.pid;
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
        } ;
        var change_password_cb = function change_password_cb (ev) {
            var obj  = obj_of_row (this);
            var url  = "/Auth/change_password?p=" + obj.pid;
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
        } ;
        var closest_el     = function closest_el (self, selector) {
            return $(self).closest (selector);
        };
        var closest_el_id = function closest_el_id (self, selector) {
            return $(self).closest (selector).prop ("id");
        };
        var create_cb = function create_cb (ev, sub_typ) {
            var sid     = closest_el_id (this, "section");
            var typ     = sid.match     (pat_typ_name) [1];
            var midd    = (! sub_typ) ? "" : ("/" + sub_typ);
            var t_row$  = $(this).closest  (selectors.obj_row);
            var url     = options.urls.page + typ + midd + "/create";
            var afs, tr_classes, outer_ids = {};
            if (t_row$.length) {
                tr_classes = t_row$.prop ("class").split (" ");
                for (var i = 0, li = tr_classes.length, c, m; i < li; i++) {
                    c = tr_classes [i];
                    m = c.match (pat_pid);
                    if (m.length) {
                        outer_ids [m [1]] = m [2];
                    };
                };
            };
            afs = $.param  (outer_ids);
            if (afs.length > 0) {
                url = url + "?" + afs;
            };
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
        };
        var create_p_cb = function create_p_cb (ev) {
            var target$ = $(ev.currentTarget);
            var menu$   = target$.data ("menu");
            if (menu$.is (":visible")) {
                menu$.dialog ("close");
            } else {
                menu$
                    .dialog ("open")
                    .dialog ("widget")
                        .position
                            ( { my : "right top"
                              , at : "right bottom"
                              , of : target$
                              }
                            );
            };
            return false;
        };
        var create_t_cb = function create_t_cb (ev) {
            var target$ = $(ev.target);
            var sub_typ = target$.data    ("etn");
            var menu$   = target$.closest (".partial-type-menu");
            var button$ = menu$.data      ("button");
            menu$.dialog          ("close");
            return create_cb.call (button$, ev, sub_typ);
        };
        var delete_cb = function delete_cb (ev) {
            var obj   = obj_of_row (this);
            var success_cb = function success_cb (response, status) {
                var row$   = obj.row$;
                var eti$, et$, etc$, repl$, xc$;
                if (! response ["error"]) {
                    eti$   = row$.children (selectors.e_type_instance);
                    et$    = eti$.children (selectors.e_type);
                    xc$    = eti$.children (".XC");
                    repl$  = $
                        ( "<div class=\""
                        + options.e_type_instance_class
                        + " feedback\"></div>"
                        );
                    if (xc$.length) {
                        repl$.append
                            ( "<span class=\"XC\">"
                            + "<a><i class=\"fa fa-ban\"></i></a>"
                            + "</span>"
                            );
                    };
                    if (et$.length) {
                        etc$ = et$.clone ();
                        etc$.css ("cursor", "auto");
                        repl$.append (etc$);
                    };
                    repl$.append
                        ( "<span class=\"Field\">"
                        + response.feedback
                        + "</span>"
                        );
                    if ("undo" in response) {
                        row$.data ("deleted", row$.html ());
                        row$.data ("title",   row$.prop ("title"));
                        row$.data ("undo",    response.undo);
                        repl$.append
                            ( "<span class=\"action\">"
                            + "<a class=\"pure-button\" data-action=\"undo\""
                            + "title=\"" + response.undo.title + "\""
                            + ">"
                            + "<i class=\"fa fa-undo\"></i>"
                            + "</a>"
                            + "</span>"
                            );
                    };
                    row$.addClass ("deleted");
                    row$.html     (repl$);
                    row$.prop     ("title", "");
                    setup_buttons (row$);
                } else {
                    $GTW.show_message ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "DELETE"
                  , url         : obj.url
                  , success     : success_cb
                  }
                , "Delete"
                );
            return false;
        };
        var edit_cb   = function edit_cb (ev) {
            var obj         = obj_of_row (this);
            var referrer_id = closest_el_id (this, selectors.app_div);
            var url         = obj.url;
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
            var success_cb  = function success_cb (response, status) {
                if (! response ["error"]) {
                    var target_id =
                        response ["target_id"] || selectors.app_div_edit;
                    var target$   = $(target_id);
                    var form$     = $(response ["form"]);
                    form$.data ("ffd_referrer", referrer_id);
                    target$.prepend (form$);
                    $(selectors.app_div).hide ();
                    target$.show ();
                } else {
                    $GTW.show_message
                        ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "GET"
                  , url         : url
                  , success     : success_cb
                  }
                , "Edit"
                );
            return false;
        };
        var expand_collapse_cb = function expand_collapse_cb (ev, target, transitive) {
            var target$   = $(target || ev.currentTarget);
            var icon$     = target$.children (".fa");
            var t_row$    = target$.closest  (selectors.obj_row);
            var nested$   = t_row$.children  ("section");
            var obj       = obj_of_row       (target$);
            var _collapse = function _collapse () {
                target$
                    .removeClass (options.xc_class_collapse)
                    .addClass    (options.xc_class_expand);
                icon$
                    .removeClass (options.icon_collapse)
                    .addClass    (options.icon_expand);
                fix_history_xc   ();
                if (nodes [obj.pid]) {
                    nodes [obj.pid].closePopup ();
                };
            };
            var _expand   = function _expand () {
                target$
                    .removeClass (options.xc_class_expand)
                    .addClass    (options.xc_class_collapse);
                icon$
                    .removeClass (options.icon_expand)
                    .addClass    (options.icon_collapse);
                fix_history_xc   ();
                if (nodes [obj.pid]) {
                    nodes [obj.pid].openPopup ();
                };
            };
            if (target$.hasClass (options.xc_class_collapse)) {
                nested$.hide ();
                _collapse    ();
            } else if (nested$.length) {
                nested$.show ();
                _expand      ();
            } else {
                var success_cb = function success_cb (response, status) {
                    if (! response ["error"]) {
                        t_row$.append  (response ["html"]);
                        setup_buttons  (t_row$);
                        _expand        ();
                    } else {
                        $GTW.show_message ("Ajax Error: " + response ["error"]);
                    };
                };
                $.gtw_ajax_2json
                    ( { type        : "GET"
                      , data        : "expand_tree="
                          + ( (transitive || (ev && ev.ctrlKey))
                            ? "transitive"
                            : 1
                            )
                      , url         : obj.url
                      , success     : success_cb
                      }
                    , "Expand nested"
                    );
            };
            return false;
        };
        var expand_node = function expand_node (pid) {
            var node$ = $("[id='node-" + pid + "']");
            if (! node$.hasClass ("deleted")) {
                var xc$   = $(selectors.xc_button, node$).first ();
                if (xc$.hasClass (options.xc_class_expand)) {
                    expand_collapse_cb (null, xc$, true);
                };
            };
        };
        var expand_collapse_node_cb = function expand_node_cb (ev) {
            var obj  = obj_of_row (this);
            var row$ = obj.row$;
            if (! row$.hasClass ("deleted")) {
                var xc$  = $(selectors.xc_button, row$).first ();
                expand_collapse_cb (null, xc$);
                return false;
            };
        };
        var firmware_cb = function firmware_cb (ev) {
            var a$    = $(this);
            var row$  = closest_el (this, selectors.obj_row);
            var name  = $(".name", row$).text ();
            var msgs$ = $("#messages");
            var mid   = new Date().valueOf().toString();
            var msg$  =
                $( "<a class=\"feedback\" id=\""
                + mid + "\" href=\"#" + mid+ "\">"
                + "The firmware for " + name
                + " will be built and an email with the download URL "
                + "sent to you."
                + "<i>✕</i></a>"
                );
            msgs$.append (msg$);
            msg$.focus ();
            msg$.on    ("click", hide_feedback);
        };
        var fix_history_xc = function fix_history_xc () {
            var ids = ids_of_expanded_objs ().join (",");
            if (ids) {
                var url   = window.location.href.split ("?") [0];
                var q     = window.location.search;
                var q_new = q.match (q_xc_pat)
                    ? q.replace (q_xc_pat, "$1" + ids)
                    : "?expand_trees=" + ids;
                $GTW.push_history (url + q_new);
            };
        };
        var graph_cb = function graph_cb (ev) {
            var a$    = $(this);
            var row$  = closest_el     (this, selectors.obj_row);
            var rid   = row$.prop      ("id");
            var typ   = type_of_obj_id (rid);
            var pref  =
                "https://marvin.funkfeuer.at/cgi-bin/smokeping/freenet.cgi?target=";
            var name  = $(".name", row$).text ();
            var node, url;
            if (typ == "node") {
                url   = pref + name;
            } else if (typ == "interface") {
                node  = $(".Node", row$).text ();
                url   = pref + node + "." + name;
            } else {
                alert ("Graph type " + typ + " is not implemented");
            };
            if (url) {
                $V5a.new_window (url);
            };
        };
        var graph_interface_cb = function graph_interface_cb (ev) {
            var a$    = $(this);
            var dg$   = $("#interface-graph");
            var row$  = closest_el     (this, selectors.obj_row);
            var name  = $(".name", row$).text ();
            var node  = $(".Node", row$).text ();
            var pref  =
                "https://marvin.funkfeuer.at/cgi-bin/smokeping/freenet.cgi?target=";
            var rid   = row$.prop      ("id");
            var typ   = type_of_obj_id (rid);
            var url_g =
                ( "https://marvin.funkfeuer.at/smokeping/freenet/"
                + node + "/" + name
                + "_last_86400.png"
                );
            var url_h = pref + node + "." + name;
            dg$.html
                ( "<a href=\""  + url_h + "\" target=\"_blank\">"
                + "<img src=\"" + url_g + "\" alt=\"Smokeping Graphik für " + name + "." + node + "\"/>"
                + "</a>"
                );
        };
        var hide_map_cb = function hide_map_cb (ev) {
            var button$ = $(ev.currentTarget);
            var id      = button$.attr ("href").replace (/^#/, "");
            var target$ = $("[id='" + id + "']");
            target$.addClass ("hidden");
            return false;
        };
        var hide_feedback = function hide_feedback (ev) {
            var target$ = $(ev.target);
            target$.remove ();
            return false;
        };
        var ids_of_expanded_objs = function ids_of_expanded_objs () {
            var xb$    = $(selectors.xc_button_collapse);
            var result = [];
            xb$.each ( function ()
              {
                var sid = closest_el_id (this, selectors.obj_row);
                result.push (pid_of_obj_id (sid));
              }
            );
            return result;
        };
        var obj_of_row  = function obj_of_row (self) {
            var result  = {};
            var row$    = closest_el       (self, selectors.obj_row)
            var sub_typ = row$.data        ("etn");
            var midd    = (! sub_typ) ? "" : ("/" + sub_typ);
            result.row$ = row$;
            result.rid  = row$.prop        ("id");
            result.pid  = pid_of_obj_id    (result.rid);
            result.sid  = closest_el_id    (self, "section");
            result.typ  = result.sid.match (pat_typ_name) [1];
            result.url  =
                options.urls.page + result.typ + midd + "/" + result.pid;
            return result;
        };
        var obj_rows_selector_all = function obj_rows_selector_all (id) {
            var typ = type_of_obj_id (id);
            return selectors.obj_row + "[class*=\"" + typ + "-\"]";
        };
        var obj_rows_selector_sel = function obj_rows_selector_sel (id) {
            return selectors.obj_row + "[class~=\"" + id + "-\"]";
        };
        var pid_of_obj_id = function pid_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [2];
        };
        var show_map_cb = function show_map_cb (ev) {
            var button$ = $(ev.currentTarget);
            var id      = button$.attr ("href").replace (/^#/, "");
            var target$ = $("[id='" + id + "']");
            target$.removeClass ("hidden");
            return false;
        };
        var type_of_obj_id = function type_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [1];
        };
        var undo_cb  = function undo_cb (ev) {
            var obj  = obj_of_row (this);
            var row$ = obj.row$;
            var rest = row$.data ("deleted");
            var undo = row$.data ("undo");
            if (undo) {
                var success_cb = function success_cb (response, status) {
                    if (! response ["error"]) {
                        row$.html         (rest);
                        row$.data         ("deleted", undefined);
                        row$.data         ("undo",    undefined);
                        row$.removeClass  ("deleted");
                        row$.prop         ("title", row$.data ("title"));
                        setup_buttons     (row$);
                    } else {
                        $GTW.show_message
                            ("Ajax Error: " + response ["error"]);
                    };
                };
                $.gtw_ajax_2json
                    ( { type        : "POST"
                      , data        : undo
                      , success     : success_cb
                      , url         : undo.url
                      }
                    , "Undo"
                    );
            } else {
                $GTW.show_message ("No undo information in DOM");
                $(".action", row$).empty ();
            };
            return false;
        };

        var ip_hide_cb = function ip_hide_cb (ev) {
            var l$ = $(selectors.app_div_id);
            l$.hide ();
        };
        var ip_show_cb = function ip_show_cb (ev) {
            var l$ = $(selectors.app_div_id);
            l$.show ();
        };
        var setup_buttons = function setup_buttons (context$) {
            var S = selectors;
            $(S.instance_spans,         context$).css  ("cursor", "pointer");
            $(S.allocate_ip_button,     context$).data ("act_cb", allocate_ip_cb);
            $(S.change_email_button,    context$).data ("act_cb", change_email_cb);
            $(S.change_password_button, context$).data ("act_cb", change_password_cb);
            $(S.create_button,          context$).data ("act_cb", create_cb);
            $(S.create_button_p,        context$).data ("act_cb", create_p_cb);
            $(S.create_button_t,        context$).data ("act_cb", create_t_cb);
            $(S.delete_button,          context$).data ("act_cb", delete_cb);
            $(S.edit_button,            context$).data ("act_cb", edit_cb);
            $(S.firmware_button,        context$).data ("act_cb", firmware_cb);
            $(S.xc_button,              context$).data ("act_cb", expand_collapse_cb);
            $(S.partial_type_menu,      context$).each
                ( function () {
                    var ptm$ = $(this);
                    var but$ = ptm$.prev (S.create_button_p);
                    setup_menu (but$, ptm$);
                  }
                );
        }
        var setup_menu = function setup_menu (button$, menu$, opts) {
            menu$.data ("button", button$);
            button$.data
              ( "menu"
              , menu$.dialog
                  ( $.extend
                      ( { autoOpen : false
                        , title    : menu$.attr ("title")
                        , width    : "auto"
                        }
                      , opts || {}
                      )
                  )
              );
        };
        var this$                      = $(this);
        selectors.e_type               = "." + options.e_type_class;
        selectors.e_type_instance      = "." + options.e_type_instance_class;
        selectors.e_type_tree          = "." + options.e_type_tree_class;
        selectors.xc_button_collapse   =
            "." + options.xc_class_collapse   + selectors.xc_button;
        selectors.xc_button_epxand     =
            "." + options.xc_class_expand     + selectors.xc_button;
        selectors.instance_spans      =
            ( ":not(.leaf) > "
            + selectors.obj_row + ":not(.deleted) > "
            + selectors.e_type_instance + " > span:not(.action)"
            );
        setup_buttons (this);
        this$.on ("click", selectors.href_action,     action_cb_wrapper);
        this$.on ("click", selectors.instance_spans,  expand_collapse_node_cb);
        this$.on ("click", selectors.hide_map_button, hide_map_cb);
        this$.on ("click", selectors.show_map_button, show_map_cb);
        this$.on ("click", selectors.undo_button,     undo_cb);
        fix_history_xc ();
        // hide the ip in interface list on ready
        $(document).ready(function () {
            $(selectors.app_div_id).hide ();
            }
        );
        // initialize the map
        $(document).ready(function initialize_map () {
            var ms = $(".map[data-markers]");
            ms.resizable ({ autoHide : false, distance : 10, ghost : false });
            L.Icon.Default.imagePath = "/media/GTW/css/images";
            for (var j=0;j<ms.length;j++) {
                var el = $(ms[j]);
                var d_markers = el.data("markers");
                // Firefox 34 returns an object, not a string, for `markers`
                var node_data = typeof d_markers === "string" ?
                    JSON.parse(d_markers) : d_markers;
                var node_map = L.map(el.attr('id'));
                L.tileLayer ( 'https://\{s\}.tile.openstreetmap.org/\{z\}/\{x\}/\{y\}.png'
                    , { maxZoom: 18
                      , attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' + '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
                      }
                    ).addTo (node_map);
                var markers = L.featureGroup()
                    .addTo(node_map);
                for (var i in node_data) {
                    var n = node_data[i];
                    nodes[n.pid] =
                        L.marker ([n.pos.lat, n.pos.lon])
                            .addTo (markers)
                            .bindPopup ("<b>"+n.name+"</b>")
                            .on ( "popupopen"
                                , function (p) {
                                    var pid = p;
                                    return function (ev) {
                                      return expand_node (pid);
                                    };
                                  } (n.pid)
                                );
                    };
                node_map.fitBounds
                    (markers.getBounds(), { padding: [20,20], maxZoom: 15 });
              };
            });

        // make position editing more interesting...
        // ... by adding a map!
        $(document).ready(function() {
            var form="form[action *='node']";
            if ($(form).length) {

                var poslat="input[name='position.lat']";
                var poslon="input[name='position.lon']";

                var update_position = function(p) {
                    $(poslat).val(p[0]).trigger("change");
                    $(poslon).val(p[1]).trigger("change");
                    }
                var marker;
                var show_marker = function() {
                    // show a marker based on the position in the form

                    var degreeToFloat = function (s) {
                        // convert degrees, minutes, seconds to float
                        if (! s.match(/[^0-9. ]/)) {
                            return parseFloat(s) };
                        var dms= s.match(/([0-9]{2}).*?([0-9]{2}).*?([0-9.]+)/).slice(1)
                        dms = dms.map(function(x) { return parseFloat(x) });
                        return dms.reduce(function(x,y,i) { return x+(y/Math.pow(60,i)) });
                        };

                    // let's see whether we have positions
                    var lat = $(poslat).val();
                    var lon = $(poslon).val();

                    if (lat && lon) {
                        lat=degreeToFloat(lat);
                        lon=degreeToFloat(lon);
                        if (marker == undefined) {
                            marker = L.marker([lat,lon],
                                    {"draggable": true})
                                    .addTo(position_map)
                                    .on("dragend", function(e) {
                                        var ll=e.target._latlng;
                                        update_position([ll.lat,ll.lng]);
                                        });
                                    }
                        else {
                            marker.setLatLng([lat, lon])
                                .update();
                            }
                        position_map.setView([lat,lon],
                            Math.max(position_map.getZoom(),15));
                        }
                    };

                var field = $(poslat).parent().parent();

                // let's restructure the Dom for a bit!
                var d = $("div",field);
                //$("div",field).detach();
                field.append("<div class='pure-g'></div>");
                $("div:last",field).append("<div id='posfields' class='pure-u-1 pure-u-md-1-2'></div>");
                d.appendTo($("#posfields"));
                $("div > div:first",field).append("<div class='Field pure-control-group'>" +
                    "<label></label>" +
                    "<button name='geolocate' class='pure-button' id='geolocate'>" +
                    "<i class='fa fa-globe' title='geolocate address'></i>" +
                    "</button>");
                $("div.pure-g",field).append("<div class='map pure-u-1 pure-u-md-1-2' id='position-map'></div>");

                // add and initialize the map
                L.Icon.Default.imagePath = "/media/GTW/css/images";
                var position_map= L.map('position-map',
                                    {"doubleClickZoom": false})
                                    .setView([48.2083537,16.3725042],10)
                                    .on("dblclick", function(e) {
                                        var ll = e.latlng;
                                        update_position([ll.lat,ll.lng]);
                                        });


                L.tileLayer ( 'https://\{s\}.tile.openstreetmap.org/\{z\}/\{x\}/\{y\}.png'
                            , { maxZoom: 18
                            , attribution: 'Map data &copy; ' +
                              '<a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
                              '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
                               }
                ).addTo (position_map);


                // show marker on load
                show_marker();

                //bind change in input fields to show marker
                $("input[name *='position.']").on("change",function() { show_marker()});
                $("button#geolocate").on("click", function() {
                    $("button#geolocate").addClass("pure-button-disabled");
                    var fields=["street","city","country"];
                    var address = fields.map(function(x) {
                        return $("input[name='"+x+"']").val() }).join(", ");
                    $.getJSON("http://nominatim.openstreetmap.org/search/?q='"+
                        address+"'&format=json",
                        function(d) {
                            if (d.length) {
                                var lat;
                                var lon;
                                var p = d.filter(function(x) {
                                    return x.class == "place";
                                    });
                                if (p.length) {
                                    lat = p[0].lat;
                                    lon = p[0].lon;
                                    }
                                else {
                                    lat = d[0].lat;
                                    lon = d[0].lon;
                                    }
                                update_position([lat,lon]);
                                };
                            $("button#geolocate").removeClass("pure-button-disabled");
                            })
                    return false;
                    });

                }

            });

        return this;
    };
  } (jQuery)
);

// __END__ html/dashboard/app.js
