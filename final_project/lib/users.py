import re
import sqlite3
from .error_codes import *
from .fitbook_db import *
from werkzeug.security import check_password_hash, generate_password_hash

MIN_LEN_USERNAME = 5
MAX_LEN_USERNAME = 15
MIN_LEN_PASSWORD = 5
MAX_LEN_PASSWORD = 15


# return error code
def is_username_valid(username):
    # Check username is not None
    if not username:
        return ERR_USERNAME_EMPTY

    # Check username is string
    if not isinstance(username, str):
        return ERR_UNSUPPORT_DATA_TYPE

    # Check length
    if len(username) < MIN_LEN_USERNAME or len(username) > MAX_LEN_USERNAME:
        return ERR_USERNAME_LEN_INVALID

    # Check characters
    pattern = "[a-zA-Z0-9_]"
    for c in username:
        found = re.search(pattern, c)
        if not found:
            return ERR_USERNAME_ILLEGAL_CHAR

    return ERR_SUCCESS


# return error code
def is_password_valid(password):
    # Check password is not None
    if not password:
        return ERR_PASSWORD_EMPTY

    # Check password is string
    if not isinstance(password, str):
        return ERR_UNSUPPORT_DATA_TYPE

    # Check length
    if len(password) < MIN_LEN_PASSWORD or len(password) > MAX_LEN_PASSWORD:
        return ERR_PASSWORD_LEN_INVALID

    # Check characters
    pattern = "[a-zA-Z0-9]"
    for c in password:
        found = re.search(pattern, c)
        if not found:
            return ERR_PASSWORD_ILLEGAL_CHAR

    return ERR_SUCCESS


# return error code
def is_register_info_valid(db, username, password, confirmation):
    if not isinstance(db, sqlite3.Connection):
        raise Exception("db is not a database")

    # Check username follows format
    code = is_username_valid(username)
    if code != ERR_SUCCESS:
        return code
    # Check password follow format
    code = is_password_valid(password)
    if code != ERR_SUCCESS:
        return code
    # Check password and confirmation are match
    if password != confirmation:
        return ERR_PASSWORD_CONFIRM_UNMATCH
    # Check register information is valid in database
    if username_exist(db, username):
        return ERR_USERNAME_REPEAT
    return ERR_SUCCESS


# get password hash
def get_password_hash(password):
    return generate_password_hash(password)


# check password hash
def password_hash_correct(password_hash, password):
    return check_password_hash(password_hash, password)


def register_user(db, username, password):
    if not isinstance(db, sqlite3.Connection):
        raise Exception("db is not a database")

    code = is_username_valid(username)
    if code != ERR_SUCCESS:
        return code
    code = is_password_valid(password)
    if code != ERR_SUCCESS:
        return code
    hash = get_password_hash(password)
    add_user(db, username, hash)
    return ERR_SUCCESS


def login_user(db, username, password):
    if not username:
        return ERR_USERNAME_EMPTY
    if not password:
        return ERR_PASSWORD_EMPTY
    if not isinstance(db, sqlite3.Connection):
        raise Exception("database manager is not FitBookDB")
    if not isinstance(username, str):
        return ERR_UNSUPPORT_DATA_TYPE
    if not isinstance(password, str):
        return ERR_UNSUPPORT_DATA_TYPE

    # Check user exist
    if not username_exist(db, username):
        return ERR_USERNAME_NOT_EXIST

    # Check password correct
    user_hash = get_user_hash(db, username)
    if not password_hash_correct(user_hash, password):
        return ERR_PASSWORD_INCORRECT

    return ERR_SUCCESS