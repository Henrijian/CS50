import os
import requests
import urllib.parse
import json
from flask import redirect, render_template, session, jsonify
from functools import wraps
from lib.error_codes import *
from lib.str_utils import *


def apology(message, code):
    return render_template("apology.html", message=message, code=code), code


def response_json(error_code, error_msg="", result=None):
    if not (isinstance(error_code, int)
            and isinstance(error_msg, str)):
        error_code = ERR_UNSUPPORT_DATA_TYPE
        error_msg = error_message(error_code)
        result = None
    if not error_msg:
        error_msg = error_message(error_code)

    base_json = {"error_code": error_code,
                 "error_message": error_msg,
                 "result": json.dumps(result)}
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


def validate_string(in_str):
    out_str = in_str.replace(" ", "_")
    out_str = remain_letter(out_str, ["_"])
    out_str = out_str.upper()
    return out_str
