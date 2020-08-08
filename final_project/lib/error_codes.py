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
ERR_MUSCLE_GROUP_EMPTY = 14
ERR_MUSCLE_GROUP_NOT_EXIST = 15
ERR_EXERCISE_ID_EMPTY = 16
ERR_EXERCISE_ID_INVALID = 17
ERR_EXERCISE_NAME_NOT_EXIST = 18
ERR_RECORD_DATE_EMPTY = 19
ERR_RECORD_DATE_INVALID = 20
ERR_EXERCISE_SETS_EMPTY = 21
ERR_EXERCISE_SETS_INVALID = 22
ERR_EXERCISE_SET_ORDER_INVALID = 23
ERR_EXERCISE_SET_WEIGHT_INVALID = 24
ERR_EXERCISE_SET_REPS_INVALID = 25
ERR_EXERCISE_ORDER_EMPTY = 26
ERR_EXERCISE_ORDER_INVALID = 27
ERR_EXERCISE_DATE_EMPTY = 28
ERR_EXERCISE_DATE_INVALID = 29
ERR_EXERCISE_ID_NOT_EXIST = 30
ERR_RECORD_ID_NOT_EXIST = 31
ERR_RECORD_DETAILS_ID_NOT_EXIST = 32
ERR_EXERCISE_TIME_INVALID = 33
ERR_USER_ID_NOT_EXIST = 34
ERR_INTERNAL = 35
ERR_EXERCISE_TYPE_INVALID = 36
ERR_EXERCISE_HOURS_INVALID = 37
ERR_EXERCISE_MINUTES_INVALID = 38
ERR_EXERCISE_SECONDS_INVALID = 39

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
    elif error_code == ERR_MUSCLE_GROUP_EMPTY:
        return "Muscle group cannot be empty"
    elif error_code == ERR_MUSCLE_GROUP_NOT_EXIST:
        return "Muscle group does not exist"
    elif error_code == ERR_EXERCISE_ID_EMPTY:
        return "Exercise id cannot be empty"
    elif error_code == ERR_RECORD_DATE_EMPTY:
        return "Record date cannot be empty"
    elif error_code == ERR_RECORD_DATE_INVALID:
        return "Record date is not valid"
    elif error_code == ERR_EXERCISE_SETS_EMPTY:
        return "Exercise sets cannot be empty"
    elif error_code == ERR_EXERCISE_SETS_INVALID:
        return "Exercise sets are not valid"
    elif error_code == ERR_EXERCISE_SET_ORDER_INVALID:
        return "Exercise set order is not valid"
    elif error_code == ERR_EXERCISE_SET_WEIGHT_INVALID:
        return "Exercise set weight is not valid"
    elif error_code == ERR_EXERCISE_SET_REPS_INVALID:
        return "Exercise set repetitions is not valid"
    elif error_code == ERR_EXERCISE_ORDER_EMPTY:
        return "Exercise order cannot be empty"
    elif error_code == ERR_EXERCISE_ORDER_INVALID:
        return "Exercise order is not valid"
    elif error_code == ERR_EXERCISE_DATE_EMPTY:
        return "Exercise date cannot be empty"
    elif error_code == ERR_EXERCISE_DATE_INVALID:
        return "Exercise date is not valid"
    elif error_code == ERR_EXERCISE_ID_NOT_EXIST:
        return "Exercise id does not exist"
    elif error_code == ERR_RECORD_ID_NOT_EXIST:
        return "Record id does not exist"
    elif error_code == ERR_RECORD_DETAILS_ID_NOT_EXIST:
        return "Record details id does not exist"
    elif error_code == ERR_EXERCISE_TIME_INVALID:
        return "Exercise time is not valid"
    elif error_code == ERR_USER_ID_NOT_EXIST:
        return "User id does not exist"
    elif error_code == ERR_INTERNAL:
        return "Internal error happened"
    elif error_code == ERR_EXERCISE_TYPE_INVALID:
        return "Exercise type is not valid"
    elif error_code == ERR_EXERCISE_HOURS_INVALID:
        return "Exercise hours is not valid"
    elif error_code == ERR_EXERCISE_MINUTES_INVALID:
        return "Exercise minutes is not valid"
    elif error_code == ERR_EXERCISE_SECONDS_INVALID:
        return "Exercise seconds is not valid"
    else:
        return "Unknown error"
