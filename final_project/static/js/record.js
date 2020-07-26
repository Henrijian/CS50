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
        weight_input.classList.add("form-control", "text-right");
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
        reps_input.classList.add("form-control", "text-right");
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

// initialize add exercise modal interface
var initialize_add_exercise_modal = function() {
    // initialize strength exercise tab

    // select first muscle group and first exercise
    const muscle_group_select = $("#strength_muscle_group_select");
    const first_muscle_group = muscle_group_select.children("option")[0];
    muscle_group_select.val(first_muscle_group.value).change();

    // clean up set items
    $("#exercise_sets").empty();

    // initialize cardio exercise tab
    const cardio_exercise_select = $("#cardio_exercise_select");
    const first_cardio_exercise = cardio_exercise_select.children("option")[0];
    cardio_exercise_select.val(first_cardio_exercise.value);

    // clean up time input
    $("#cardio_exercise_time").children("input").val("");
}

// initialize add exercise modal before showing it toe user
$('#modal_add_exercise').on("show.bs.modal", function (e) {
  // do something...
  initialize_add_exercise_modal();
//  alert("ahahhahah");
})

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