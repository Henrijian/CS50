const ALERT_CONTAINER_COMP_CLASS = "alert_at_func";
const ALERT_MESSAGE_COMP_CLASS = "alert_at_func_message";

var alert_at = function(container, message) {
    var message_items = $(container).children("." + ALERT_CONTAINER_COMP_CLASS).find(" ." + ALERT_MESSAGE_COMP_CLASS);
    if (message_items.length == 0) {
        const alert_item = document.createElement("div");
        alert_item.classList.add("alert", "alert-danger", "alert-dismissible", "fade",  "show", ALERT_CONTAINER_COMP_CLASS);
        alert_item.setAttribute("role", "alert");
        container.insertBefore(alert_item, container.firstChild);

        const message_item = document.createElement("div");
        message_item.classList.add(ALERT_MESSAGE_COMP_CLASS);
        message_item.textContent = message;
        alert_item.appendChild(message_item);

        const dismiss_btn = document.createElement("button");
        dismiss_btn.classList.add("close");
        dismiss_btn.setAttribute("type", "button");
        dismiss_btn.setAttribute("data-dismiss", "alert");
        alert_item.appendChild(dismiss_btn);

        const dismiss_span = document.createElement("span");
        dismiss_span.textContent = "x";
        dismiss_btn.appendChild(dismiss_span);
    } else {
        message_items.get(0).textContent = message;
    }
}

var close_alert_at = function(container) {
    $(container).find("." + ALERT_CONTAINER_COMP_CLASS).alert("close");
}

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

$(".datepicker").datepicker(
{
    autoclose: true,
    disableTouchKeyboard: true,
    endDate: "0d",
    forceParse: true,
    format: "yyyy-mm-dd",
    immediateUpdates: true,
    multidate: false,
    orientation: "left bottom",
    startDate: "2000-01-01",
    templates: {
                    leftArrow: "<i class=\"fas fa-caret-left\"></i>",
                    rightArrow: "<i class=\"fas fa-caret-right\"></i>"
                },
    todayBtn: "linked",
    todayHighlight: true,
    toggleActive: true
});

// bind collapse toggler to switch icon in different state
$(document).on("show.bs.collapse", ".collapse", function(event) {
    on_show_collapse_event(event);
});

// bind collapse toggler to switch icon in different state
$(document).on("hide.bs.collapse", ".collapse", function(event) {
    on_close_collpase_event(event);
});

refresh_collapse_toggler();