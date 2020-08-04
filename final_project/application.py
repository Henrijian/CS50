import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# self-defined library
from lib.helpers import *
from lib.error_codes import *
from lib.fitbookdb import FitBookDB
# user associated lib
from lib.users import *
from lib.exercises import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database manager
db_manager = FitBookDB("fitbook.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/api/register_check", methods=["GET", "POST"])
def register_check():
    if request.method == "POST":
        # Get register information
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check register information is in valid format
        status_code = is_register_info_valid(db_manager, username, password, confirmation)
        if status_code != ERR_SUCCESS:
            return response_json(status_code)

        return response_json(ERR_SUCCESS)
    else:
        status_code = ERR_UNSUPPORT_REQUEST_METHOD
        return apology(error_message(status_code), status_code)


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
        status_code = is_register_info_valid(db_manager, username, password, confirmation)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        # Add user to database
        status_code = register_user(db_manager, username, password)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/api/login_check", methods=["GET", "POST"])
def login_check():
    if request.method == "POST":
        # Get log-in information
        username = request.form.get("username")
        password = request.form.get("password")

        # Check log-in information
        status_code = login_user(db_manager, username, password)
        if status_code != ERR_SUCCESS:
            return response_json(status_code)

        return response_json(ERR_SUCCESS)
    else:
        status_code = ERR_UNSUPPORT_REQUEST_METHOD
        return apology(error_message(status_code), status_code)


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
        status_code = login_user(db_manager, username, password)
        if status_code != ERR_SUCCESS:
            return apology(error_message(status_code), status_code)

        # Remember which user has logged in
        user_id = db_manager.get_user_id(username)
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


@app.route("/api/get_exercises")
@login_required
def get_exercises():
    muscle_group_value = request.args.get('muscle_group')
    if not muscle_group_value:
        return response_json(ERR_MUSCLE_GROUP_EMPTY)

    muscle_groups = db_manager.get_muscle_groups()
    muscle_group_text = ""
    for muscle_group in muscle_groups:
        if validate_string(muscle_group) == muscle_group_value:
            muscle_group_text = muscle_group
    if not muscle_group_text:
        return response_json(ERR_MUSCLE_GROUP_NOT_EXIST)

    exercise_ids_names = db_manager.get_exercise_ids_names_by_muscle_group(muscle_group_text)
    if not exercise_ids_names:
        return response_json(ERR_MUSCLE_GROUP_NOT_EXIST)
    exercise_ids_names = sorted(exercise_ids_names, key=lambda token: token[1])

    return response_json(ERR_SUCCESS, result=exercise_ids_names)


@app.route("/api/get_exercise_by_id")
@login_required
def get_exercise_by_id():
    exercise_id = request.args.get('id')
    if not exercise_id:
        return response_json(ERR_EXERCISE_ID_EMPTY)

    try:
        exercise_id = int(exercise_id)
    except:
        return response_json(ERR_EXERCISE_ID_INVALID)

    exercise_name = db_manager.get_exercise_name_by_id(exercise_id)
    if not exercise_name:
        return response_json(ERR_EXERCISE_NAME_NOT_EXIST)

    return response_json(ERR_SUCCESS, result=exercise_name)


@app.route("/api/get_record", methods=["GET", "POST"])
@login_required
def get_record():
    if request.method == "POST":
        user_id = session["user_id"]

        # Exercise date
        record_date_str = request.form["record_date"]
        if not record_date_str:
            return response_json(ERR_EXERCISE_DATE_EMPTY)
        record_date = exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_EXERCISE_DATE_INVALID)

        exercise_records = get_exercise_records(db_manager, user_id, record_date)
        # try:
        #     exercise_records = get_exercise_records(db_manager, user_id, record_date)
        # except:
        #     return response_json(ERR_INTERNAL)

        result = {"exercise_records": exercise_records.data()}
        return response_json(ERR_SUCCESS, result=result)
    else:
        status_code = ERR_UNSUPPORT_REQUEST_METHOD
        return apology(error_message(status_code), status_code)

@app.route("/api/append_strength_exercise", methods=["GET", "POST"])
@login_required
def append_strength_exercise():
    if request.method == "POST":
        # user id
        user_id = session["user_id"]

        # Record date
        record_date_str = request.form["exercise_date"]
        if not record_date_str:
            return response_json(ERR_RECORD_DATE_EMPTY)
        record_date = exercise_date_str_to_date(record_date_str)
        if not record_date:
            return response_json(ERR_RECORD_DATE_INVALID)

        # Exercise id
        exercise_id = request.form['exercise_id']
        if not exercise_id:
            return response_json(ERR_EXERCISE_ID_EMPTY)

        # Exercise sets
        exercise_sets_str = request.form['exercise_sets']
        if not exercise_sets_str:
            return response_json(ERR_EXERCISE_SETS_EMPTY)
        try:
            exercise_set_dicts = json.loads(exercise_sets_str)
        except:
            return response_json(ERR_EXERCISE_SETS_INVALID)

        if len(exercise_set_dicts) == 0:
            return response_json(ERR_EXERCISE_SETS_EMPTY)

        exercise_sets = ExerciseSets()
        try:
            for exercise_set_dict in exercise_set_dicts:
                set_order = int(exercise_set_dict["set_order"])
                set_weight = int(exercise_set_dict["set_weight"])
                set_reps = int(exercise_set_dict["set_reps"])
                status = is_exercise_set_valid(set_order, set_weight, set_reps)
                if status != ERR_SUCCESS:
                    return response_json(status)

                exercise_set_same_order = exercise_sets.find_by_order(set_order)
                if exercise_set_same_order:
                    exercise_set_same_order.sub_sets.append_set(set_order, set_weight, set_reps)
                else:
                    exercise_sets.append_set(set_order, set_weight, set_reps)
            exercise_sets.sort_by_order()
        except:
            return response_json(ERR_EXERCISE_SETS_INVALID)

        status_code = append_strength_exercise_record(db_manager, user_id, record_date,
                                                      exercise_id, exercise_sets)
        if status_code == ERR_SUCCESS:
            record_id = db_manager.get_record_id(user_id, record_date)
            exercise_orders = db_manager.get_record_details_orders(record_id)
            exercise_order = max(exercise_orders)
            record_details_id = db_manager.get_record_details_id(record_id, exercise_id, exercise_order)
            exercise_name = db_manager.get_exercise_name_by_id(exercise_id)
            return response_json(status_code, result={"record_details_id": record_details_id,
                                                      "exercise_name": exercise_name})
        else:
            return response_json(status_code)
    else:
        status_code = ERR_UNSUPPORT_REQUEST_METHOD
        return apology(error_message(status_code), status_code)


@app.route("/api/append_cardio_exercise", methods=["GET", "POST"])
@login_required
def append_cardio_exercise():
    if request.method == "POST":
        # user id
        user_id = session["user_id"]

        # Record date
        record_date_str = request.form["exercise_date"]
        if not record_date_str:
            return response_json(ERR_RECORD_DATE_EMPTY)
        record_date = exercise_date_str_to_date(record_date_str)
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

        status_code = appen_cardio_exercise_record(db_manager, user_id, record_date, exercise_id, exercise_hours,
                                                   exercise_minutes, exercise_seconds)
        if status_code == ERR_SUCCESS:
            record_id = db_manager.get_record_id(user_id, record_date)
            exercise_orders = db_manager.get_record_details_orders(record_id)
            exercise_order = max(exercise_orders)
            record_details_id = db_manager.get_record_details_id(record_id, exercise_id, exercise_order)
            exercise_name = db_manager.get_exercise_name_by_id(exercise_id)
            return response_json(status_code, result={"record_details_id": record_details_id,
                                                      "exercise_name": exercise_name})
        else:
            return response_json(status_code)
    else:
        status_code = ERR_UNSUPPORT_REQUEST_METHOD
        return apology(error_message(status_code), status_code)

@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    if request.method == "POST":
        return render_template("record.html")
    else:
        strength_muscle_group_captions = sorted(db_manager.get_strength_muscle_groups())
        strength_muscle_group_names = []
        for caption in strength_muscle_group_captions:
            name = validate_string(caption)
            strength_muscle_group_names.append(name)
        if len(strength_muscle_group_captions) != len(strength_muscle_group_names):
            raise Exception("count of muscle group captions and names are not equal")

        if len(strength_muscle_group_captions) > 0:
            strength_exercise_ids_names = db_manager.get_exercise_ids_names_by_muscle_group(strength_muscle_group_captions[0])
            sorted(strength_exercise_ids_names, key=lambda token: token[1])
            strength_exercise_ids = []
            strength_exercise_names = []
            for token in strength_exercise_ids_names:
                strength_exercise_ids.append(token[0])
                strength_exercise_names.append(token[1])
        else:
            strength_exercise_ids = []
            strength_exercise_names = []
        if len(strength_exercise_ids) != len(strength_exercise_names):
            raise Exception("count of exercise ids and names are not equal")

        cardio_exercise_ids_names = db_manager.get_cardio_exercise_ids_names()
        sorted(cardio_exercise_ids_names, key=lambda token: token[1])
        cardio_exercise_ids = []
        cardio_exercise_names = []
        for token in cardio_exercise_ids_names:
            cardio_exercise_ids.append(token[0])
            cardio_exercise_names.append(token[1])

        return render_template("record.html", strength_muscle_group_captions=strength_muscle_group_captions,
                               strength_muscle_group_names=strength_muscle_group_names,
                               strength_exercise_ids=strength_exercise_ids,
                               strength_exercise_names=strength_exercise_names,
                               cardio_exercise_ids=cardio_exercise_ids,
                               cardio_exercise_names=cardio_exercise_names)

def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)
