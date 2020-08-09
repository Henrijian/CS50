import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, _app_ctx_stack
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# self-defined library
from lib.helpers import *
from lib.error_codes import *
from lib.fitbook_db import *
# user associated lib
from lib.users import *
from lib import exercises

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database manager
DATABASE = "fitbook.db"


def get_db():
    db = getattr(_app_ctx_stack.top, "_database", None)
    if db is None:
        db = _app_ctx_stack.top._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.text_factory = str
        db.row_factory = lambda cur, row: dict((col[0], row[idx]) for idx, col in enumerate(cur.description))
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(_app_ctx_stack.top, "_database", None)
    if db is not None:
        db.close()


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


##################################################
# Pages
##################################################
@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get register information
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check register information is in valid format
        status_code = is_register_info_valid(get_db(), username, password, confirmation)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        # Add user to database
        status_code = register_user(get_db(), username, password)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        # Get log-in information
        username = request.form.get("username")
        password = request.form.get("password")

        # Check log-in information
        status_code = login_user(get_db(), username, password)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        # Remember which user has logged in
        user_id = get_user_id(get_db(), username)
        session["user_id"] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    if request.method == "POST":
        return render_template("record.html")
    else:
        # Get user ID
        user_id = session["user_id"]
        # Get record date
        record_date_request = request.args.get("record_date", None)
        if record_date_request:
            record_date = exercises.exercise_date_str_to_date(record_date_request)
            if not record_date:
                raise Exception("Request date is invalid: %s" % record_date_request)
        else:
            record_date = datetime.datetime.now()
        record_date_str = exercises.exercise_date_to_date_str(record_date)
        # Get strength muscle groups
        strength_muscle_groups = sorted(get_strength_muscle_groups(get_db()))
        # Get strength exercise names and ids
        strength_exercise_ids_names = get_exercise_ids_names_by_muscle_group(get_db(), strength_muscle_groups[0])
        strength_exercise_ids_names = sorted(strength_exercise_ids_names, key=lambda token: token[1])
        # Get Cardio exercise names and ids
        cardio_exercise_ids_names = get_cardio_exercise_ids_names(get_db())
        cardio_exercise_ids_names = sorted(cardio_exercise_ids_names, key=lambda token: token[1])
        # Get exercise records
        exercise_records = exercises.get_exercise_records(get_db(), user_id, record_date)
        # Get templates of exercise records
        exercise_record_templates = []
        for exercise_record in exercise_records:
            exercise_type = exercise_record.exercise_type
            record_details_id = exercise_record.record_details_id
            if exercise_type == EXERCISE_TYPE_STRENGTH:
                exercise_record_template = get_strength_exercise_record_template(record_details_id)
            elif exercise_type == EXERCISE_TYPE_CARDIO:
                exercise_record_template = get_cardio_exercise_record_template(record_details_id)
            else:
                raise Exception("Unknown exercise type* %s" % exercise_type)
            exercise_record_templates.append(exercise_record_template)
        # Get templates of max weight exercise records
        max_weight_records = exercises.get_max_weight_records(get_db(), user_id, record_date)
        max_weight_records.sort_by_name()
        max_weight_record_templates = []
        for record in max_weight_records:
            template = get_max_weight_record_template(record.max_weight_record_id)
            max_weight_record_templates.append(template)

        return render_template("record.html",
                               record_date_str=record_date_str,
                               strength_muscle_groups=strength_muscle_groups,
                               strength_exercise_ids_names=strength_exercise_ids_names,
                               cardio_exercise_ids_names=cardio_exercise_ids_names,
                               exercise_record_templates=exercise_record_templates,
                               max_weight_record_templates=max_weight_record_templates)


def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


##################################################
# API
##################################################
@app.route("/api/login_check", methods=["GET", "POST"])
def login_check():
    if request.method == "POST":
        # Get log-in information
        username = request.form.get("username")
        password = request.form.get("password")

        # Check log-in information
        status_code = login_user(get_db(), username, password)
        if status_code != ERR_SUCCESS:
            return response_json(status_code)

        return response_json(ERR_SUCCESS)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/register_check", methods=["GET", "POST"])
def register_check():
    if request.method == "POST":
        # Get register information
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check register information is in valid format
        status_code = is_register_info_valid(get_db(), username, password, confirmation)
        if status_code != ERR_SUCCESS:
            return response_json(status_code)

        return response_json(ERR_SUCCESS)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_muscle_group_exercises")
@login_required
def get_muscle_group_exercises():
    muscle_group = request.args.get('muscle_group')
    if not muscle_group:
        return response_json(ERR_MUSCLE_GROUP_EMPTY)

    muscle_groups = get_muscle_groups(get_db())
    if not (muscle_group in muscle_groups):
        return response_json(ERR_MUSCLE_GROUP_NOT_EXIST)

    exercise_ids_names = get_exercise_ids_names_by_muscle_group(get_db(), muscle_group)
    if not exercise_ids_names:
        return response_json(ERR_MUSCLE_GROUP_NOT_EXIST)
    exercise_ids_names = sorted(exercise_ids_names, key=lambda token: token[1])

    return response_json(ERR_SUCCESS, result=exercise_ids_names)


@app.route("/api/get_exercise_name")
@login_required
def get_exercise_name():
    exercise_id = request.args.get("id")
    if not exercise_id:
        return response_json(ERR_EXERCISE_ID_EMPTY)

    try:
        exercise_id = int(exercise_id)
    except Exception as e:
        print(e)
        return response_json(ERR_EXERCISE_ID_INVALID)

    exercise_name = get_exercise_name_by_id(get_db(), exercise_id)
    if not exercise_name:
        return response_json(ERR_EXERCISE_NAME_NOT_EXIST)

    return response_json(ERR_SUCCESS, result=exercise_name)


@app.route("/api/get_record", methods=["GET", "POST"])
@login_required
def get_record():
    if request.method == "POST":
        # Get user id
        user_id = session["user_id"]
        # Get record date
        record_date_str = request.form["record_date"]
        if not record_date_str:
            return response_json(ERR_EXERCISE_DATE_EMPTY)
        record_date = exercises.exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_EXERCISE_DATE_INVALID)
        # Get exercise records
        try:
            exercise_records = exercises.get_exercise_records(get_db(), user_id, record_date)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        # Get templates of exercise records
        exercise_record_templates = []
        for exercise_record in exercise_records:
            exercise_type = exercise_record.exercise_type
            record_details_id = exercise_record.record_details_id
            if exercise_type == EXERCISE_TYPE_STRENGTH:
                exercise_record_template = get_strength_exercise_record_template(record_details_id)
            elif exercise_type == EXERCISE_TYPE_CARDIO:
                exercise_record_template = get_cardio_exercise_record_template(record_details_id)
            else:
                raise Exception("Unknown exercise type* %s" % exercise_type)
            exercise_record_templates.append(exercise_record_template)
        exercise_records_template = "\n".join(exercise_record_templates)
        # Get templates of max weight exercise records
        max_weight_records = exercises.get_max_weight_records(get_db(), user_id, record_date)
        max_weight_records.sort_by_name()
        max_weight_record_templates = []
        for record in max_weight_records:
            template = get_max_weight_record_template(record.max_weight_record_id)
            max_weight_record_templates.append(template)
        max_weight_records_template = "\n".join(max_weight_record_templates)
        # Organize result
        result = {"exercise_records": exercise_records_template,
                  "max_weight_records": max_weight_records_template}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_exercise_record", methods=["GET", "POST"])
@login_required
def get_exercise_record():
    if request.method == "POST":
        record_details_id = request.form["record_details_id"]
        try:
            exercise_record = exercises.get_exercise_record(get_db(), record_details_id)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)

        return response_json(ERR_SUCCESS, result=exercise_record.data())
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_exercise_records", methods=["GET", "POST"])
@login_required
def get_exercise_records():
    if request.method == "POST":
        # Get user id
        user_id = session["user_id"]
        # Get record date
        record_date_str = request.form["record_date"]
        if not record_date_str:
            return response_json(ERR_EXERCISE_DATE_EMPTY)
        record_date = exercises.exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_EXERCISE_DATE_INVALID)
        # Get exercise records
        try:
            exercise_records = exercises.get_exercise_records(get_db(), user_id, record_date)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        # Get templates of exercise records
        exercise_records_htmls = []
        for exercise_record in exercise_records:
            exercise_type = exercise_record.exercise_type
            record_details_id = exercise_record.record_details_id
            if exercise_type == EXERCISE_TYPE_STRENGTH:
                exercise_record_template = get_strength_exercise_record_template(record_details_id)
            elif exercise_type == EXERCISE_TYPE_CARDIO:
                exercise_record_template = get_cardio_exercise_record_template(record_details_id)
            else:
                raise Exception("Unknown exercise type* %s" % exercise_type)
            exercise_records_htmls.append(exercise_record_template)
        exercise_records_html = "\n".join(exercise_records_htmls)
        # Organize result
        result = {"exercise_records_html": exercise_records_html}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_strength_exercise_record", methods=["GET", "POST"])
@login_required
def get_strength_exercise_record():
    if request.method == "POST":
        # Get record details id
        record_details_id = request.form["record_details_id"]
        if not record_details_id_exist(get_db(), record_details_id):
            return response_json(ERR_RECORD_DETAILS_ID_NOT_EXIST)
        # Get strength exercise record template
        try:
            exercise_record_template = get_strength_exercise_record_template(record_details_id)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        result = {"exercise_record_html": exercise_record_template}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_cardio_exercise_record", methods=["GET", "POST"])
@login_required
def get_cardio_exercise_record():
    if request.method == "POST":
        # Get record details id
        record_details_id = request.form["record_details_id"]
        if not record_details_id_exist(get_db(), record_details_id):
            return response_json(ERR_RECORD_DETAILS_ID_NOT_EXIST)
        # Get strength exercise record template
        try:
            exercise_record_template = get_cardio_exercise_record_template(record_details_id)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        result = {"exercise_record_html": exercise_record_template}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_exercise_set", methods=["GET", "POST"])
def get_exercise_set():
    if request.method == "POST":
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)
    else:
        set_order = request.args.get("set_order", type=int, default=1)
        set_weight = request.args.get("set_weight", type=int, default=0)
        set_reps = request.args.get("set_reps", type=int, default=0)
        is_sub_set = request.args.get("is_sub_set") == "true"

        exercise_set_template = get_exercise_set_template(set_order, set_weight, set_reps, is_sub_set)
        result = {"exercise_set_template": exercise_set_template}
        return response_json(ERR_SUCCESS, result=result)


@app.route("/api/get_exercise_sets", methods=["GET", "POST"])
@login_required
def get_exercise_sets():
    if request.method == "POST":
        # Get record details id
        record_details_id = request.form["record_details_id"]
        if not record_details_id_exist(get_db(), record_details_id):
            return response_json(ERR_RECORD_DETAILS_ID_NOT_EXIST)
        # Get exercise record
        try:
            exercise_record = exercises.get_exercise_record(get_db(), record_details_id)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        # Get exercise sets templates
        exercise_sets_htmls = []
        exercise_sets = exercise_record.exercise_sets
        cur_order = 1
        for exercise_set in exercise_sets:
            set_order = cur_order
            set_weight = exercise_set.weight
            set_reps = exercise_set.reps
            set_html = get_exercise_set_template(set_order, set_weight, set_reps, False)
            exercise_sets_htmls.append(set_html)
            for sub_set in exercise_set.sub_sets:
                sub_order = set_order
                sub_weight = sub_set.weight
                sub_reps = sub_set.reps
                sub_html = get_exercise_set_template(sub_order, sub_weight, sub_reps, True)
                exercise_sets_htmls.append(sub_html)
            cur_order += 1
        exercise_sets_html = "\n".join(exercise_sets_htmls)
        result = {"exercise_sets_html": exercise_sets_html}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/edit_exercise_record", methods=["GET", "POST"])
@login_required
def edit_exercise_record():
    if request.method == "POST":
        # Get record details id
        record_details_id = request.form["record_details_id"]
        exercise_id = request.form["exercise_id"]
        if not exercise_id:
            return response_json(ERR_EXERCISE_ID_EMPTY)
        # Get exercise type
        exercise_type = get_exercise_type_by_id(get_db(), exercise_id)
        if not exercise_type:
            return response_json(ERR_EXERCISE_ID_INVALID)
        # According exercise type, get needed information
        if exercise_type == EXERCISE_TYPE_STRENGTH: # strength exercise
            # Exercise sets
            exercise_sets_str = request.form["exercise_sets"]
            if not exercise_sets_str:
                return response_json(ERR_EXERCISE_SETS_EMPTY)
            try:
                exercise_sets = exercises.parse_exercise_sets(exercise_sets_str)
            except Exception as e:
                print(e)
                return response_json(ERR_EXERCISE_SETS_INVALID)
            if len(exercise_sets) == 0:
                return response_json(ERR_EXERCISE_SETS_EMPTY)
            # Update to database
            try:
                status_code = exercises.change_to_strength_exercise_record(get_db(), record_details_id, exercise_id,
                                                                           exercise_sets)
            except Exception as e:
                print(e)
                status_code = ERR_INTERNAL
        elif exercise_type == EXERCISE_TYPE_CARDIO: # cardio exercise
            exercise_hours = request.form["exercise_hours"]
            exercise_minutes = request.form["exercise_minutes"]
            exercise_seconds = request.form["exercise_seconds"]
            # Update to database
            try:
                status_code = exercises.change_to_cardio_exercise_record(get_db(), record_details_id, exercise_id,
                                                                         exercise_hours, exercise_minutes,
                                                                         exercise_seconds)
            except Exception as e:
                print(e)
                status_code = ERR_INTERNAL
        else:
            return response_json(ERR_EXERCISE_TYPE_INVALID)

        return response_json(status_code)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/delete_exercise_record", methods=["GET", "POST"])
@login_required
def delete_exercise_record():
    if request.method == "POST":
        # Get record details id
        record_details_id = request.form["record_details_id"]
        if not record_details_id_exist(get_db(), record_details_id):
            return response_json(ERR_RECORD_DETAILS_ID_NOT_EXIST)
        # Delete record details
        try:
            delete_record_details(get_db(), record_details_id)
        except Exception as e:
            print(e)
            return response_json(ERR_DELETE_EXERCISE_RECORD_FAILED)
        return response_json(ERR_SUCCESS)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/append_strength_exercise_records", methods=["GET", "POST"])
@login_required
def append_strength_exercise_records():
    if request.method == "POST":
        # user id
        user_id = session["user_id"]

        # Record date
        record_date_str = request.form["exercise_date"]
        if not record_date_str:
            return response_json(ERR_RECORD_DATE_EMPTY)
        record_date = exercises.exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_RECORD_DATE_INVALID)

        # Exercise id
        exercise_id = request.form['exercise_id']
        if not exercise_id:
            return response_json(ERR_EXERCISE_ID_EMPTY)

        # Exercise sets
        exercise_sets_str = request.form['exercise_sets']

        # Exercise sets
        exercise_sets_str = request.form["exercise_sets"]
        if not exercise_sets_str:
            return response_json(ERR_EXERCISE_SETS_EMPTY)
        try:
            exercise_sets = exercises.parse_exercise_sets(exercise_sets_str)
        except Exception as e:
            print(e)
            return response_json(ERR_EXERCISE_SETS_INVALID)

        if len(exercise_sets) == 0:
            return response_json(ERR_EXERCISE_SETS_EMPTY)

        status_code = exercises.append_strength_exercise_record(get_db(), user_id, record_date,
                                                                exercise_id, exercise_sets)
        if status_code == ERR_SUCCESS:
            record_id = get_record_id(get_db(), user_id, record_date)
            exercise_orders = get_record_details_orders(get_db(), record_id)
            exercise_order = max(exercise_orders)
            record_details_id = get_record_details_id(get_db(), record_id, exercise_id, exercise_order)
            return response_json(status_code, result={"record_details_id": record_details_id})
        else:
            return response_json(status_code)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/append_cardio_exercise_records", methods=["GET", "POST"])
@login_required
def append_cardio_exercise_records():
    if request.method == "POST":
        # user id
        user_id = session["user_id"]

        # Record date
        record_date_str = request.form["exercise_date"]
        if not record_date_str:
            return response_json(ERR_RECORD_DATE_EMPTY)
        record_date = exercises.exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_RECORD_DATE_INVALID)

        # Exercise id
        exercise_id = request.form["exercise_id"]

        # Exercise hours
        exercise_hours = request.form["exercise_hours"]

        # Exercise minutes
        exercise_minutes = request.form["exercise_minutes"]

        # Exercise seconds
        exercise_seconds = request.form["exercise_seconds"]

        status_code = exercises.append_cardio_exercise_record(get_db(), user_id, record_date, exercise_id,
                                                              exercise_hours, exercise_minutes, exercise_seconds)
        if status_code == ERR_SUCCESS:
            record_id = get_record_id(get_db(), user_id, record_date)
            exercise_orders = get_record_details_orders(get_db(), record_id)
            exercise_order = max(exercise_orders)
            record_details_id = get_record_details_id(get_db(), record_id, exercise_id, exercise_order)
            return response_json(status_code, result={"record_details_id": record_details_id})
        else:
            return response_json(status_code)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/append_max_weight_records", methods=["GET", "POST"])
@login_required
def append_max_weight_records():
    if request.method == "POST":
        # user id
        user_id = session["user_id"]

        # Record date
        record_date_str = request.form["exercise_date"]
        if not record_date_str:
            return response_json(ERR_RECORD_DATE_EMPTY)
        record_date = exercises.exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_RECORD_DATE_INVALID)

        # Get exercise id
        exercise_id = request.form["exercise_id"]

        # Get max weight
        max_weight = request.form["max_weight"]
        # Check max weight
        try:
            max_weight = int(max_weight)
            if not exercises.is_max_weight_valid(max_weight):
                return response_json(ERR_MAX_WEIGHT_INVALID)
        except Exception as e:
            print(e)
            return response_json(ERR_MAX_WEIGHT_INVALID)

        # Get record id
        record_id = get_record_id(get_db(), user_id, record_date)

        # Check Max weight record existence
        if max_weight_record_exist(get_db(), record_id, exercise_id, max_weight):
            return response_json(ERR_MAX_WEIGHT_REPEAT)

        status_code = exercises.append_max_weight_record(get_db(), user_id, record_date, exercise_id, max_weight)
        if status_code == ERR_SUCCESS:
            record_id = get_record_id(get_db(), user_id, record_date)
            max_weight_record_id = get_max_weight_record_id(get_db(), record_id, exercise_id, max_weight)
            return response_json(status_code, result={"max_weight_record_id": max_weight_record_id})
        else:
            return response_json(status_code)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


@app.route("/api/get_max_weight_record", methods=["GET", "POST"])
@login_required
def get_max_weight_record():
    if request.method == "POST":
        # Check max weight record id
        max_weight_record_id = request.form["max_weight_record_id"]
        if not max_weight_record_id_exist(get_db(), max_weight_record_id):
            return response_json(ERR_MAX_WEIGHT_INVALID)
        # Get max weight record html
        try:
            max_weight_record_html = get_max_weight_record_template(max_weight_record_id)
        except Exception as e:
            print(e)
            return response_json(ERR_INTERNAL)
        result = {"max_weight_record_html": max_weight_record_html}
        return response_json(ERR_SUCCESS, result=result)
    else:
        return response_json(ERR_UNSUPPORT_REQUEST_METHOD)


##################################################
# Templates
##################################################
def get_strength_exercise_record_template(record_details_id):
    if not record_details_id_exist(get_db(), record_details_id):
        raise Exception("Record details id does not exist")
    # get exercise record
    exercise_record = exercises.get_exercise_record(get_db(), record_details_id)
    # get exercise type
    exercise_type = exercise_record.exercise_type
    # check exercise type
    if not exercise_type == EXERCISE_TYPE_STRENGTH:
        raise Exception("Specified exercise is not a strength exercise")
    # get exercise name
    exercise_name = exercise_record.exercise_name
    # get exercise sets
    exercise_sets = exercise_record.exercise_sets.data()
    # check exercise sets
    if len(exercise_sets) == 0:
        raise Exception("Required strength exercise does not have any set")
    return render_template("record_exercise_strength.html",
                           record_details_id=record_details_id,
                           exercise_name=exercise_name,
                           exercise_sets=exercise_sets)


def get_cardio_exercise_record_template(record_details_id):
    if not record_details_id_exist(get_db(), record_details_id):
        raise Exception("Record details id does not exist")
    # get exercise record
    exercise_record = exercises.get_exercise_record(get_db(), record_details_id)
    # get exercise type
    exercise_type = exercise_record.exercise_type
    # check exercise type
    if not exercise_type == EXERCISE_TYPE_CARDIO:
        raise Exception("Specified exercise is not a cardio exercise")
    # get exercise name
    exercise_name = exercise_record.exercise_name
    # get exercise time
    exercise_time = exercise_record.exercise_time
    exercise_hours = exercise_time.hours
    exercise_minutes = exercise_time.minutes
    exercise_seconds = exercise_time.seconds
    return render_template("record_exercise_cardio.html",
                           record_details_id=record_details_id,
                           exercise_name=exercise_name,
                           exercise_hours=exercise_hours,
                           exercise_minutes=exercise_minutes,
                           exercise_seconds=exercise_seconds)


def get_exercise_set_template(set_order=0, set_weight=0, set_reps=0, is_sub_set=False):
    if not isinstance(set_order, int):
        raise Exception("set_order type error")
    if not isinstance(set_weight, int):
        raise Exception("set_weight type error")
    if not isinstance(set_reps, int):
        raise Exception("set_reps type error")
    if not isinstance(is_sub_set, bool):
        raise Exception("is_sub_set type error")
    return render_template("exercise_set.html",
                           set_order=set_order,
                           set_weight=set_weight,
                           set_reps=set_reps,
                           is_sub_set=is_sub_set)


def get_max_weight_record_template(max_weight_record_id):
    if not max_weight_record_id_exist(get_db(), max_weight_record_id):
        raise Exception("Max weight record id(%s) does not exist" % max_weight_record_id)
    # Get exercise name
    exercise_id = get_max_weight_records_exercise_id(get_db(), max_weight_record_id)
    if exercise_id <= 0:
        raise Exception("Cannot get exercise id by max weight record id(%s)" % max_weight_record_id)
    exercise_name = get_exercise_name_by_id(get_db(), exercise_id)
    if not exercise_name:
        raise Exception("Cannot get exercise name by exercise id(%s)" % exercise_id)
    # Get exercise max weight
    exercise_max_weight = get_max_weight_records_weight(get_db(), max_weight_record_id)
    if exercise_max_weight <= 0:
        raise Exception("Cannot get exercise max weight by max weight record id(%s)" % max_weight_record_id)
    return render_template("record_max_weight_exercise.html",
                           max_weight_record_id=max_weight_record_id,
                           exercise_name=exercise_name,
                           exercise_max_weight=exercise_max_weight)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)