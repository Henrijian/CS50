ERR_SUCCESS = 0
ERR_UNSUPPORT_REQUEST_METHOD = 1
ERR_UNSUPPORT_DATA_TYPE = 2
ERR_USERNAME_EMPTY = 3
ERR_USERNAME_LEN_INVALID = 4
ERR_USERNAME_ILLEGAL_CHAR = 5
ERR_PASSWORD_EMPTY = 6
ERR_PASSWORD_LEN_INVALID = 7
ERR_PASSWORD_ILLEGAL_CHAR = 8
ERR_PASSWORD_CONFIRM_EMPTY = 9
ERR_PASSWORD_CONFIRM_UNMATCH = 10
ERR_USERNAME_REPEAT = 11
ERR_USERNAME_NOT_EXIST = 12
ERR_PASSWORD_INCORRECT = 13


def error_message(error_code):
    if error_code == ERR_SUCCESS:
        return "Success"
    elif error_code == ERR_UNSUPPORT_REQUEST_METHOD:
        return "Request method is not supported"
    elif error_code == ERR_UNSUPPORT_DATA_TYPE:
        return "Input data type is not supported"
    elif error_code == ERR_USERNAME_EMPTY:
        return "Username cannot be empty"
    elif error_code == ERR_USERNAME_LEN_INVALID:
        return "Username length is not valid"
    elif error_code == ERR_USERNAME_ILLEGAL_CHAR:
        return "Username includes invalid characters"
    elif error_code == ERR_PASSWORD_EMPTY:
        return "Password cannot be empty"
    elif error_code == ERR_PASSWORD_LEN_INVALID:
        return "Password length is not valid"
    elif error_code == ERR_PASSWORD_ILLEGAL_CHAR:
        return "Password includes invalid characters"
    elif error_code == ERR_PASSWORD_CONFIRM_EMPTY:
        return "Password confirmation cannot be empty"
    elif error_code == ERR_PASSWORD_CONFIRM_UNMATCH:
        return "Password and confirmation are not match"
    elif error_code == ERR_USERNAME_REPEAT:
        return "Username already exist"
    elif error_code == ERR_USERNAME_NOT_EXIST:
        return "Username does not exist"
    elif error_code == ERR_PASSWORD_INCORRECT:
        return "Password is not correct"
    else:
        return "Unknown error"
