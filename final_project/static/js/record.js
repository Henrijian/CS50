//==================================================
// global constants
//==================================================
const RECORD_CALENDAR_ID = "record_calendar";
const RECORD_CALENDAR_HEADER_ID = "record_calendar_header";
const BTN_RECORD_CALENDAR_PREV_ID = "btn_record_calendar_prev";
const BTN_RECORD_CALENDAR_TODAY_ID = "btn_record_calendar_today";
const BTN_RECORD_CALENDAR_NEXT_ID = "btn_record_calendar_next";
const MODAL_ADD_EXERCISE_ID = "modal_add_exercise";
const MODAL_ADD_MAX_WEIGHT_ID = "modal_add_max_weight";
const STRENGTH_MUSCLE_GROUP_SELECT_ID = "strength_muscle_group_select"
const STRENGTH_EXERCISE_SELECT_ID = "strength_exercise_select";
const MAX_WEIGHT_MUSCLE_GROUP_SELECT_ID = "max_weight_muscle_group_select";
const MAX_WEIGHT_EXERCISE_SELECT_ID = "max_weight_exercise_select";
const MAX_WEIGHT_INPUT_ID = "max_weight_input";
const EXERCISE_SETS_ID = "exercise_sets";
const CARDIO_EXERCISE_SELECT_ID = "cardio_exercise_select";
const CARDIO_EXERCISE_TIME_ID = "cardio_exercise_time";
const CARDIO_EXERCISE_HOURS_ID = "cardio_exercise_hrs";
const CARDIO_EXERCISE_MINUTES_ID = "cardio_exercise_mins";
const CARDIO_EXERCISE_SECONDS_ID = "cardio_exercise_secs";
const CARD_RECORD_EXERCISE_ID = "card_record_exercise";
const BTN_ADD_EXERCISE_ID = "btn_add_exercise";
const BTN_SAVE_EXERCISE_ID = "btn_save_exercise";
const BTN_APPEND_EXERCISE_RECORDS_ID = "btn_append_exercise_records";
const BTN_APPEND_EXERCISE_SETS_ID = "btn_append_exercise_sets";
const BTN_ADD_MAX_WEIGHT_ID = "btn_add_max_weight";
const BTN_SAVE_MAX_WEIGHT_ID = "btn_save_max_weight";
const BTN_APPEND_MAX_WEIGHT_RECORDS_ID = "btn_append_max_weight_records";
const STRENGTH_EXERCISE_TAB_ID = "strength_exercise_tab";
const CARDIO_EXERCISE_TAB_ID = "cardio_exercise_tab";
const STRENGTH_EXERCISE_TAB_PANE_ID = "strength_exercise_tab_pane";
const CARDIO_EXERCISE_TAB_PANE_ID = "cardio_exercise_tab_pane";
const EXERCISE_RECORDS_ID = "exercise_records";
const MAX_WEIGHT_RECORDS_ID = "max_weight_records";
const RECORD_DATE_ID = "record_date";
const DATEPICKER_RECORD_DATE_ID = "datepicker_record_date";
const BODY_WEIGHT_INPUT_ID = "body_weight_input";
const BODY_WEIGHT_EDIT_BUTTON_ID = "btn_edit_body_weight";
const BODY_WEIGHT_SAVE_BUTTON_ID = "btn_save_body_weight";
const MUSCLE_WEIGHT_INPUT_ID = "muscle_weight_input";
const MUSCLE_WEIGHT_EDIT_BUTTON_ID = "btn_edit_muscle_weight";
const MUSCLE_WEIGHT_SAVE_BUTTON_ID = "btn_save_muscle_weight";
const FAT_RATE_INPUT_ID = "fat_rate_input";
const FAT_RATE_EDIT_BUTTON_ID = "btn_edit_fat_rate";
const FAT_RATE_SAVE_BUTTON_ID = "btn_save_fat_rate";
const EXERCISE_EVENT_PREFIX = "exercise_event_";
//==================================================
// global variables
//==================================================
var RECORD_CALENDAR = null;
//==================================================
// functions implementation
//==================================================
//--------------------------------------------------
// general
//--------------------------------------------------
var get_record_date = function() {
    const input_exercise_date = $("#" + RECORD_DATE_ID).get(0);
    if (!input_exercise_date) {
        return null;
    }
    return input_exercise_date.value;
}
var refresh_all_record_data = function(record_date) {
    const exercise_records_container = document.getElementById(EXERCISE_RECORDS_ID);
    if (!exercise_records_container) {
        console.log("exercise records container does not exist");
        return false;
    }
    const max_weight_records_container = document.getElementById(MAX_WEIGHT_RECORDS_ID);
    if (!max_weight_records_container) {
        console.log("max weight records container does not exist");
        return false;
    }

    $.ajax({
        url: "/api/get_record_html",
        type: "POST",
        data: {record_date: record_date},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                // Update exercise records
                const exercise_records_html = result["exercise_records_html"];
                initialize_exercise_records();
                exercise_records_container.innerHTML = exercise_records_html;
                refresh_collapse_toggler();
                // Update max weight records
                const max_weight_records_html = result["max_weight_records_html"];
                initialize_max_weight_records();
                max_weight_records_container.innerHTML = max_weight_records_html;
                // Update body record
                initialize_body_weight_input();
                const body_weight = result["body_weight"];
                $("#" + BODY_WEIGHT_INPUT_ID).val(body_weight);
                initialize_muscle_weight_input();
                const muscle_weight = result["muscle_weight"];
                $("#" + MUSCLE_WEIGHT_INPUT_ID).val(muscle_weight);
                initialize_fat_rate_input();
                const fat_rate = result["fat_rate"];
                $("#" + FAT_RATE_INPUT_ID).val(fat_rate);
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
//--------------------------------------------------
// exercise record
//--------------------------------------------------
var set_set_item_order = function(set_item, set_order) {
    if (!set_item) {
        return false;
    }
    if (set_order <= 0) {
        return false;
    }
    set_item.attr("set_order", set_order);
    set_item.find(".set_order_text").text(set_order);
}
var hide_add_exercise_button = function() {
    $("#" + BTN_ADD_EXERCISE_ID).removeClass("d-block");
    $("#" + BTN_ADD_EXERCISE_ID).addClass("d-none");
}
var show_add_exercise_button = function() {
    $("#" + BTN_ADD_EXERCISE_ID).removeClass("d-none");
    $("#" + BTN_ADD_EXERCISE_ID).addClass("d-block");
}
var hide_save_exercise_button = function() {
    $("#" + BTN_SAVE_EXERCISE_ID).removeClass("d-block");
    $("#" + BTN_SAVE_EXERCISE_ID).addClass("d-none");
}
var show_save_exercise_button = function() {
    $("#" + BTN_SAVE_EXERCISE_ID).removeClass("d-none");
    $("#" + BTN_SAVE_EXERCISE_ID).addClass("d-block");
}
var initialize_exercise_modal = function() {
    // select first muscle group and first exercise
    const muscle_group_select = $("#" + STRENGTH_MUSCLE_GROUP_SELECT_ID);
    if (muscle_group_select.length == 0)
    {
        console.log("cannot get muscle group select");
        return false;
    }
    const first_muscle_group = muscle_group_select.children("option")[0];
    muscle_group_select.val(first_muscle_group.value).change();

    // clean up set items
    $("#" + EXERCISE_SETS_ID).empty();

    // initialize cardio exercise tab
    const cardio_exercise_select = $("#" + CARDIO_EXERCISE_SELECT_ID);
    const first_cardio_exercise = cardio_exercise_select.children("option")[0];
    cardio_exercise_select.val(first_cardio_exercise.value);

    // clean up time input
    $("#" + CARDIO_EXERCISE_TIME_ID).children("input").val("");
}
var initialize_add_exercise_modal = function() {
    initialize_exercise_modal();

    // hide save button
    hide_save_exercise_button();

    // show add button
    show_add_exercise_button();
}
var initialize_edit_exercise_modal = function(record_details_id) {
    initialize_exercise_modal();

    // show save button
    show_save_exercise_button();

    // hide add button
    hide_add_exercise_button();

    const save_button = document.getElementById(BTN_SAVE_EXERCISE_ID);
    if (!save_button) {
        console.log("cannot find save button");
        return false;
    }
    save_button.setAttribute("onclick", "save_edit_exercise_modal(" + record_details_id + ")");
}
var show_strength_edit_exercise_modal = function(record_details_id, muscle_group, exercise_name, exercise_sets) {
    initialize_edit_exercise_modal(record_details_id);
    // select strength tab
    $("#" + STRENGTH_EXERCISE_TAB_ID).tab("show");
    // update muscle group
    const muscle_group_select = document.getElementById(STRENGTH_MUSCLE_GROUP_SELECT_ID);
    if (!muscle_group_select) {
        console.log("cannot get strength muscle group select");
        return false;
    }
    $(muscle_group_select).val(muscle_group);
    // update exercise
    const exercise_select = document.getElementById(STRENGTH_EXERCISE_SELECT_ID);
    if (!exercise_select) {
        console.log("cannot get strength exercise select");
        return false;
    }
    $.ajax({
        url: "/api/get_muscle_group_exercises",
        type: "GET",
        data: {muscle_group: muscle_group},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const exercise_ids_names = $.parseJSON(data["result"]);
                $(exercise_select).empty();
                var exercise_id = -1;
                $.each(exercise_ids_names, function(index, value) {
                    const exercise_option = document.createElement("option");
                    exercise_option.setAttribute("value", value[0]);
                    exercise_option.textContent = value[1];
                    if (value[1] == exercise_name) {
                        exercise_id = value[0];
                    }
                    exercise_select.append(exercise_option);
                });
                if (exercise_id <= 0) {
                    warning("Exercise does not exist");
                    return false;
                }
                $(exercise_select).val(exercise_id);
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
    // update exercise sets
    const sets_container = document.getElementById(EXERCISE_SETS_ID);
    if (!sets_container) {
        console.log("cannot get exercise sets container");
        return false;
    }
    $.ajax({
        url: "/api/get_exercise_sets_html",
        type: "POST",
        data: {record_details_id: record_details_id},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_sets_html_string = result["exercise_sets_html"];
                const exercise_sets_element = $.parseHTML(exercise_sets_html_string);
                $(sets_container).append(exercise_sets_element);
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
    $("#" + MODAL_ADD_EXERCISE_ID).modal("show");
}
var show_cardio_edit_exercise_modal = function(record_details_id, exercise_name, exercise_hours, exercise_minutes, exercise_seconds) {
    initialize_edit_exercise_modal(record_details_id);
    // select strength tab
    $("#" + CARDIO_EXERCISE_TAB_ID).tab("show");
    // update exercise
    const exercise_select = document.getElementById(CARDIO_EXERCISE_SELECT_ID);
    if (!exercise_select) {
        console.log("cannot get cardio exercise select");
        return false;
    }
    $(exercise_select).children("option").each(function() {
        if ($(this).html() == exercise_name) {
            $(exercise_select).val($(this).val());
            return false;
        }
    });
    // update exercise hours
    const exercise_hours_input = document.getElementById(CARDIO_EXERCISE_HOURS_ID);
    if (!exercise_hours_input) {
        console.log("cannot get exercise_hours_input");
        return false;
    }
    exercise_hours_input.value = exercise_hours;
    // update exercise minutes
    const exercise_minutes_input = document.getElementById(CARDIO_EXERCISE_MINUTES_ID);
    if (!exercise_minutes_input) {
        console.log("cannot get exercise_minutes_input");
        return false;
    }
    exercise_minutes_input.value = exercise_minutes;
    // update exercise seconds
    const exercise_seconds_input = document.getElementById(CARDIO_EXERCISE_SECONDS_ID);
    if (!exercise_seconds_input) {
        console.log("cannot get exercise_seconds_input");
        return false;
    }
    exercise_seconds_input.value = exercise_seconds;
    $("#" + MODAL_ADD_EXERCISE_ID).modal("show");
}
var show_edit_exercise_modal = function(record_details_id) {
    // load edit exercise modal
    $.ajax({
        url: "/api/get_exercise_record",
        type: "POST",
        data: {record_details_id: record_details_id},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const record_details_id = result["record_details_id"];
                const exercise_type = result["exercise_type"];
                const muscle_group = result["muscle_group"];
                const exercise_name = result["exercise_name"];
                if (exercise_type == "strength") {
                    const exercise_sets = get_exercise_sets(result["exercise_sets"]);
                    show_strength_edit_exercise_modal(record_details_id, muscle_group, exercise_name, exercise_sets);
                } else if (exercise_type == "cardio") {
                    const exercise_time = result["exercise_time"];
                    const exercise_hours = exercise_time["hours"];
                    const exercise_minutes = exercise_time["minutes"];
                    const exercise_seconds = exercise_time["seconds"];
                    show_cardio_edit_exercise_modal(record_details_id, exercise_name, exercise_hours, exercise_minutes, exercise_seconds);
                } else {
                    console.log("unknown exercise type");
                }
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var save_edit_exercise_modal = function(record_details_id) {
    const strength_exercise_tab_active = $("#" + STRENGTH_EXERCISE_TAB_PANE_ID + ".active").length > 0;
    var exercise_id;
    var exercise_name;
    var exercise_sets;
    var exercise_sets = [];
    var exercise_hours;
    var exercise_minutes;
    var exercise_seconds;
    if (strength_exercise_tab_active) {
        // get exercise id
        const exercise_select = $("#" + STRENGTH_EXERCISE_SELECT_ID);
        if (exercise_select.length == 0) {
            console.log("exercise selector does not exist");
            return false;
        }
        exercise_id = $("#" + STRENGTH_EXERCISE_SELECT_ID).val();
        // get exercise_name
        exercise_name = $("#" + STRENGTH_EXERCISE_SELECT_ID + " :selected").text();
        // get strength exercise sets
        const exercise_set_items = $("#" + EXERCISE_SETS_ID).children(".exercise_set, .exercise_sub_set");
        if (exercise_set_items.length == 0) {
            warning("sets cannot be empty");
            return false;
        }
        exercise_set_items.each(function(index) {
            const order = $(this).attr("set_order");
            if (!order) {
                console.log("cannot get set order");
                return false;
            }

            // get weight of each set
            const weight_input = $(this).children("input.exercise_weight").get(0);
            if (!weight_input) {
                console.log("cannot get weight input");
                return false;
            }
            const weight = weight_input.value;

            // get repetitions of each set
            const reps_input = $(this).children("input.exercise_reps").get(0);
            if (!reps_input) {
                console.log("cannot get repetitions input");
                return false;
            }
            const reps = reps_input.value;

            exercise_sets.push({
                set_order: order,
                set_weight: weight,
                set_reps: reps,
            });
        });
    }
    else {
        // get exercise id
        const exercise_select = $("#" + CARDIO_EXERCISE_SELECT_ID);
        if (exercise_select.length == 0) {
            console.log("exercise selector does not exist");
            return false;
        }
        exercise_id = $("#" + CARDIO_EXERCISE_SELECT_ID).val();
        // get exercise_name
        exercise_name = $("#" + CARDIO_EXERCISE_SELECT_ID + " :selected").text();
        // get exercise hours
        exercise_hours = document.getElementById(CARDIO_EXERCISE_HOURS_ID).value;
        // get exercise minutes
        exercise_minutes = document.getElementById(CARDIO_EXERCISE_MINUTES_ID).value;
        // get exercise seconds
        exercise_seconds = document.getElementById(CARDIO_EXERCISE_SECONDS_ID).value;
    }
    if (!exercise_id) {
        console.log("cannot get exercise id");
        return false;
    }
    if (!exercise_name) {
        console.log("cannot get exercise name");
        return false;
    }
    // add exercise record to server
    $.ajax({
        url: "/api/edit_exercise_record",
        type: "POST",
        data: {"record_details_id": record_details_id,
               "exercise_id": exercise_id,
               "exercise_sets": JSON.stringify(exercise_sets),
               "exercise_hours": exercise_hours,
               "exercise_minutes": exercise_minutes,
               "exercise_seconds": exercise_seconds},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                refresh_exercise_records(get_record_date());
                $("#" + MODAL_ADD_EXERCISE_ID).modal("hide");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var initialize_exercise_records = function() {
    $("#" + EXERCISE_RECORDS_ID).empty();
}
var refresh_exercise_records = function(record_date) {
    const exercise_records_container = document.getElementById(EXERCISE_RECORDS_ID);
    if (!exercise_records_container) {
        console.log("exercise records container does not exist");
        return false;
    }

    initialize_exercise_records();
    // add exercise record to server
    $.ajax({
        url: "/api/get_exercise_records_html",
        type: "POST",
        data: {record_date: record_date},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_records_html = result["exercise_records_html"];
                exercise_records_container.innerHTML = exercise_records_html;
                refresh_collapse_toggler();
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var delete_exercise_record = function(record_details_id) {
    // delete exercise record to server
    $.ajax({
        url: "/api/delete_exercise_record",
        type: "POST",
        data: {"record_details_id": record_details_id},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                refresh_exercise_records(get_record_date());
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
// convert server exercise sets data to local exercise sets
var get_exercise_sets = function(exercise_sets_data) {
    if (!exercise_sets_data) {
        console.log("cannot deal with null exercise sets data");
        return [];
    }

    var exercise_sets = [];
    $.each(exercise_sets_data, function(i, set_data){
        const order = set_data["order"];
        const weight = set_data["weight"];
        const reps = set_data["reps"];
        exercise_sets.push({
            set_order: order,
            set_weight: weight,
            set_reps: reps,
        });
        const sub_sets = set_data["sub_sets"];
        $.each(sub_sets, function(j, sub_set_data) {
            const sub_order = sub_set_data["order"];
            const sub_weight = sub_set_data["weight"];
            const sub_reps = sub_set_data["reps"];
            exercise_sets.push({
                set_order: order,
                set_weight: sub_weight,
                set_reps: sub_reps,
            });
        });
    });
    return exercise_sets;
}
//--------------------------------------------------
// max weight record
//--------------------------------------------------
var hide_add_max_weight_button = function() {
    $("#" + BTN_ADD_MAX_WEIGHT_ID).removeClass("d-block");
    $("#" + BTN_ADD_MAX_WEIGHT_ID).addClass("d-none");
}
var show_add_max_weight_button = function() {
    $("#" + BTN_ADD_MAX_WEIGHT_ID).removeClass("d-none");
    $("#" + BTN_ADD_MAX_WEIGHT_ID).addClass("d-block");
}
var hide_save_max_weight_button = function() {
    $("#" + BTN_SAVE_MAX_WEIGHT_ID).removeClass("d-block");
    $("#" + BTN_SAVE_MAX_WEIGHT_ID).addClass("d-none");
}
var show_save_max_weight_button = function() {
    $("#" + BTN_SAVE_MAX_WEIGHT_ID).removeClass("d-none");
    $("#" + BTN_SAVE_MAX_WEIGHT_ID).addClass("d-block");
}
var initialize_max_weight_modal = function() {
    // select first muscle group and first exercise
    const muscle_group_select = $("#" + MAX_WEIGHT_MUSCLE_GROUP_SELECT_ID);
    if (muscle_group_select.length == 0)
    {
        console.log("cannot get max weight muscle group select");
        return false;
    }
    const first_muscle_group = muscle_group_select.children("option")[0];
    muscle_group_select.val(first_muscle_group.value).change();

    // clean up max weight input
    $("#" + MAX_WEIGHT_INPUT_ID).val("");
}
var initialize_add_max_weight_modal = function() {
    initialize_max_weight_modal();

    // hide save button
    hide_save_max_weight_button();

    // show add button
    show_add_max_weight_button();
}
var initialize_edit_max_weight_modal = function(max_weight_record_id) {
    initialize_max_weight_modal();

    // hide add button
    hide_add_max_weight_button();

    // show save button
    show_save_max_weight_button();

    const save_button = document.getElementById(BTN_SAVE_MAX_WEIGHT_ID);
    if (!save_button) {
        console.log("cannot find save button");
        return false;
    }
    save_button.setAttribute("onclick", "save_edit_max_weight_modal(" + max_weight_record_id + ")");
}
var show_edit_max_weight_modal = function(max_weight_record_id) {
    // initialize modal
    initialize_edit_max_weight_modal(max_weight_record_id);
    // load edit max weight modal
    $.ajax({
        url: "/api/get_max_weight_record",
        type: "POST",
        data: {max_weight_record_id: max_weight_record_id},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const max_weight_record = result["max_weight_record"];
                const muscle_group = max_weight_record["muscle_group"];
                const exercise_id = max_weight_record["exercise_id"];
                const exercise_name = max_weight_record["exercise_name"];
                const max_weight = max_weight_record["max_weight"];
                // update muscle group
                const muscle_group_select = document.getElementById(MAX_WEIGHT_MUSCLE_GROUP_SELECT_ID);
                if (!muscle_group_select) {
                    console.log("cannot get max weight muscle group select");
                    return false;
                }
                $(muscle_group_select).val(muscle_group);
                // update exercise
                const exercise_select = document.getElementById(MAX_WEIGHT_EXERCISE_SELECT_ID);
                if (!exercise_select) {
                    console.log("cannot get max weight exercise select");
                    return false;
                }
                $.ajax({
                    url: "/api/get_muscle_group_exercises",
                    type: "GET",
                    data: {muscle_group: muscle_group},
                    dataType: "json",
                    beforeSend:function() {
                        trigger_show_loading_modal();
                    },
                    success:function(data) {
                        if (data["error_code"] == 0) {
                            const exercise_ids_names = $.parseJSON(data["result"]);
                            $(exercise_select).empty();
                            $.each(exercise_ids_names, function(index, value) {
                                const exercise_option = document.createElement("option");
                                exercise_option.setAttribute("value", value[0]);
                                exercise_option.textContent = value[1];
                                exercise_select.append(exercise_option);
                            });
                            $(exercise_select).val(exercise_id);
                        } else {
                            warning(data["error_message"]);
                        }
                    },
                    complete:function() {
                        trigger_hide_loading_modal();
                    }
                });
                // update max weight input
                const max_weight_input = document.getElementById(MAX_WEIGHT_INPUT_ID);
                if (!max_weight_input) {
                    console.log("max weight input does not exist");
                    return false;
                }
                $(max_weight_input).val(max_weight);
                // show edit max weight modal
                $("#" + MODAL_ADD_MAX_WEIGHT_ID).modal("show");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var save_edit_max_weight_modal = function(max_weight_record_id) {
    // get exercise id
    const exercise_select = document.getElementById(MAX_WEIGHT_EXERCISE_SELECT_ID);
    if (!exercise_select) {
        warning("cannot get exercise");
        return false;
    }
    const exercise_id = $(exercise_select).val();
    if (!exercise_id) {
        warning("cannot get exercise id");
        return false;
    }
    // get max weight
    const max_weight_input = document.getElementById(MAX_WEIGHT_INPUT_ID);
    if (!max_weight_input) {
        warning("cannot get max weight");
        return false;
    }
    const max_weight = $(max_weight_input).val();
    if (!max_weight) {
        warning("cannot get max weight");
        return false;
    }
    // add max weight record to server
    $.ajax({
        url: "/api/edit_max_weight_record",
        type: "POST",
        data: {"max_weight_record_id": max_weight_record_id,
               "exercise_id": exercise_id,
               "max_weight": max_weight},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                refresh_max_weight_records(get_record_date());
                $("#" + MODAL_ADD_MAX_WEIGHT_ID).modal("hide");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var initialize_max_weight_records = function() {
    $("#" + MAX_WEIGHT_RECORDS_ID).empty();
}
var refresh_max_weight_records = function(record_date) {
    const max_weight_records_container = document.getElementById(MAX_WEIGHT_RECORDS_ID);
    if (!max_weight_records_container) {
        console.log("max weight records container does not exist");
        return false;
    }

    initialize_max_weight_records();
    $.ajax({
        url: "/api/get_max_weight_records_html",
        type: "POST",
        data: {record_date: record_date},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const max_weight_records_html = result["max_weight_records_html"];
                max_weight_records_container.innerHTML = max_weight_records_html;
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var delete_max_weight_record = function(max_weight_record_id) {
    // delete exercise record in server
    $.ajax({
        url: "/api/delete_max_weight_record",
        type: "POST",
        data: {"max_weight_record_id": max_weight_record_id},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                refresh_max_weight_records(get_record_date());
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
//--------------------------------------------------
// body weight record
//--------------------------------------------------
var initialize_body_weight_input = function() {
    $("#" + BODY_WEIGHT_INPUT_ID).val("");
}
//--------------------------------------------------
// fat rate record
//--------------------------------------------------
var initialize_fat_rate_input = function() {
    $("#" + FAT_RATE_INPUT_ID).val("");
}
//--------------------------------------------------
// muscle weight record
//--------------------------------------------------
var initialize_muscle_weight_input = function() {
    $("#" + MUSCLE_WEIGHT_INPUT_ID).val("");
}
//--------------------------------------------------
// date picker
//--------------------------------------------------
var initialize_datepicker = function(initial_date_str) {
    $("#" + RECORD_DATE_ID).datepicker("destroy");
    $("#" + RECORD_DATE_ID).datepicker({
        autoclose: true,
        disableTouchKeyboard: true,
        endDate: initial_date_str,
        forceParse: true,
        format: "yyyy-mm-dd",
        immediateUpdates: true,
        multidate: false,
        orientation: "left bottom",
        startDate: "2000-01-01",
        templates: {
            leftArrow: "<i class=\"fas fa-caret-left\"></i>",
            rightArrow: "<i class=\"fas fa-caret-right\"></i>"},
        todayBtn: "linked",
        todayHighlight: true,
        toggleActive: false
    });
}

//--------------------------------------------------
// record calendar
//--------------------------------------------------
var disable_record_calendar_prev_button = function() {
    $("#" + BTN_RECORD_CALENDAR_PREV_ID).attr("disabled", true);
}
var enable_record_calendar_prev_button = function() {
    $("#" + BTN_RECORD_CALENDAR_PREV_ID).attr("disabled", false);
}
var disable_record_calendar_next_button = function() {
    $("#" + BTN_RECORD_CALENDAR_NEXT_ID).attr("disabled", true);
}
var enable_record_calendar_next_button = function() {
    $("#" + BTN_RECORD_CALENDAR_NEXT_ID).attr("disabled", false);
}
var disable_record_calendar_today_button = function() {
    $("#" + BTN_RECORD_CALENDAR_TODAY_ID).attr("disabled", true);
}
var enable_record_calendar_today_button = function() {
    $("#" + BTN_RECORD_CALENDAR_TODAY_ID).attr("disabled", false);
}
var refresh_calendar_exercise_events_between = function(start_date, end_date) {
    // clear exercise events first
    var exercise_events = RECORD_CALENDAR.getEvents();
    $.each(exercise_events, function(index, exercise_event) {
        if (exercise_event.id.startsWith(EXERCISE_EVENT_PREFIX)){
            exercise_event.remove();
        }
    });
    // load exercise events
    $.ajax({
        url: "/api/get_exercise_dates",
        type: "GET",
        data: {
            start_year: start_date.getFullYear(),
            start_month: start_date.getMonth() + 1,
            start_date: start_date.getDate(),
            end_year: end_date.getFullYear(),
            end_month: end_date.getMonth() + 1,
            end_date: end_date.getDate()
        },
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                var exercise_dates = $.parseJSON(data["result"]);
                $.each(exercise_dates, function(index, value) {
                    RECORD_CALENDAR.addEvent({
                        id: EXERCISE_EVENT_PREFIX + value,
                        start: value,
                        allDay: true
                    });
                });
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
}
var refresh_record_calendar = function() {
    const start_date = RECORD_CALENDAR.view.activeStart;
    const end_date = RECORD_CALENDAR.view.activeEnd;
    refresh_calendar_exercise_events_between(start_date, end_date);
    RECORD_CALENDAR.select(get_record_date());
}
var initialize_record_calendar = function(initial_date_str) {
    const record_calendar_element = document.getElementById(RECORD_CALENDAR_ID);
    RECORD_CALENDAR = new FullCalendar.Calendar(record_calendar_element, {
        bootstrapFontAwesome: {
            prev: 'fa-chevron-left',
            next: 'fa-chevron-right'
        },
        dateClick: function(info) {
            const today = new Date();
            const clicked_date_str = info.dateStr;
            const clicked_date = new Date(clicked_date_str);
            if (clicked_date.setHours(0,0,0,0) <= today.setHours(0,0,0,0)) {
                RECORD_CALENDAR.select(clicked_date_str);
            }
        },
        eventClick: function(eventClickInfo) {
            const today = new Date();
            const clicked_date_str = eventClickInfo.event.startStr;
            const clicked_date = new Date(clicked_date_str);
            if (clicked_date.setHours(0,0,0,0) <= today.setHours(0,0,0,0)) {
                RECORD_CALENDAR.select(clicked_date_str);
            }
        },
        eventContent: {
            html: "<span class=\"badge badge-danger\"><i class=\"fas fa-fire-alt\"></i><span class=\"d-none d-lg-inline\">workout</span></span>"
        },
        eventColor: 'transparent',
        datesSet: function(dateInfo) {
            // refresh header
            $("#" + RECORD_CALENDAR_HEADER_ID).text(dateInfo.view.title);
            // refresh buttons
            const today = new Date();
            const start_date = dateInfo.start;
            const end_date = dateInfo.end;
            if (today.setHours(0,0,0,0) < end_date.setHours(0,0,0,0)) {
                disable_record_calendar_next_button();
            } else {
                enable_record_calendar_next_button();
            }
            if (start_date.setHours(0,0,0,0) <= today.setHours(0,0,0,0) &&
                today.setHours(0,0,0,0) < end_date.setHours(0,0,0,0)) {
                disable_record_calendar_today_button();
            } else {
                enable_record_calendar_today_button();
            }
            // refresh events
            refresh_calendar_exercise_events_between(start_date, end_date);
            // refresh selected date
            const selected_date = new Date(get_record_date());
            if (start_date.setHours(0,0,0,0) <= selected_date.setHours(0,0,0,0) &&
                selected_date.setHours(0,0,0,0) < end_date.setHours(0,0,0,0)) {
                RECORD_CALENDAR.select(get_record_date());
            }
        },
        fixedWeekCount: false,
        headerToolbar: false,
        height: "auto",
        initialDate: initial_date_str,
        initialView: "dayGridMonth",
        select: function(selectionInfo) {
            const today = new Date();
            const selected_date_str = selectionInfo.startStr;
            const selected_date = new Date(selected_date_str);
            if (today.setHours(0,0,0,0) == selected_date.setHours(0,0,0,0)) {
                const tomorrow = new Date(today);
                tomorrow.setDate(tomorrow.getDate() + 1);
                $("#" + RECORD_DATE_ID).datepicker("setEndDate", tomorrow);
                $("#" + RECORD_DATE_ID).datepicker("update", selected_date);
                $("#" + RECORD_DATE_ID).datepicker("setEndDate", today);
            } else {
                $("#" + RECORD_DATE_ID).datepicker("update", selected_date);
            }
            // check whether refresh calendar view
            const view_start_date = RECORD_CALENDAR.view.activeStart;
            const view_end_date = RECORD_CALENDAR.view.activeEnd;
            if (selected_date.setHours(0,0,0,0) < view_start_date.setHours(0,0,0,0) ||
                view_end_date.setHours(0,0,0,0) <= selected_date.setHours(0,0,0,0)) {
                RECORD_CALENDAR.gotoDate(selectionInfo.start);
            }
            refresh_all_record_data(selected_date_str);
        },
        showNonCurrentDates: false,
        themeSystem: "bootstrap",
        timeZone: 'local',
        unselectAuto: false
    });
    RECORD_CALENDAR.render();
    RECORD_CALENDAR.select(initial_date_str);
}

//==================================================
// event binding
//==================================================
//--------------------------------------------------
// record calendar - components
//--------------------------------------------------
$("#" + BTN_RECORD_CALENDAR_PREV_ID).on("click", function() {
    RECORD_CALENDAR.prev();
});
$("#" + BTN_RECORD_CALENDAR_NEXT_ID).on("click", function() {
    RECORD_CALENDAR.next();
});
$("#" + BTN_RECORD_CALENDAR_TODAY_ID).on("click", function() {
    RECORD_CALENDAR.today();
});
//--------------------------------------------------
// datepicker - components
//--------------------------------------------------
// datepicker onChangeDate event
$("#" + RECORD_DATE_ID).datepicker().on("changeDate", function(e) {
    const record_date = e.format();
    refresh_all_record_data(record_date);
    RECORD_CALENDAR.select(record_date);
});
// muscle group selector onChange event
$("select.muscle_group_select").on("change", function() {
    var exercises_select_id = $(this).attr("muscle-group-exercises");
    if (!exercises_select_id) {

        return false;
    }
    var exercises_select = $("#" + exercises_select_id);
    if (!exercises_select) {
        return false;
    }
    $.ajax({
        url: "/api/get_muscle_group_exercises",
        type: "GET",
        data: {muscle_group: $(this).val()},
        dataType: "json",
        success:function( data ) {
            if (data["error_code"] == 0) {
                var exercise_ids_names = $.parseJSON(data["result"]);
                exercises_select.empty();
                $.each(exercise_ids_names, function(index, value) {
                    const exercise_option = document.createElement("option");
                    exercise_option.setAttribute("value", value[0]);
                    exercise_option.textContent = value[1];
                    exercises_select.append(exercise_option);
                });
            } else {
                warning(data["error_message"]);
            }
        }
    });
});
//--------------------------------------------------
// exercise record - components
//--------------------------------------------------
// append exercise button onClick event
$("#" + BTN_APPEND_EXERCISE_RECORDS_ID).on("click", function() {
    // get exercise date
    if (!get_record_date()) {
        warning("Must specify date");
        return false;
    }
    initialize_add_exercise_modal();
});
// add exercise button onClick event
$("#" + BTN_ADD_EXERCISE_ID).on("click", function() {
    const record_exercises = document.getElementById(EXERCISE_RECORDS_ID);
    if (!record_exercises) {
        console.log("exercise records container does not exist");
        return false;
    }
    // get active exercise tab
    const strength_tab_active = $("#" + STRENGTH_EXERCISE_TAB_PANE_ID + ".active").length > 0;
    // get exercise date
    const exercise_date = get_record_date();

    if (strength_tab_active) {
        // get exercise id
        const exercise_select = $("#" + STRENGTH_EXERCISE_SELECT_ID);
        if (exercise_select.length == 0) {
            console.log("exercise selector does not exist");
            return false;
        }
        const exercise_id = exercise_select.get(0).value;

        // get strength exercise sets
        var exercise_sets = [];
        const exercise_set_items = $("#" + EXERCISE_SETS_ID).children(".exercise_set, .exercise_sub_set");
        if (exercise_set_items.length == 0) {
            warning("sets cannot be empty");
            return false;
        }
        exercise_set_items.each(function(index) {
            const order = $(this).attr("set_order");
            if (!order) {
                console.log("cannot get set order");
                return false;
            }

            // get weight of each set
            const weight_input = $(this).children("input.exercise_weight").get(0);
            if (!weight_input) {
                console.log("cannot get weight input");
                return false;
            }
            const weight = weight_input.value;

            // get repetitions of each set
            const reps_input = $(this).children("input.exercise_reps").get(0);
            if (!reps_input) {
                console.log("cannot get repetitions input");
                return false;
            }
            const reps = reps_input.value;

            exercise_sets.push({
                set_order: order,
                set_weight: weight,
                set_reps: reps,
            });
        });

        // add exercise record to server
        $.ajax({
            url: "/api/append_strength_exercise_records",
            type: "POST",
            data: {exercise_date: exercise_date,
                   exercise_id: exercise_id,
                   exercise_sets: JSON.stringify(exercise_sets)},
            dataType: "json",
            beforeSend:function() {
                trigger_show_loading_modal();
            },
            success:function(data) {
                refresh_exercise_records(exercise_date);
                refresh_record_calendar();
                $("#" + MODAL_ADD_EXERCISE_ID).modal('hide');
            },
            complete:function() {
                trigger_hide_loading_modal();
            }
        });
    } else {
        // get exercise id
        const exercise_select = $("#" + CARDIO_EXERCISE_SELECT_ID);
        if (exercise_select.length == 0) {
            console.log("exercise selector does not exist");
            return false;
        }
        const exercise_id = exercise_select.get(0).value;

        // get exercise hours
        const exercise_hours = document.getElementById(CARDIO_EXERCISE_HOURS_ID).value;
        // get exercise minutes
        const exercise_minutes = document.getElementById(CARDIO_EXERCISE_MINUTES_ID).value;
        // get exercise seconds
        const exercise_seconds = document.getElementById(CARDIO_EXERCISE_SECONDS_ID).value;

        // add exercise record to server
        $.ajax({
            url: "/api/append_cardio_exercise_records",
            type: "POST",
            data: {exercise_date: exercise_date,
                   exercise_id: exercise_id,
                   exercise_hours: exercise_hours,
                   exercise_minutes: exercise_minutes,
                   exercise_seconds: exercise_seconds},
            dataType: "json",
            beforeSend:function() {
                trigger_show_loading_modal();
            },
            success:function(data) {
                refresh_exercise_records(exercise_date);
                refresh_record_calendar();
                $("#" + MODAL_ADD_EXERCISE_ID).modal('hide');
            },
            complete:function() {
                trigger_hide_loading_modal();
            }
        });
    }
});
// add exercise set button onClick event
$("#" + BTN_APPEND_EXERCISE_SETS_ID).on("click", function() {
    const sets_container = $("#" + EXERCISE_SETS_ID).get(0);
    if (!sets_container) {
        console.log("cannot get sets container");
        return false;
    }
    const sets_count = $(sets_container).children(".exercise_set").length;
    const set_order = sets_count + 1;
    // get exercise set element
    $.ajax({
        url: "/api/get_exercise_set_html",
        type: "GET",
        data: {set_order: set_order,
               set_weight: 0,
               set_reps: 0,
               is_sub_set: false},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_set_html_string = result["exercise_set_html"];
                const exercise_set_element = $.parseHTML(exercise_set_html_string);
                $(sets_container).append(exercise_set_element);
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});
// add exercise sub set button onClick event
$(document).on("click", ".btn_add_sub_set", function() {
    var set_item = $(this).parents(".exercise_set, .exercise_sub_set").get(0);
    if (!set_item) {
        console.log("cannot get exercise set item");
        return false;
    }
    const set_order = set_item.getAttribute("set_order");
    // get exercise set element
    $.ajax({
        url: "/api/get_exercise_set_html",
        type: "GET",
        data: {set_order: set_order,
               set_weight: 0,
               set_reps: 0,
               is_sub_set: true},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_set_html_string = result["exercise_set_html"];
                const exercise_set_element = $.parseHTML(exercise_set_html_string);
                $(set_item).after(exercise_set_element);
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});
// delete exercise sub set button onClick event
$(document).on("click", ".btn_delete_sub_set", function() {
    var sub_set_item = $(this).parents(".exercise_sub_set").get(0);
    if (!sub_set_item) {
        console.log("cannot get exercise sub set item")
        return false;
    }
    sub_set_item.remove();
});
// delete exercise set button onClick event
$(document).on("click", ".btn_delete_set", function() {
    var set_item = $(this).parents(".exercise_set").get(0);
    if (!set_item) {
        console.log("cannot get exercise set item")
        return false;
    }
    const set_order_str = set_item.getAttribute("set_order");
    const set_order = parseInt(set_order_str, 10);

    // remove sub set items
    $(set_item).siblings("[set_order='" + set_order_str + "']").remove();

    // update set order after currently deleted set order
    const set_items = $(set_item).siblings(".exercise_set, .exercise_sub_set");
    set_items.each(function() {
        const each_set_order = parseInt($(this).attr("set_order"), 10);
        if (each_set_order > set_order) {
            set_set_item_order($(this), each_set_order - 1);
        }
    });
    $(set_item).remove();
});
//--------------------------------------------------
// max weight record - components
//--------------------------------------------------
// append max weight button onClick event
$("#" + BTN_APPEND_MAX_WEIGHT_RECORDS_ID).on("click", function() {
    // get exercise date
    if (!get_record_date()) {
        warning("Must specify date");
        return false;
    }
    initialize_add_max_weight_modal();
});
// add max weight button onClick event
$("#" + BTN_ADD_MAX_WEIGHT_ID).on("click", function() {
    const max_weight_records = document.getElementById(MAX_WEIGHT_RECORDS_ID);
    if (!max_weight_records) {
        console.log("max weight records container does not exist");
        return false;
    }
    // get exercise date
    const exercise_date = get_record_date();
    // get exercise id
    const exercise_select = document.getElementById(MAX_WEIGHT_EXERCISE_SELECT_ID);
    if (!exercise_select) {
        console.log("exercise selector does not exist");
        return false;
    }
    const exercise_id = exercise_select.value;
    // get max weight
    const max_weight_input = document.getElementById(MAX_WEIGHT_INPUT_ID);
    if (!max_weight_input) {
        console.log("max weight input does not exist");
        return false;
    }
    const max_weight = max_weight_input.value;
    // add exercise record to server
    $.ajax({
        url: "/api/append_max_weight_records",
        type: "POST",
        data: {exercise_date: exercise_date,
               exercise_id: exercise_id,
               max_weight: max_weight},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                refresh_max_weight_records(exercise_date);
                $("#" + MODAL_ADD_MAX_WEIGHT_ID).modal('hide');
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});
//--------------------------------------------------
// body weight record - components
//--------------------------------------------------
// edit body weight button onClick event
$("#" + BODY_WEIGHT_EDIT_BUTTON_ID).on("click", function() {
    $("#" + BODY_WEIGHT_INPUT_ID).removeAttr("readonly");
    $("#" + BODY_WEIGHT_EDIT_BUTTON_ID).addClass("d-none");
    $("#" + BODY_WEIGHT_SAVE_BUTTON_ID).removeClass("d-none");
});
// save body weight button onClick event
$("#" + BODY_WEIGHT_SAVE_BUTTON_ID).on("click", function() {
    const record_date = get_record_date();
    const body_weight = $("#" + BODY_WEIGHT_INPUT_ID).val();
    $.ajax({
        url: "/api/edit_body_weight",
        type: "POST",
        data: {record_date: record_date,
               body_weight: body_weight},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                $("#" + BODY_WEIGHT_INPUT_ID).prop("readonly", true);
                $("#" + BODY_WEIGHT_SAVE_BUTTON_ID).addClass("d-none");
                $("#" + BODY_WEIGHT_EDIT_BUTTON_ID).removeClass("d-none");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});
//--------------------------------------------------
// muscle weight record - components
//--------------------------------------------------
// edit muscle weight button onClick event
$("#" + MUSCLE_WEIGHT_EDIT_BUTTON_ID).on("click", function() {
    $("#" + MUSCLE_WEIGHT_INPUT_ID).removeAttr("readonly");
    $("#" + MUSCLE_WEIGHT_EDIT_BUTTON_ID).addClass("d-none");
    $("#" + MUSCLE_WEIGHT_SAVE_BUTTON_ID).removeClass("d-none");
});
// save muscle weight button onClick event
$("#" + MUSCLE_WEIGHT_SAVE_BUTTON_ID).on("click", function() {
    const record_date = get_record_date();
    const muscle_weight = $("#" + MUSCLE_WEIGHT_INPUT_ID).val();
    $.ajax({
        url: "/api/edit_muscle_weight",
        type: "POST",
        data: {record_date: record_date,
               muscle_weight: muscle_weight},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                $("#" + MUSCLE_WEIGHT_INPUT_ID).prop("readonly", true);
                $("#" + MUSCLE_WEIGHT_SAVE_BUTTON_ID).addClass("d-none");
                $("#" + MUSCLE_WEIGHT_EDIT_BUTTON_ID).removeClass("d-none");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});
//--------------------------------------------------
// fat rate record - components
//--------------------------------------------------
// edit fat rate button onClick event
$("#" + FAT_RATE_EDIT_BUTTON_ID).on("click", function() {
    $("#" + FAT_RATE_INPUT_ID).removeAttr("readonly");
    $("#" + FAT_RATE_EDIT_BUTTON_ID).addClass("d-none");
    $("#" + FAT_RATE_SAVE_BUTTON_ID).removeClass("d-none");
});
// save fat rate button onClick event
$("#" + FAT_RATE_SAVE_BUTTON_ID).on("click", function() {
    const record_date = get_record_date();
    const fat_rate = $("#" + FAT_RATE_INPUT_ID).val();
    $.ajax({
        url: "/api/edit_fat_rate",
        type: "POST",
        data: {record_date: record_date,
               fat_rate: fat_rate},
        dataType: "json",
        beforeSend:function() {
            trigger_show_loading_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                $("#" + FAT_RATE_INPUT_ID).prop("readonly", true);
                $("#" + FAT_RATE_SAVE_BUTTON_ID).addClass("d-none");
                $("#" + FAT_RATE_EDIT_BUTTON_ID).removeClass("d-none");
            } else {
                warning(data["error_message"]);
            }
        },
        complete:function() {
            trigger_hide_loading_modal();
        }
    });
});