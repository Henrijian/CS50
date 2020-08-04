//==================================================
// global variables
//==================================================

const MODAL_ADD_EXERCISE_ID = "modal_add_exercise";

const MODAL_ADD_EXERCISE_LOADING_ID = "modal_add_exercise_loading";

const STRENGTH_MUSCLE_GROUP_SELECT_ID = "strength_muscle_group_select"

const STRENGTH_EXERCISE_SELECT_ID = "strength_exercise_select";

const EXERCISE_SETS_ID = "exercise_sets";

const CARDIO_EXERCISE_SELECT_ID = "cardio_exercise_select";

const CARDIO_EXERCISE_TIME_ID = "cardio_exercise_time";

const CARDIO_EXERCISE_HOURS_ID = "cardio_exercise_hrs";

const CARDIO_EXERCISE_MINUTES_ID = "cardio_exercise_mins";

const CARDIO_EXERCISE_SECONDS_ID = "cardio_exercise_secs";

const CARD_RECORD_EXERCISE_ID = "card_record_exercise";

const BTN_ADD_EXERCISE_ID = "btn_add_exercise";

const BTN_SAVE_EXERCISE_ID = "btn_save_exercise";

const BTN_APPEND_RECORD_EXERCISES_ID = "btn_append_record_exercises";

const STRENGTH_EXERCISE_TAB_ID = "strength_exercise_tab";

const RECORD_EXERCISES_ID = "record_exercises";

const RECORD_EXERCISE_DATE_ID = "record_exercise_date";

const RECORD_LOADING_ID = "record_loading";

//==================================================
// functions definitions
//==================================================

// get set element
var get_set_element = function(set_order, is_sub_set) {
        // create set item
        const set_item = document.createElement("div");
        set_item.classList.add("input-group", "input-group-sm", "row", "m-0");
        set_item.setAttribute("set_order", set_order);
        if (is_sub_set) {
            set_item.classList.add("exercise_sub_set");
        } else {
            set_item.classList.add("exercise_set");
        }

        // append set header to set item
        const set_header = document.createElement("div");
        set_item.appendChild(set_header);
        set_header.classList.add("input-group-prepend", "col-sm-2", "p-0", "d-flex");

        const set_header_span = document.createElement("span");
        set_header.appendChild(set_header_span);
        set_header_span.classList.add("input-group-text", "flex-fill");
        set_header_span.textContent = "Set";

        const set_header_bold = document.createElement("b");
        set_header_span.appendChild(set_header_bold);
        set_header_bold.classList.add("set_order_text", set_order);
        set_header_bold.textContent = set_order;
        if (is_sub_set) {
            set_header_span.style.visibility = "hidden";
        }

        // append set weight input to set item
        const weight_input = document.createElement("input");
        weight_input.classList.add("form-control", "text-right", "exercise_weight");
        weight_input.type = "number";
        weight_input.placeholder="weight";
        weight_input.value = "";
        set_item.appendChild(weight_input);
        const weight_input_append = document.createElement("div");
        weight_input_append.classList.add("input-group-append");
        set_item.appendChild(weight_input_append);
        const weight_input_append_span = document.createElement("span");
        weight_input_append_span.classList.add("input-group-text");
        weight_input_append_span.textContent = "kg";
        weight_input_append.appendChild(weight_input_append_span);


        // append set reps input to set item
        const reps_input = document.createElement("input");
        reps_input.classList.add("form-control", "text-right", "exercise_reps");
        reps_input.type = "number";
        reps_input.placeholder="repetitions";
        reps_input.value = "";
        set_item.appendChild(reps_input);
        const reps_input_append = document.createElement("div");
        reps_input_append.classList.add("input-group-append");
        set_item.appendChild(reps_input_append);
        const reps_input_append_span = document.createElement("span");
        reps_input_append_span.classList.add("input-group-text");
        reps_input_append_span.textContent = "reps";
        reps_input_append.appendChild(reps_input_append_span);


        // append action dropdown button to set item
        const action_button_container = document.createElement("div");
        action_button_container.classList.add("input-group-append");
        set_item.appendChild(action_button_container);

        // dropdown button
        const action_button = document.createElement("button");
        action_button.classList.add("input-group-text", "btn", "btn-outline-primary", "dropdown-toggle", "px-1");
        action_button.type = "button";
        action_button.setAttribute("data-toggle", "dropdown");
        action_button_container.appendChild(action_button);

        // dropdown menu
        const action_menu = document.createElement("div");
        action_menu.classList.add("dropdown-menu");
        action_button_container.appendChild(action_menu);

        // add set menu item
        const menu_item_add = document.createElement("a");
        menu_item_add.classList.add("dropdown-item", "btn_add_sub_set");
        menu_item_add.href = "#";
        menu_item_add.textContent = "Add";
        action_menu.appendChild(menu_item_add);

        // delete set menu item
        const menu_item_delete = document.createElement("a");
        if (is_sub_set) {
            menu_item_delete.classList.add("dropdown-item", "btn_delete_sub_set");
        } else {
            menu_item_delete.classList.add("dropdown-item", "btn_delete_set");
        }
        menu_item_delete.href = "#";
        menu_item_delete.textContent = "Delete";
        action_menu.appendChild(menu_item_delete);

        return set_item;
}

// get exercise record card header
var get_exercise_record_card_element = function(record_details_id, exercise_name) {
    // create exercise card
    const exercise_card = document.createElement("div");
    exercise_card.classList.add("card", "exercise_record");
    exercise_card.setAttribute("record_details_id", record_details_id);

    // card header
    const card_header = document.createElement("div");
    exercise_card.appendChild(card_header);
    card_header.classList.add("card-header", "px-2");

    // card header link
    const card_header_link = document.createElement("a");
    card_header.appendChild(card_header_link);
    card_header_link.setAttribute("data-toggle", "collapse");
    card_header_link.setAttribute("aria-expanded", "false");
    const card_body_id = "exercose_record_" + record_details_id;
    card_header_link.setAttribute("href", "#" + card_body_id);
    card_header_link.innerHTML = "<i class=\"fas fa-caret-down collapse-open\"></i>"
                                +"<i class=\"fas fa-caret-up collapse-close\"></i>"
                                +exercise_name;

    // dropdown menu
    const dropdown_container = document.createElement("div");
    card_header.appendChild(dropdown_container);
    dropdown_container.classList.add("dropdown", "float-right");
    // dropdown button
    const dropdown_button = document.createElement("button");
    dropdown_container.appendChild(dropdown_button);
    dropdown_button.classList.add("btn", "btn-outline-primary", "btn-sm", "m-0", "p-0", "px-3");
    dropdown_button.setAttribute("style", "border-color: rgba(0,0,0,0);");
    dropdown_button.setAttribute("type", "button");
    dropdown_button.setAttribute("data-toggle", "dropdown");
    // dropdown icon
    const dropdown_icon = document.createElement("i");
    dropdown_button.appendChild(dropdown_icon);
    dropdown_icon.classList.add("fas", "fa-ellipsis-h");
    // dropdown menu
    const dropdown_menu = document.createElement("div");
    dropdown_container.appendChild(dropdown_menu);
    dropdown_menu.classList.add("dropdown-menu");
    // dropdown edit button
    const edit_button = document.createElement("a");
    dropdown_menu.appendChild(edit_button);
    edit_button.classList.add("btn", "dropdown-item");
    edit_button.setAttribute("type", "button");
    edit_button.setAttribute("data-toggle", "modal");
    edit_button.setAttribute("data-target", "#" + MODAL_ADD_EXERCISE_ID);
    edit_button.textContent = "Edit";
    // dropdown delete button
    const delete_button = document.createElement("a");
    dropdown_menu.appendChild(delete_button);
    delete_button.classList.add("btn", "dropdown-item");
    delete_button.setAttribute("type", "button");
    delete_button.setAttribute("href", "#");
    delete_button.textContent = "Delete";

    // collapse body
    const collapse_body = document.createElement("div");
    exercise_card.appendChild(collapse_body);
    collapse_body.setAttribute("id", card_body_id);
    collapse_body.classList.add("collapse");
    $(collapse_body).on("show.bs.collapse", function(event) {
        on_show_collapse_event(event);
    });
    $(collapse_body).on("hide.bs.collapse", function(event) {
        on_close_collpase_event(event);
    });
    // card body
    const card_body = document.createElement("div");
    collapse_body.appendChild(card_body);
    card_body.classList.add("card-body", "p-0");

    return exercise_card;
}

// get strength exercise element
var get_strength_exercise_element = function(record_details_id, exercise_name, exercise_sets) {
    // get card element
    const card_element = get_exercise_record_card_element(record_details_id, exercise_name);
    // get card body
    const card_body = $(card_element).find(".card-body").get(0);
    // sets table
    const sets_table = document.createElement("table");
    card_body.appendChild(sets_table);
    sets_table.classList.add("table", "table-hover", "table-dark", "table-sm", "m-0");
    // sets table header
    const table_header = document.createElement("thead");
    sets_table.appendChild(table_header);
    // header row
    const header_row = document.createElement("tr");
    table_header.appendChild(header_row);
    // headers
    const set_col_header = document.createElement("th");
    header_row.appendChild(set_col_header);
    set_col_header.setAttribute("scope", "col");
    set_col_header.textContent = "Set";

    const weight_col_header = document.createElement("th");
    header_row.appendChild(weight_col_header);
    weight_col_header.setAttribute("scope", "col");
    weight_col_header.textContent = "Weight(kg)";

    const reps_col_header = document.createElement("th");
    header_row.appendChild(reps_col_header);
    reps_col_header.setAttribute("scope", "col");
    reps_col_header.textContent = "Reps";

    // table body
    const table_body = document.createElement("tbody");
    sets_table.appendChild(table_body);

    var set_order = "";
    for (var i = 0; i < exercise_sets.length; i++) {
        var set_token = exercise_sets[i];
        var set_row = document.createElement("tr");
        table_body.appendChild(set_row);

        var set_order_cell = document.createElement("th");
        set_row.appendChild(set_order_cell);
        set_order_cell.setAttribute("scope", "row");
        if (set_order != set_token["set_order"]) {
            set_order_cell.textContent = set_token["set_order"];
            set_order = set_token["set_order"];
        }

        var set_weight_cell = document.createElement("td");
        set_row.appendChild(set_weight_cell);
        set_weight_cell.classList.add("weight_cell");
        set_weight_cell.textContent = set_token["set_weight"];

        var set_reps_cell = document.createElement("td");
        set_row.appendChild(set_reps_cell);
        set_reps_cell.classList.add("reps_cell");
        set_reps_cell.textContent = set_token["set_reps"];
    }
    return card_element;
}

// get cardio exercise element
var get_cardio_exercise_element = function(record_details_id, exercise_name, exercise_hours, exercise_minutes, exercise_seconds) {
    // get card element
    const card_element = get_exercise_record_card_element(record_details_id, exercise_name);
    // get card body
    const card_body = $(card_element).find(".card-body").get(0);
    // time table
    const time_table = document.createElement("table");
    card_body.appendChild(time_table);
    time_table.classList.add("table", "table-hover", "table-dark", "table-sm", "m-0");
    // sets table header
    const table_header = document.createElement("thead");
    time_table.appendChild(table_header);
    // header row
    const header_row = document.createElement("tr");
    table_header.appendChild(header_row);
    // headers
    const hrs_col_header = document.createElement("th");
    header_row.appendChild(hrs_col_header);
    hrs_col_header.setAttribute("scope", "col");
    hrs_col_header.textContent = "Hrs";

    const mins_col_header = document.createElement("th");
    header_row.appendChild(mins_col_header);
    mins_col_header.setAttribute("scope", "col");
    mins_col_header.textContent = "Mins";

    const secs_col_header = document.createElement("th");
    header_row.appendChild(secs_col_header);
    secs_col_header.setAttribute("scope", "col");
    secs_col_header.textContent = "Secs";

    // table body
    const table_body = document.createElement("tbody");
    time_table.appendChild(table_body);
    // table row
    const time_row = document.createElement("tr");
    table_body.appendChild(time_row);
    // hours cell
    const hours_cell = document.createElement("th");
    time_row.appendChild(hours_cell);
    hours_cell.setAttribute("scope", "row");
    hours_cell.classList.add("hours_cell");
    hours_cell.textContent = exercise_hours;
    // minutes cell
    const minutes_cell = document.createElement("td");
    time_row.appendChild(minutes_cell);
    minutes_cell.classList.add("minutes_cell");
    minutes_cell.textContent = exercise_minutes;
    // seconds cell
    const seconds_cell = document.createElement("td");
    time_row.appendChild(seconds_cell);
    seconds_cell.classList.add("seconds_cell");
    seconds_cell.textContent = exercise_seconds;

    return card_element;
}

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

// initialize add exercise modal
var initialize_add_exercise_modal = function() {
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

    // hide save button
    hide_save_exercise_button();

    // show add button
    show_add_exercise_button();
}

// initialize exercise records
var initialize_exercise_records = function() {
    $("#" + RECORD_EXERCISES_ID).empty();
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

// load information to add exercise modal
var load_add_exercise_modal = function(exercise_date, exercise_order) {
    // add exercise record to server
    $.ajax({
        url: "/api/get_exercise_record",
        type: "POST",
        data: {exercise_date: exercise_date,
               exercise_order: exercise_order},
        dataType: "json",
        beforeSend:function() {
            toggle_on_loading_progress_bar_exercise_modal();
        },
        success:function(data) {
            if (data["error_code"] == 0) {
                console.log(data["result"]);
            } else {
                console.log(data["error_message"]);
                alert_add_exercise_modal(data["error_message"]);
                initialize_add_exercise_modal();
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_exercise_modal();
        }
    });
}

// get record date
var get_record_date = function() {
    const input_exercise_date = $("#" + RECORD_EXERCISE_DATE_ID).get(0);
    if (!input_exercise_date) {
        return null;
    }
    return input_exercise_date.value;
}

//==================================================
// event binding
//==================================================

// bind add exercise button onClick event
$("#" + BTN_APPEND_RECORD_EXERCISES_ID).on("click", function() {
    // get exercise date
    if (!get_record_date()) {
        alert_record_exercise_card("Must specify date");
        return false;
    }
    initialize_add_exercise_modal();
});

// bind .btn_add_exercise button onClick event,
// to check exercise record before add it to main container
$("#" + BTN_ADD_EXERCISE_ID).on("click", function() {
    const record_exercises = document.getElementById(RECORD_EXERCISES_ID);
    if (!record_exercises) {
        console.log("exercise records container does not exist");
        return false;
    }
    const strength_tab_active = $("#" + STRENGTH_EXERCISE_TAB_ID + ".active").length > 0;
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
            url: "/api/append_strength_exercise",
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
                    const exercise_name = result["exercise_name"];
                    const record_exercise_card = get_strength_exercise_element(record_details_id, exercise_name, exercise_sets);
                    record_exercises.append(record_exercise_card);
                    refresh_collapse_toggler();
                    $("#" + MODAL_ADD_EXERCISE_ID).modal('hide')
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
            url: "/api/append_cardio_exercise",
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
                    const exercise_name = result["exercise_name"];
                    const record_exercise_card = get_cardio_exercise_element(record_details_id, exercise_name, exercise_hours, exercise_minutes, exercise_seconds);
                    record_exercises.append(record_exercise_card);
                    refresh_collapse_toggler();
                    $("#" + MODAL_ADD_EXERCISE_ID).modal('hide')
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

// bind datepicker onChangeDate event
$("#" + RECORD_EXERCISE_DATE_ID).datepicker().on("changeDate", function(e){
    initialize_exercise_records();
    const exercise_records_element = document.getElementById(RECORD_EXERCISES_ID);
    if (!exercise_records_element) {
        console.log("exercise records container does not exist");
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
                const exercise_records = result["exercise_records"];
                for (i = 0; i < exercise_records.length; i++)
                {
                    var exercise_record = exercise_records[i];
                    var record_details_id = exercise_record["record_details_id"];
                    var exercise_type = exercise_record["exercise_type"];
                    var exercise_name = exercise_record["exercise_name"];
                    if (exercise_type == "strength") {
                        var exercise_sets = [];
                        var exercise_sets_json = exercise_record["exercise_sets"];
                        $.each(exercise_sets_json, function(i, set_json){
                            const order = set_json["order"];
                            const weight = set_json["weight"];
                            const reps = set_json["reps"];
                            exercise_sets.push({
                                set_order: order,
                                set_weight: weight,
                                set_reps: reps,
                            });
                            const sub_sets = set_json["sub_sets"];
                            $.each(sub_sets, function(j, sub_set_json) {
                                const sub_order = sub_set_json["order"];
                                const sub_weight = sub_set_json["weight"];
                                const sub_reps = sub_set_json["reps"];
                                exercise_sets.push({
                                    set_order: order,
                                    set_weight: sub_weight,
                                    set_reps: sub_reps,
                                });
                            });
                        });

                        var exercise_record_element = get_strength_exercise_element(record_details_id, exercise_name, exercise_sets);
                    } else if (exercise_type == "cardio") {
                        var exercise_time = exercise_record["exercise_time"];
                        var exercise_hours = exercise_time["hours"];
                        var exercise_minutes = exercise_time["minutes"];
                        var exercise_seconds = exercise_time["seconds"];
                        var exercise_record_element = get_cardio_exercise_element(record_details_id, exercise_name, exercise_hours, exercise_minutes, exercise_seconds);
                    } else {
                        console.log("unknown exercise type: " + exercise_type);
                        continue;
                    }
                    exercise_records_element.appendChild(exercise_record_element);
                }
                refresh_collapse_toggler();
            } else {
                alert_record_exercise_card(data["error_message"]);
            }
        },
        complete:function() {
            toggle_off_loading_progress_bar_record();
        }
    });
});

// bind .muscle_group_select select element onChange event to get exercises list from server,
// then refresh exercises select element list
$(function() {
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
            url: "/api/get_exercises",
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
});

// bound .btn_add_set button element onClick event to append set into the container
$(function() {
    $("body").on("click", ".btn_add_set", function() {
        var sets_container_id = $(this).attr("sets-container");
        if (!sets_container_id) {
            return false;
        }
        var sets_container = $("#" + sets_container_id);
        if (!sets_container) {
            return false;
        }
        const sets_count = sets_container.children(".exercise_set").length;
        const set_order = sets_count + 1;
        const set_item = get_set_element(set_order);
        sets_container.append(set_item);
    });
});

// bind .btn_add_sub_set element onClick event to append sub set item
// after currently selected set item
$(function() {
    $("body").on("click", ".btn_add_sub_set", function() {
        var set_items = $(this).parents(".exercise_set, .exercise_sub_set");
        if (set_items.length == 0) {
            return false;
        }
        const set_item = set_items[0];
        const set_order = set_item.getAttribute("set_order");
        const sub_set_item = get_set_element(set_order, true);
        set_item.after(sub_set_item);
    });
});

// bind .btn_delete_sub_set element onClick event to delete currently selected sub set item
$(function() {
    $("body").on("click", ".btn_delete_sub_set", function() {
        var sub_set_items = $(this).parents(".exercise_sub_set");
        if (sub_set_items.length == 0) {
            return false;
        }
        const sub_set_item = sub_set_items[0];
        sub_set_item.remove();
    });
});

// bind .btn_delete_set element onClick event to delete currently selected set item and its sub set items
$(function() {
    $("body").on("click", ".btn_delete_set", function() {
        var parent_set_items = $(this).parents(".exercise_set");
        if (parent_set_items.length == 0) {
            return false;
        }
        const set_item = parent_set_items[0];
        const set_order_str = set_item.getAttribute("set_order");
        const set_order = parseInt(set_order_str, 10);

        // remove sub set items
        $(set_item).siblings("[set_order='" + set_order_str + "']").remove();

        // update set order after currently deleted set order
        const set_items = $(set_item).siblings(".exercise_set, .exercise_sub_set");
        set_items.each(function() {
            var cur_set_order = parseInt($(this).attr("set_order"), 10);
            if (cur_set_order > set_order) {
                set_set_item_order($(this), cur_set_order - 1);
            }
        });
        $(set_item).remove();
    });
});