// Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
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
//    ««revision-date»»···
//--

;( function ($) {
    "use strict";
    $.fn.cndb_dashboard = function cndb_dashboard (opts) {
        var selectors = $.extend
            ( { app_div          : "[id^=\"app-D:\"]"
              , app_div_edit     : "[id=\"app-D:edit\"]"
              , create_button    : "[href=#create]"
              , create_button_p  : "[href=#create-partial]"
              , create_button_t  : "[href=#create-type]"
              , delete_button    : "[href=#delete]"
              , edit_button      : "[href=#edit]"
              , filter_button    : "[href=#filter]"
              , firmware_button  : "[href=#firmware]"
              , graph_button     : "[href=#graphs]"
              , graph_button_if  : ".interface-table [href=#graphs]"
              , graph_button_node: ".node-table [href=#graphs]"
              , obj_row          : "tr"
              , root             : "#app"
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
              }
            , opts || {}
            , { selectors : selectors
              , urls      : urls
              }
            );
        var active_filters = {};
        var nodes={};
        var pat_div_name   = new RegExp (options.app_div_prefix + "(\\w+)$");
        var pat_pid        = new RegExp ("^([^-]+)-(\\d+)$");
        var pat_typ_name   = new RegExp (options.app_typ_prefix + "(\\w+)$");
        var closest_el     = function closest_el (self, selector) {
            return $(self).closest (selector);
        };
        var closest_el_id = function closest_el_id (self, selector) {
            return $(self).closest (selector).prop ("id");
        };
        var create_cb = function create_cb (ev, sub_typ) {
            var afs   = $.param       (active_filters);
            var sid   = closest_el_id (this, "section");
            var typ   = sid.match     (pat_typ_name) [1];
            var midd  = (! sub_typ) ? "" : ("/" + sub_typ);
            var url   = options.urls.page + typ + midd + "/create";
            if (afs.length > 0) {
                url   = url + "?" + afs;
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
            var target$ = $(ev.delegateTarget);
            var menu$   = target$.next ();
            if (menu$.is (":visible")) {
                menu$.hide ();
            } else {
                menu$.show ();
            };
            return false;
        };
        var create_t_cb = function create_t_cb (ev) {
            var target$ = $(ev.target);
            var sub_typ = target$.data ("etn");
            var menu$   = target$.closest (".partial-type-menu");
            menu$.hide ();
            return create_cb.call (this, ev, sub_typ);
        };
        var delete_cb = function delete_cb (ev) {
            var obj   = obj_of_row (this);
            var success_cb = function success_cb (response, status) {
                var cs  = $("td", obj.row$).length;
                if (! response ["error"]) {
                    obj.row$.html
                        ( "<td class=\"feedback\" colspan=\"" + cs + "\">"
                        + (  response.html
                          || response.replacement
                          || "Deleted"
                          )
                        + "</td>"
                        );
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
        var do_filter = function do_filter (ev) {
            var id    = closest_el_id (this, selectors.obj_row);
            var all   = obj_rows_selector_all (id);
            var sel   = obj_rows_selector_sel (id);
            $(all).hide ();
            $(sel).show ();
        };
        var filter_cb = function filter_cb (ev) {
            var a$      = $(this);
            var id      = closest_el_id         (this, selectors.obj_row);
            var pid     = pid_of_obj_id         (id);
            var typ     = type_of_obj_id        (id);
            var all     = obj_rows_selector_all (id);
            var typ_cb  = filter_typ_cb [typ];
            var hide$;
            if (a$.hasClass (options.active_button_class)) {
                // currently filtered --> show all instances
                $(all).show ();
                delete active_filters [typ];
                a$.removeClass(options.active_button_class);
            } else {
                active_filters [typ] = pid;
                if (typ_cb) {
                    typ_cb.apply (this, arguments);
                };
                a$.addClass (options.active_button_class);
            };
            // execute all filters that are active now
            hide$ = $(selectors.filter_active_button);
            hide$.each (do_filter);
            return false;
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
                window.open (url).focus ();
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
        var hide_feedback = function hide_feedback (ev) {
            var target$ = $(ev.target);
            target$.remove ();
            return false;
        };
        var obj_of_row  = function obj_of_row (self) {
            var result  = {};
            var row$    = closest_el       (self, selectors.obj_row)
            result.row$ = row$;
            result.rid  = row$.prop        ("id");
            result.pid  = pid_of_obj_id    (result.rid);
            result.sid  = closest_el_id    (self, "section");
            result.typ  = result.sid.match (pat_typ_name) [1];
            result.url  = options.urls.page + result.typ + "/" + result.pid;
            return result;
        };
        var obj_rows_selector_all = function obj_rows_selector_all (id) {
            var typ = type_of_obj_id (id);
            return selectors.obj_row + "[class*=\"" + typ + "\"]";
        };
        var obj_rows_selector_sel = function obj_rows_selector_sel (id) {
            return selectors.obj_row + "[class~=\"" + id + "-\"]";
        };
        var pid_of_obj_id = function pid_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [2];
        };
        var type_of_obj_id = function type_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [1];
        };

        var focus_map_cb = function(e) {
            var id=$(e.target).parent().parent().parent().attr("class");
            var pid=id.match(/node-([0-9]+)-/)[1]
            if (nodes[pid]) {
                nodes[pid].openPopup();
                };
            };

        // Define custom actions on filter here
        var filter_typ_cb = {
            //interface : graph_interface_cb
            node: focus_map_cb,
        };

        selectors.filter_active_button =
            "." + options.active_button_class + selectors.filter_button;
        $(selectors.create_button    ).on ("click", create_cb);
        $(selectors.create_button_p  ).on ("click", create_p_cb);
        $(selectors.create_button_t  ).on ("click", create_t_cb);
        $(selectors.delete_button    ).on ("click", delete_cb);
        $(selectors.edit_button      ).on ("click", edit_cb);
        $(selectors.filter_button    ).on ("click", filter_cb);
        $(selectors.firmware_button  ).on ("click", firmware_cb);
        //$(selectors.graph_button_if  ).on ("click", graph_interface_cb);
        $(selectors.graph_button_node).on ("click", graph_cb);


        // initialize the map
        $(document).ready(function() {
            var ms = $(".map[data-markers]");
            L.Icon.Default.imagePath = "/media/GTW/css/images";
            for (var j=0;j<ms.length;j++) {
                var el = $(ms[j]);
                var node_data = JSON.parse(el.data("markers"));

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
                    nodes[n.pid] = L.marker([n.pos.lat, n.pos.lon])
                                    .addTo (markers)
                                    .bindPopup("<b>"+n.name+"</b>")
                                    .on("popupopen",
                                        function(p) {
                                            var pid = p;
                                            return function() {
                                                var sel = obj_rows_selector_sel ("node-"+pid);
                                                var all = obj_rows_selector_all ("node-"+pid);
                                                $("#node-"+pid+" a[href='#filter']")
                                                    .addClass(options.active_button_class);
                                                $(all).hide();
                                                $(sel).show();}}(n.pid)
                                        )
                                    .on("popupclose",
                                        function(p) {
                                            var pid=p;
                                            return function() {
                                                $("#node-"+pid+" a[href='#filter']")
                                                    .removeClass(options.active_button_class);
                                                var all = obj_rows_selector_all ("node-"+pid);
                                                $(all).show();}}(n.pid)
                                         );
                    };
                node_map.fitBounds(markers.getBounds(),
                    {padding: [20,20]
                    , maxZoom: 15});
                    };
            });
        
        // make position editing more interesting...
        // ... by adding a map!
        $(document).ready(function() {
            var form="form[action *='node']";
            if ($(form).length) {
                
                var poslat="input[name='position.lat']";
                var poslon="input[name='position.lon']";
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
                        console.log([lat,lon]);
                        if (marker == undefined) {  
                            marker = L.marker([lat,lon],
                                    {"draggable": true})
                                    .addTo(position_map)
                                    .on("dragend", function(e) {
                                        var ll=e.target._latlng;
                                        $(poslat).val(ll.lat);
                                        $(poslon).val(ll.lng);
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
                $("div",field).remove();
                field.append("<div class='pure-g-r'></div>");
                $("div",field).append("<div class='pure-u-1-2'></div>");
                $("div > div",field).append(d);
                $("div.pure-g-r",field).append("<div class='map pure-u-1-2' id='position-map'></div>");

                // add and initialize the map
                L.Icon.Default.imagePath = "/media/GTW/css/images";
                var position_map= L.map('position-map',
                                    {"doubleClickZoom": false})
                                    .setView([48.2083537,16.3725042],10)
                                    .on("dblclick", function(e) {
                                        var ll = e.latlng;
                                        $(poslat).val(ll.lat);
                                        $(poslon).val(ll.lng);
                                        show_marker();
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

                }

            });

        return this;
    };
  } (jQuery)
);

// __END__ html/dashboard/app.js
