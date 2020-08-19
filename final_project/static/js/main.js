//==================================================
// global constants
//==================================================
const ALERT_CONTAINER_COMP_CLASS = "alert_at_func";
const ALERT_MESSAGE_COMP_CLASS = "alert_at_func_message";
const LOADING_MODAL_ID = "loading_modal";
//==================================================
// global variables
//==================================================
var LOADING_COUNT = 0;
//==================================================
// function implementation
//==================================================
//--------------------------------------------------
// collapse toggler
//--------------------------------------------------
var get_collapse_toggler = function(toggled_id) {
    if (!toggled_id) {
        return null;
    }
    var togglers = $("[data-toggle='collapse']");
    if (togglers.length == 0) {
        return null;
    }
    var toggler = null;
    togglers.each(function() {
        var toggle_id = $(this).attr("href");
        if (!toggle_id) {
            return;
        }
        toggle_id = toggle_id.replace("#", "");
        if (toggled_id == toggle_id) {
            toggler = $(this);
            return false;
        }
    });
    return toggler;
}
var show_opened_collpase_toggler = function(toggled_id) {
    const toggler = get_collapse_toggler(toggled_id);
    if (!toggler) {
        return false;
    }
    var open_icon = toggler.children(".collapse-open");
    var close_icon = toggler.children(".collapse-close");
    if (!open_icon || !close_icon) {
        return false;
    }
    open_icon.css("display", "inline");
    close_icon.css("display", "none");
}
var show_closed_collapse_toggler = function(toggled_id) {
    const toggler = get_collapse_toggler(toggled_id);
    if (!toggler) {
        return false;
    }
    var open_icon = toggler.children(".collapse-open");
    var close_icon = toggler.children(".collapse-close");
    if (!open_icon || !close_icon) {
        return false;
    }
    open_icon.css("display", "none");
    close_icon.css("display", "inline");
}
var refresh_collapse_toggler = function() {
    var togglers = $("[data-toggle='collapse']");
    if (togglers.length == 0) {
        return;
    }
    togglers.each(function(index) {
        const collapse_href = $(this).attr("href");
        if (!collapse_href) {
            return;
        }
        const collapse_id = collapse_href.replace("#", "");
        if ($(this).hasClass("collapsed")) {
            show_closed_collapse_toggler(collapse_id);
        } else {
            show_opened_collpase_toggler(collapse_id);
        }
    });
}
var on_show_collapse_event = function(event) {
    const collapse_id = $(event.target).attr("id");
    show_opened_collpase_toggler(collapse_id);
}
var on_close_collpase_event = function(event) {
    const collapse_id = $(event.target).attr("id");
    show_closed_collapse_toggler(collapse_id);
}
//--------------------------------------------------
// loading modal
//--------------------------------------------------
var show_loading_modal = function() {
    $("#" + LOADING_MODAL_ID).modal("show");
    $("#" + LOADING_MODAL_ID).removeClass("hide_loading_modal");
}
var hide_loading_modal = function() {
    $("#" + LOADING_MODAL_ID).modal("hide");
    $("#" + LOADING_MODAL_ID).addClass("hide_loading_modal");
}
var trigger_show_loading_modal = function() {
    if (LOADING_COUNT == 0) {
        show_loading_modal();
    }
    LOADING_COUNT += 1;
}
var trigger_hide_loading_modal = function() {
    LOADING_COUNT -= 1;
    if (LOADING_COUNT == 0) {
        hide_loading_modal();
    }
}
$("#" + LOADING_MODAL_ID).on("shown.bs.modal", function (event) {
    if (LOADING_COUNT == 0) {
        hide_loading_modal();
    }
});
//--------------------------------------------------
// alert
//--------------------------------------------------
var warning = function(message) {
    toastr.error(message);
}
//==================================================
// initialization
//==================================================
// bind collapse toggler to switch icon in different state
$(document).on("show.bs.collapse", ".collapse", function(event) {
    on_show_collapse_event(event);
});
// bind collapse toggler to switch icon in different state
$(document).on("hide.bs.collapse", ".collapse", function(event) {
    on_close_collpase_event(event);
});
refresh_collapse_toggler();
// settings of alert dialog
toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": true,
  "progressBar": true,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "swing",
  "showMethod": "show",
  "hideMethod": "hide"
}