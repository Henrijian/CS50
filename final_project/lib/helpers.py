import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session, jsonify
from functools import wraps
from lib.error_codes import *


def apology(message, code):
    return render_template("apology.html", message=message, code=code), code


def response_json(error_code):
    if not isinstance(error_code, int):
        error_code = ERR_UNSUPPORT_DATA_TYPE
    base_json = {"error_code": error_code,
                 "error_message": error_message(error_code)}
    return jsonify(base_json)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

