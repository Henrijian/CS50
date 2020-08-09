//==================================================
// global variables
//==================================================

const MODAL_ADD_EXERCISE_ID = "modal_add_exercise";

const MODAL_ADD_MAX_WEIGHT_ID = "modal_add_max_weight";

const MODAL_ADD_EXERCISE_LOADING_ID = "modal_add_exercise_loading";

const MODAL_ADD_MAX_WEIGHT_LOADING_ID = "modal_add_max_weight_loading";

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

const RECORD_LOADING_ID = "record_loading";

//==================================================
// functions definitions
//==================================================

// change set item order
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

// initialize exercise modal
var initialize_exercise_modal = function() {
    // clean alert message
    close_alert_add_exercise_modal();

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

// initialize add exercise modal
var initialize_add_exercise_modal = function() {
    initialize_exercise_modal();

    // hide save button
    hide_save_exercise_button();

    // show add button
    show_add_exercise_button();
}

// initialize edit exercise modal
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

// initialize max weight modal
var initialize_max_weight_modal = function() {
    // clean alert message
    close_alert_add_max_weight_modal();

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

// initialize add max weight modal
var initialize_add_max_weight_modal = function() {
    initialize_max_weight_modal();

    // hide save button
    hide_save_max_weight_button();

    // show add button
    show_add_max_weight_button();
}

// initialize save max weight modal
var initialize_save_max_weight_modal = function() {
    initialize_max_weight_modal();

    // hide add button
    hide_add_max_weight_button();

    // show save button
    show_save_max_weight_button();
}

// load strength exercise modal
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
            toggle_on_loading_progress_bar_exercise_modal();
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
                    alert_add_exercise_modal("Exercise does not exist");
                    return false;
                }
                $(exercise_select).val(exercise_id);
            } else {
                alert_add_exercise_modal(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_exercise_modal();
        }
    });
    // update exercise sets
    const sets_container = document.getElementById(EXERCISE_SETS_ID);
    if (!sets_container) {
        console.log("cannot get exercise sets container");
        return false;
    }
    $.ajax({
        url: "/api/get_exercise_sets",
        type: "POST",
        data: {record_details_id: record_details_id},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_exercise_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_sets_html_string = result["exercise_sets_html"];
                const exercise_sets_element = $.parseHTML(exercise_sets_html_string);
                $(sets_container).append(exercise_sets_element);
            } else {
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_exercise_modal();
        }
    });
    $("#" + MODAL_ADD_EXERCISE_ID).modal("show");
}

// load cardio exercise modal
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

// show edit exercise modal
var show_edit_exercise_modal = function(record_details_id) {
    // load edit exercise modal
    $.ajax({
        url: "/api/get_exercise_record",
        type: "POST",
        data: {record_details_id: record_details_id},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_record();
            toggle_on_loading_progress_bar_exercise_modal();
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
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_exercise_modal();
            toggle_off_loading_progress_bar_record();
        }
    });
}

// save edit exercise modal
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
            alert_add_exercise_modal("sets cannot be empty");
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
            toggle_on_loading_progress_bar_exercise_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const exercise_records_element = document.getElementById(EXERCISE_RECORDS_ID);
                if (!exercise_records_element) {
                    console.log("exercise records container does not exist");
                    return false;
                }
                // add exercise record to server
                $.ajax({
                    url: "/api/get_exercise_records",
                    type: "POST",
                    data: {record_date: get_record_date()},
                    dataType: "json",
                    beforeSend:function() {
                        toggle_on_loading_progress_bar_exercise_modal();
                    },
                    success:function(data) {
                        if (data["error_code"] == 0) {
                            const result = JSON.parse(data["result"]);
                            const exercise_records = result["exercise_records_html"];
                            initialize_exercise_records();
                            exercise_records_element.innerHTML = exercise_records;
                            refresh_collapse_toggler();
                            $("#" + MODAL_ADD_EXERCISE_ID).modal("hide");
                        } else {
                            alert_add_exercise_modal(data["error_message"]);
                        }
                    },
                    complete:function() {
                        toggle_off_loading_progress_bar_exercise_modal();
                    }
                });
            } else {
                alert_add_exercise_modal(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_exercise_modal();
        }
    });
}

// delete exercise record
var delete_exercise_record = function(record_details_id) {
    // delete exercise record to server
    $.ajax({
        url: "/api/delete_exercise_record",
        type: "POST",
        data: {"record_details_id": record_details_id},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_record();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const exercise_records_element = document.getElementById(EXERCISE_RECORDS_ID);
                if (!exercise_records_element) {
                    console.log("exercise records container does not exist");
                    return false;
                }
                // refresh exercise records from server
                $.ajax({
                    url: "/api/get_exercise_records",
                    type: "POST",
                    data: {record_date: get_record_date()},
                    dataType: "json",
                    beforeSend:function() {
                        toggle_on_loading_progress_bar_exercise_modal();
                    },
                    success:function(data) {
                        if (data["error_code"] == 0) {
                            const result = JSON.parse(data["result"]);
                            const exercise_records = result["exercise_records_html"];
                            initialize_exercise_records();
                            exercise_records_element.innerHTML = exercise_records;
                            refresh_collapse_toggler();
                            $("#" + MODAL_ADD_EXERCISE_ID).modal("hide");
                        } else {
                            alert_add_exercise_modal(data["error_message"]);
                        }
                    },
                    complete:function() {
                        toggle_off_loading_progress_bar_exercise_modal();
                    }
                });
            } else {
                alert_add_exercise_modal(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_record();
        }
    });
}

// initialize exercise records
var initialize_exercise_records = function() {
    $("#" + EXERCISE_RECORDS_ID).empty();
}

// initialize max weight records
var initialize_max_weight_records = function() {
    $("#" + MAX_WEIGHT_RECORDS_ID).empty();
}

// alert message in add exercise modal
var alert_add_exercise_modal = function(message) {
    if (!message) {
        return false;
    }
    const add_exercise_modal_body = $("#" + MODAL_ADD_EXERCISE_ID).find(".modal-body").get(0);
    if (!add_exercise_modal_body) {
        return false;
    }
    alert_at(add_exercise_modal_body, message);
}

// close alert message in add modal exercise modal
var close_alert_add_exercise_modal = function() {
    const add_exercise_modal_body = $("#" + MODAL_ADD_EXERCISE_ID).find(".modal-body").get(0);
    if (!add_exercise_modal_body) {
        return false;
    }
    close_alert_at(add_exercise_modal_body);
}

// alert message in add max weight modal
var alert_add_max_weight_modal = function(message) {
    if (!message) {
        return false;
    }
    const add_max_weight_modal_body = $("#" + MODAL_ADD_MAX_WEIGHT_ID).find(".modal-body").get(0);
    if (!add_max_weight_modal_body) {
        return false;
    }
    alert_at(add_max_weight_modal_body, message);
}

// close alert message in add max weight modal
var close_alert_add_max_weight_modal = function () {
    const add_max_weight_modal_body = $("#" + MODAL_ADD_MAX_WEIGHT_ID).find(".modal-body").get(0);
    if (!add_max_weight_modal_body) {
        return false;
    }
    close_alert_at(add_max_weight_modal_body);
}

// alert message in record card
var alert_record_exercise_card = function(message) {
    if (!message) {
        return false;
    }
    const record_card_body = $("#" + CARD_RECORD_EXERCISE_ID).find(".card-body").get(0);
    if (!record_card_body) {
        return false;
    }
    alert_at(record_card_body, message);
}

// toggle on loading progress bar in record card
var toggle_on_loading_progress_bar_record = function() {
    const loading_progress_bar = $("#" + RECORD_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.remove("d-none");
}

// toggle off loading progress bar in record card
var toggle_off_loading_progress_bar_record = function() {
    const loading_progress_bar = $("#" + RECORD_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.add("d-none");
}

// toggle on loading progress bar in add exercise modal
var toggle_on_loading_progress_bar_exercise_modal = function() {
    const loading_progress_bar = $("#" + MODAL_ADD_EXERCISE_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.remove("d-none");
}

// toggle off loading progress bar in add exercise modal
var toggle_off_loading_progress_bar_exercise_modal = function() {
    const loading_progress_bar = $("#" + MODAL_ADD_EXERCISE_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.add("d-none");
}

// toggle on loading progress bar in add max weight modal
var toggle_on_loading_progress_bar_max_weight_modal = function() {
    const loading_progress_bar = $("#" + MODAL_ADD_MAX_WEIGHT_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.remove("d-none");
}

// toggle off loading progress bar in add max weight modal
var toggle_off_loading_progress_bar_max_weight_modal = function() {
    const loading_progress_bar = $("#" + MODAL_ADD_MAX_WEIGHT_LOADING_ID).get(0);
    if (!loading_progress_bar) {
        return false;
    }
    loading_progress_bar.classList.add("d-none");
}


// get record date
var get_record_date = function() {
    const input_exercise_date = $("#" + RECORD_DATE_ID).get(0);
    if (!input_exercise_date) {
        return null;
    }
    return input_exercise_date.value;
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

//==================================================
// event binding
//==================================================

// bind muscle group selector onChange event to refresh exercises select element list
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
                form_alert(data["error_message"]);
            }
        }
    });
});

// bind append exercise button onClick event
$("#" + BTN_APPEND_EXERCISE_RECORDS_ID).on("click", function() {
    // get exercise date
    if (!get_record_date()) {
        alert_record_exercise_card("Must specify date");
        return false;
    }
    initialize_add_exercise_modal();
});

// bind add exercise button onClick event to check exercise record before add it to main container
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
            alert_add_exercise_modal("sets cannot be empty");
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
                toggle_on_loading_progress_bar_exercise_modal();
            },
            success:function(data) {
                if (data["error_code"] == 0) {
                    const result = JSON.parse(data["result"]);
                    const record_details_id = result["record_details_id"];
                    $.ajax({
                        url: "/api/get_strength_exercise_record",
                        type: "POST",
                        data: {record_details_id: record_details_id},
                        dataType: "json",
                        beforeSend:function() {
                            toggle_on_loading_progress_bar_exercise_modal();
                        },
                        success:function(data) {
                            if (data["error_code"] == 0) {
                                const result = JSON.parse(data["result"]);
                                const exercise_record_html_string = result["exercise_record_html"];
                                const exercise_record_element = $.parseHTML(exercise_record_html_string);
                                $(record_exercises).append(exercise_record_element);
                                refresh_collapse_toggler();
                                $("#" + MODAL_ADD_EXERCISE_ID).modal('hide');
                            } else {
                                alert_add_exercise_modal(data["error_message"]);
                            }
                        },
                        complete:function() {
                            toggle_off_loading_progress_bar_exercise_modal();
                        }
                    });
                } else {
                    alert_add_exercise_modal(data["error_message"]);
                }
            },
            complete:function() {
                toggle_off_loading_progress_bar_exercise_modal();
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
                toggle_on_loading_progress_bar_exercise_modal();
            },
            success:function(data) {
                if (data["error_code"] == 0) {
                    const result = JSON.parse(data["result"]);
                    const record_details_id = result["record_details_id"];
                    $.ajax({
                        url: "/api/get_cardio_exercise_record",
                        type: "POST",
                        data: {record_details_id: record_details_id},
                        dataType: "json",
                        beforeSend:function() {
                            toggle_on_loading_progress_bar_exercise_modal();
                        },
                        success:function(data) {
                            if (data["error_code"] == 0) {
                                const result = JSON.parse(data["result"]);
                                const exercise_record_html_string = result["exercise_record_html"];
                                const exercise_record_element = $.parseHTML(exercise_record_html_string);
                                $(record_exercises).append(exercise_record_element);
                                refresh_collapse_toggler();
                                $("#" + MODAL_ADD_EXERCISE_ID).modal('hide');
                            } else {
                                alert_add_exercise_modal(data["error_message"]);
                            }
                        },
                        complete:function() {
                            toggle_off_loading_progress_bar_exercise_modal();
                        }
                    });
                } else {
                    alert_add_exercise_modal(data["error_message"]);
                }
            },
            complete:function() {
                toggle_off_loading_progress_bar_exercise_modal();
            }
        });
    }
});

// bind append max weight button onClick event
$("#" + BTN_APPEND_MAX_WEIGHT_RECORDS_ID).on("click", function() {
    // get exercise date
    if (!get_record_date()) {
        alert_record_exercise_card("Must specify date");
        return false;
    }
    initialize_add_max_weight_modal();
});

// bind add max weight button onClick event to check max weight record before add it to main container
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
            toggle_on_loading_progress_bar_max_weight_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const max_weight_record_id = result["max_weight_record_id"];
                $.ajax({
                    url: "/api/get_max_weight_record",
                    type: "POST",
                    data: {max_weight_record_id: max_weight_record_id},
                    dataType: "json",
                    beforeSend:function() {
                        toggle_on_loading_progress_bar_max_weight_modal();
                    },
                    success:function(data) {
                        if (data["error_code"] == 0) {
                            const result = JSON.parse(data["result"]);
                            const max_weight_record_html = result["max_weight_record_html"];
                            const max_weight_record_element = $.parseHTML(max_weight_record_html);
                            $(max_weight_records).append(max_weight_record_element);
                            $("#" + MODAL_ADD_MAX_WEIGHT_ID).modal('hide');
                        } else {
                            alert_add_max_weight_modal(data["error_message"]);
                        }
                    },
                    complete:function() {
                        toggle_off_loading_progress_bar_max_weight_modal();
                    }
                });
            } else {
                alert_add_max_weight_modal(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_max_weight_modal();
        }
    });
});

// bind datepicker onChangeDate event to change record in container
$("#" + RECORD_DATE_ID).datepicker().on("changeDate", function(e){
    const exercise_records_element = document.getElementById(EXERCISE_RECORDS_ID);
    if (!exercise_records_element) {
        console.log("exercise records container does not exist");
        return false;
    }
    const max_weight_records_element = document.getElementById(MAX_WEIGHT_RECORDS_ID);
    if (!max_weight_records_element) {
        console.log("max weight records container does not exist");
        return false;
    }
    const record_date = e.format();
    // add exercise record to server
    $.ajax({
        url: "/api/get_record",
        type: "POST",
        data: {record_date: record_date},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_record();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                // Update exercise records
                const exercise_records = result["exercise_records"];
                initialize_exercise_records();
                exercise_records_element.innerHTML = exercise_records;
                refresh_collapse_toggler();
                // Update max weight records
                const max_weight_records = result["max_weight_records"];
                initialize_max_weight_records();
                max_weight_records_element.innerHTML = max_weight_records;
            } else {
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_record();
        }
    });
});

// bind add exercise set button onClick event to append set item in sets container
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
        url: "/api/get_exercise_set",
        type: "GET",
        data: {set_order: set_order,
               set_weight: 0,
               set_reps: 0,
               is_sub_set: false},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_record();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_set_html_string = result["exercise_set_template"];
                const exercise_set_element = $.parseHTML(exercise_set_html_string);
                $(sets_container).append(exercise_set_element);
            } else {
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_record();
        }
    });
});

// bind add exercise sub set button onClick event to append sub set item after currently selected set item
$(document).on("click", ".btn_add_sub_set", function() {
    var set_item = $(this).parents(".exercise_set, .exercise_sub_set").get(0);
    if (!set_item) {
        console.log("cannot get exercise set item");
        return false;
    }
    const set_order = set_item.getAttribute("set_order");
    // get exercise set element
    $.ajax({
        url: "/api/get_exercise_set",
        type: "GET",
        data: {set_order: set_order,
               set_weight: 0,
               set_reps: 0,
               is_sub_set: true},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_record();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                const result = JSON.parse(data["result"]);
                const exercise_set_html_string = result["exercise_set_template"];
                const exercise_set_element = $.parseHTML(exercise_set_html_string);
                $(set_item).after(exercise_set_element);
            } else {
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_record();
        }
    });
});

// bind delete exercise sub set button onClick event to delete currently selected sub set item
$(document).on("click", ".btn_delete_sub_set", function() {
    var sub_set_item = $(this).parents(".exercise_sub_set").get(0);
    if (!sub_set_item) {
        console.log("cannot get exercise sub set item")
        return false;
    }
    sub_set_item.remove();
});

// bind delete exercise set button onClick event to delete currently selected set item and its sub set items
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