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
from lib.users import is_register_info_valid, register_user, login_user

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


@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    if request.method == "POST":
        return render_template("record.html")
    else:
        muscle_groups = sorted(db_manager.get_muscle_groups())
        muscle_group_values_texts = []
        for muscle_group in muscle_groups:
            muscle_group_value = validate_string(muscle_group)
            muslce_group_text = muscle_group
            muslce_group_token = (muscle_group_value, muslce_group_text)
            muscle_group_values_texts.append(muslce_group_token)

        if len(muscle_groups) > 0:
            strength_exercise_ids_names = db_manager.get_exercise_ids_names_by_muscle_group(muscle_groups[0])
            strength_exercise_ids_names = sorted(strength_exercise_ids_names, key=lambda token: token[1])
        else:
            strength_exercise_ids_names = []
        cardio_exercise_ids_names = sorted(db_manager.get_cardio_exercise_ids_names())

        return render_template("record.html", muscle_group_values_texts=muscle_group_values_texts,
                               strength_exercise_ids_names=strength_exercise_ids_names,
                               cardio_exercise_ids_names=cardio_exercise_ids_names)

def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)
