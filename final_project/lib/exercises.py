import datetime
import sqlite3
from .error_codes import *
from .fitbook_db import *

EXERCISE_DATE_FMT = "%Y-%m-%d"
MAX_EXERCISE_SET_ORDER = 100
MAX_EXERCISE_WEIGHT = 1000
MAX_EXERCISE_REPS = 1000


class ExerciseSet:
    def __init__(self):
        self.order = 0
        self.weight = 0
        self.reps = 0
        self.sub_sets = ExerciseSets()

    def data(self):
        return {"order": self.order,
                "weight": self.weight,
                "reps": self.reps,
                "sub_sets": self.sub_sets.data()}


class ExerciseSets:
    def __init__(self):
        self.sets = []

    def __getitem__(self, idx):
        if idx <= len(self.sets):
            return self.sets[idx]
        else:
            raise IndexError

    def append_set(self, order, weight, reps):
        if not (isinstance(order, int) and isinstance(weight, int) and isinstance(reps, int)):
            return -1
        set = ExerciseSet()
        set.order = order
        set.weight = weight
        set.reps = reps
        self.sets.append(set)
        return len(self.sets) - 1

    def append_sub_set(self, set_idx, order, weight, reps):
        if not (isinstance(set_idx, int) and isinstance(order, int) and
                isinstance(weight, int) and isinstance(reps, int)):
            return -1
        for idx, set in enumerate(self.sets):
            if idx == set_idx:
                set.sub_sets.append_set(order, weight, reps)
                return idx
        return -1

    def data(self):
        data = []
        for set in self.sets:
            set_data = set.data()
            data.append(set_data)
        return data

    def sort_by_order(self):
        self.sets = sorted(self.sets, key=lambda set: set.order)

    def find_by_order(self, order):
        for set in self.sets:
            if set.order == order:
                return set
        return None


class ExerciseTime:
    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

    def data(self):
        return {"hours": self.hours,
                "minutes": self.minutes,
                "seconds": self.seconds}


class ExerciseRecord:
    def __init__(self):
        self.record_details_id = -1
        self.exercise_type = ""
        self.muscle_group = ""
        self.exercise_name = ""
        self.exercise_sets = ExerciseSets()
        self.exercise_time = ExerciseTime()

    def data(self):
        return {
            "record_details_id": self.record_details_id,
            "exercise_type": self.exercise_type,
            "muscle_group": self.muscle_group,
            "exercise_name": self.exercise_name,
            "exercise_sets": self.exercise_sets.data(),
            "exercise_time": self.exercise_time.data()
        }


class ExerciseRecords:
    def __init__(self):
        self.records = []

    def __getitem__(self, idx):
        if idx <= len(self.records):
            return self.records[idx]
        else:
            raise IndexError

    def data(self):
        data = []
        for record in self.records:
            record_data = record.data()
            data.append(record_data)
        return data

    def append(self, exercise_record):
        self.records.append(exercise_record)


def exercise_date_str_to_date(date_str):
    if not isinstance(date_str, str):
        return None
    try:
        return datetime.datetime.strptime(date_str, EXERCISE_DATE_FMT)
    except:
        return None


def is_exercise_set_valid(set_order, set_weight, set_reps):
    # check order
    try:
        set_order = int(set_order)
    except:
        return ERR_EXERCISE_SET_ORDER_INVALID
    if not (0 < set_order < MAX_EXERCISE_SET_ORDER):
        return ERR_EXERCISE_SET_ORDER_INVALID

    # check weight
    try:
        set_weight = int(set_weight)
    except:
        return ERR_EXERCISE_SET_WEIGHT_INVALID
    if not (0 < set_weight < MAX_EXERCISE_WEIGHT):
        return ERR_EXERCISE_SET_WEIGHT_INVALID

    # check reps
    try:
        set_reps = int(set_reps)
    except:
        return ERR_EXERCISE_SET_REPS_INVALID
    if not (0 < set_reps < MAX_EXERCISE_REPS):
        return ERR_EXERCISE_SET_REPS_INVALID

    return ERR_SUCCESS


def append_strength_exercise_record(db, user_id, record_date, exercise_id, exercise_sets):
    # db manager
    if not isinstance(db, sqlite3.Connection):
        raise Exception("db is not a database")

    # User id
    if not user_id_exist(db, user_id):
        return ERR_USER_ID_NOT_EXIST

    # Record date
    if not record_date:
        return ERR_RECORD_DATE_EMPTY
    if not isinstance(record_date, datetime.datetime):
        return ERR_RECORD_DATE_INVALID

    # Exercise id
    if not exercise_id:
        return ERR_EXERCISE_ID_EMPTY
    exercise_name = get_exercise_name_by_id(db, exercise_id)
    if not exercise_name:
        return ERR_EXERCISE_ID_INVALID

    # Exercise type
    exercise_type = get_exercise_type_by_id(db, exercise_id)
    if not exercise_type == EXERCISE_TYPE_STRENGTH:
        return ERR_EXERCISE_TYPE_INVALID

    # Exercise sets
    if not isinstance(exercise_sets, ExerciseSets):
        return ERR_EXERCISE_SETS_INVALID
    if len(exercise_sets.sets) == 0:
        return ERR_EXERCISE_SETS_EMPTY

    # Get record id
    record_id = get_record_id(db, user_id, record_date)
    if record_id <= 0:
        add_record_id(db, user_id, record_date)
        record_id = get_record_id(db, user_id, record_date)
        if record_id <= 0:
            raise Exception("Add record to database failed")

    # Get exercise order
    exercise_orders = []
    record_details_ids = get_record_details_ids(db, record_id)
    for rdid in record_details_ids:
        exercise_order = get_record_details_exercise_order(db, rdid)
        exercise_orders.append(exercise_order)
    if exercise_orders:
        exercise_order = max(exercise_orders) + 1
    else:
        exercise_order = 1

    # Add record details
    add_record_details(db, record_id, exercise_id, exercise_order)
    record_details_id = get_record_details_id(db, record_id, exercise_id, exercise_order)
    if record_details_id <= 0:
        raise Exception("Add record details to database failed")

    # Add strength records
    for idx, set in enumerate(exercise_sets):
        set_order = idx + 1
        main_inset_order = 1
        main_weight = set.weight
        main_reps = set.reps
        add_strength_record(db, record_details_id, set_order, main_inset_order, main_weight, main_reps)
        if get_strength_record_id(db, record_details_id, set_order, main_inset_order, main_weight,
                                  main_reps) <= 0:
            raise Exception("Add strength record to database failed")
        for sub_idx, sub_set in enumerate(set.sub_sets):
            sub_inset_order = main_inset_order + sub_idx + 1
            sub_weight = sub_set.weight
            sub_reps = sub_set.reps
            add_strength_record(db, record_details_id, set_order, sub_inset_order, sub_weight, sub_reps)
            if get_strength_record_id(db, record_details_id, set_order, sub_inset_order, sub_weight, sub_reps) <= 0:
                raise Exception("Add sub strength record to database failed")

    return ERR_SUCCESS


def appen_cardio_exercise_record(db, user_id, record_date, exercise_id, exercise_hours,
                                 exercise_minutes, exercise_seconds):
    if not isinstance(db, sqlite3.Connection):
        raise Exception("db is not a database")

    # User id
    if not user_id_exist(db, user_id):
        return ERR_USER_ID_NOT_EXIST

    # Record date
    if not record_date:
        return ERR_RECORD_DATE_EMPTY
    if not isinstance(record_date, datetime.datetime):
        return ERR_RECORD_DATE_INVALID

    # Exercise id
    if not exercise_id:
        return ERR_EXERCISE_ID_EMPTY
    exercise_name = get_exercise_name_by_id(db, exercise_id)
    if not exercise_name:
        return ERR_EXERCISE_ID_INVALID

    # Exercise hours
    if exercise_hours:
        try:
            exercise_hours = int(exercise_hours)
        except:
            return ERR_EXERCISE_HOURS_INVALID
        if (0 > exercise_hours) or (exercise_hours > 99):
            return ERR_EXERCISE_HOURS_INVALID
    else:
        exercise_hours = 0

    # Exercise minutes
    if exercise_minutes:
        try:
            exercise_minutes = int(exercise_minutes)
        except:
            return ERR_EXERCISE_MINUTES_INVALID
        if (0 > exercise_minutes) or (exercise_minutes > 59):
            return ERR_EXERCISE_MINUTES_INVALID
    else:
        exercise_minutes = 0

    # Exercise seconds
    if exercise_seconds:
        try:
            exercise_seconds = int(exercise_seconds)
        except:
            return ERR_EXERCISE_SECONDS_INVALID
        if (0 > exercise_seconds) or (exercise_seconds > 59):
            return ERR_EXERCISE_SECONDS_INVALID
    else:
        exercise_seconds = 0

    if (exercise_hours == 0) and (exercise_minutes == 0) and (exercise_seconds == 0):
        return ERR_EXERCISE_TIME_NOT_EXIST

    # Exercise type
    exercise_type = get_exercise_type_by_id(db, exercise_id)
    if not exercise_type == EXERCISE_TYPE_CARDIO:
        return ERR_EXERCISE_TYPE_INVALID

    # Get record id
    record_id = get_record_id(db, user_id, record_date)
    if record_id <= 0:
        add_record_id(db, user_id, record_date)
        record_id = get_record_id(db, user_id, record_date)
        if record_id <= 0:
            raise Exception("Add record to database failed")

    # Get exercise order
    exercise_orders = get_record_details_orders(db, record_id)
    if exercise_orders:
        exercise_order = max(exercise_orders) + 1
    else:
        exercise_order = 1

    # Add record details
    add_record_details(db, record_id, exercise_id, exercise_order)
    record_details_id = get_record_details_id(db, record_id, exercise_id, exercise_order)
    if record_details_id <= 0:
        raise Exception("Add record details to database failed")

    # Add to database
    add_cardio_record(db, record_details_id, exercise_hours, exercise_minutes, exercise_seconds)
    if not cardio_record_exist(db, record_details_id, exercise_hours, exercise_minutes, exercise_seconds):
        raise Exception("Add cardio record to database failed")

    return ERR_SUCCESS


def get_exercise_record(db, record_details_id):
    if not isinstance(db, sqlite3.Connection):
        raise Exception("database manager is not FitBookDB")

    if not record_details_id_exist(db, record_details_id):
        raise Exception("record details id does not exist")

    # Get exercise record
    exercise_record = ExerciseRecord()
    exercise_record.record_details_id = record_details_id

    # Get exercise id
    exercise_id = get_exercise_id_by_record_details_id(db, record_details_id)
    if exercise_id <= 0:
        raise Exception("Cannot get exercise id by record details id(%s)" % record_details_id)

    # Get exercise type
    exercise_type = get_exercise_type_by_id(db, exercise_id)
    if not exercise_type:
        raise Exception("Cannot get exercise type by id(%d)" % exercise_id)
    exercise_record.exercise_type = exercise_type

    # Get muscle group
    muscle_group = get_exercise_muscle_group_by_id(db, exercise_id)
    if not muscle_group:
        raise Exception("Cannot get muscle group by id(%d)" % exercise_id)
    exercise_record.muscle_group = muscle_group

    # Get exercise name
    exercise_name = get_exercise_name_by_id(db, exercise_id)
    if not exercise_name:
        raise Exception("Cannot get exercise name by id(%d)" % exercise_id)
    exercise_record.exercise_name = exercise_name

    if exercise_type == EXERCISE_TYPE_STRENGTH:
        # Get exercise sets
        strength_record_ids = get_strength_records_ids_by_record_details_id(db, record_details_id)
        for strength_record_id in strength_record_ids:
            set_order = get_set_order_by_strength_record_id(db, strength_record_id)
            if set_order <= 0:
                raise Exception("cannot get set order from strength record id(%d)" % strength_record_id)
            inset_order = get_inset_order_by_strength_record_id(db, strength_record_id)
            if inset_order <= 0:
                raise Exception("cannot get inset order from strength record id(%d)" % strength_record_id)
            weight = get_weight_by_strength_record_id(db, strength_record_id)
            reps = get_reps_by_strength_record_id(db, strength_record_id)
            if inset_order > 1:
                for exercise_set in exercise_record.exercise_sets:
                    if exercise_set.order == set_order:
                        exercise_set.sub_sets.append_set(inset_order, weight, reps)
                        exercise_set.sub_sets.sort_by_order()
                        break
            else:
                exercise_record.exercise_sets.append_set(set_order, weight, reps)
        exercise_record.exercise_sets.sort_by_order()
    elif exercise_type == EXERCISE_TYPE_CARDIO:
        # Get cardio exercise time
        hours = get_hours_by_record_details_id(db, record_details_id)
        minutes = get_minutes_by_record_details_id(db, record_details_id)
        seconds = get_seconds_by_record_details_id(db, record_details_id)
        if hours < 0 or minutes < 0 or seconds < 0:
            raise Exception("cannot get cardio exercise time from record details id(%d)" % record_details_id)
        exercise_record.exercise_time.hours = hours
        exercise_record.exercise_time.minutes = minutes
        exercise_record.exercise_time.seconds = seconds
    else:
        raise Exception("Unknown exercise type(%s)" % exercise_type)
    return exercise_record


def get_exercise_records(db, user_id, record_date):
    if not isinstance(db, sqlite3.Connection):
        raise Exception("database manager is not FitBookDB")
    if not user_id:
        raise Exception("Cannot get exercise records by empty user id")
    if not isinstance(record_date, datetime.datetime):
        raise Exception("Invalid type of record date")

    exercise_records = ExerciseRecords()

    # Get record id
    record_id = get_record_id(db, user_id, record_date)
    if record_id <= 0:
        return exercise_records

    # Get record details ids and exercise ids and orders
    rdids_eids_orders = get_rdids_eids_orders_by_record_id(db, record_id)
    if not rdids_eids_orders:
        return exercise_records
    sorted(rdids_eids_orders, key=lambda token: token[2])
    record_details_ids = []
    exercise_ids = []
    exercise_orders = []
    for token in rdids_eids_orders:
        record_details_ids.append(token[0])
        exercise_ids.append(token[1])
        exercise_orders.append(token[2])

    # Get exercise records
    for i in range(len(record_details_ids)):
        record_details_id = record_details_ids[i]
        exercise_record = get_exercise_record(db, record_details_id)
        exercise_records.append(exercise_record)
    return exercise_records
