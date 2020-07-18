import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# self-defined library
from lib.helpers import apology, login_required, response_json
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


@app.route("/register_check", methods=["GET", "POST"])
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


@app.route("/login_check", methods=["GET", "POST"])
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


def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)
