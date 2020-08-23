import sqlite3
import os
import datetime

USERS_TABLE = "users"
USERS_ID_COL = "id"
USERS_USERNAME_COL = "username"
USERS_HASH_COL = "hash"

EXERCISES_TABLE = "exercises"
EXERCISES_ID_COL = "id"
EXERCISES_NAME_COL = "name"
EXERCISES_MUSCLE_GROUP_COL = "muscle_group"
EXERCISES_TYPE_COL = "type"

MUSCLE_GROUPS_TABLE = "muscle_groups"
MUSCLE_GROUPS_NAME_COL = "name"

EXERCISE_TYPE_STRENGTH = "strength"
EXERCISE_TYPE_CARDIO = "cardio"

RECORDS_TABLE = "records"
RECORDS_ID_COL = "id"
RECORDS_UID_COL = "uid"
RECORDS_DATE_COL = "date"
RECORDS_DATE_FMT = "%Y-%m-%d"

RECORD_DETAILS_TABLE = "record_details"
RECORD_DETAILS_ID_COL = "id"
RECORD_DETAILS_RID_COL = "rid"
RECORD_DETAILS_EID_COL = "eid"
RECORD_DETAILS_ORDER_COL = "order"

STRENGTH_RECORDS_TABLE = "strength_records"
STRENGTH_RECORDS_ID_COL = "id"
STRENGTH_RECORDS_RDID_COL = "rdid"
STRENGTH_RECORDS_SET_ORDER_COL = "set_order"
STRENGTH_RECORDS_INSET_ORDER_COL = "inset_order"
STRENGTH_RECORDS_WEIGHT_COL = "weight"
STRENGTH_RECORDS_REPS_COL = "reps"

CARDIO_RECORDS_TABLE = "cardio_records"
CARDIO_RECORDS_RDID_COL = "rdid"
CARDIO_RECORDS_HRS_COL = "hours"
CARDIO_RECORDS_MINS_COL = "minutes"
CARDIO_RECORDS_SECS_COL = "seconds"

MAX_WEIGHT_RECORDS_TABLE = "max_weight_records"
MAX_WEIGHT_RECORDS_ID_COL = "id"
MAX_WEIGHT_RECORDS_RID_COL = "rid"
MAX_WEIGHT_RECORDS_EID_COL = "eid"
MAX_WEIGHT_RECORDS_WEIGHT_COL = "weight"

BODY_RECORDS_TABLE = "body_records"
BODY_RECORDS_ID_COL = "id"
BODY_RECORDS_RID_COL = "rid"
BODY_RECORDS_WEIGHT_COL = "weight"
BODY_RECORDS_MUSCLE_WEIGHT_COL = "muscle_weight"
BODY_RECORDS_FAT_RATE_COL = "fat_rate"

##################################################
# users table
##################################################
def get_usernames(db):
    sql = "SELECT %s FROM %s" % (USERS_USERNAME_COL, USERS_TABLE)
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    usernames = []
    for row in rows:
        usernames.append(row[USERS_USERNAME_COL])
    return usernames


def get_user_hash(db, username):
    username = username.lower()
    sql = "SELECT %s FROM %s WHERE %s=?" % (USERS_HASH_COL, USERS_TABLE, USERS_USERNAME_COL)
    cur = db.cursor()
    cur.execute(sql, (username,))
    user_hash = ""
    row = cur.fetchone()
    if row:
        user_hash = row[USERS_HASH_COL]
    return user_hash


def get_user_id(db, username):
    sql = "SELECT %s FROM %s WHERE %s=?" % (USERS_ID_COL, USERS_TABLE, USERS_USERNAME_COL)
    cur = db.cursor()
    cur.execute(sql, (username,))
    uid = -1
    row = cur.fetchone()
    if row:
        uid = row[USERS_ID_COL]
    return uid


def username_exist(db, username):
    username = username.lower()
    usernames = get_usernames(db)
    return username in usernames


def add_user(db, username, hash):
    username = username.lower()
    if username_exist(db, username):
        raise Exception("Username(%s) already exist" % username)

    sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (USERS_TABLE, USERS_USERNAME_COL, USERS_HASH_COL)
    cur = db.cursor()
    cur.execute(sql, (username, hash))
    if not cur.lastrowid:
        raise Exception("Add user(%s) to database failed" % username)
    db.commit()


def user_id_exist(db, user_id):
    sql = "SELECT * FROM %s WHERE %s=?" % (USERS_TABLE, USERS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    return len(rows) > 0


##################################################
# exercises table
##################################################
def exercise_id_exist(db, exercise_id):
    sql = "SELECT * FROM %s WHERE %s=?" % (EXERCISES_TABLE, EXERCISES_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_id,))
    rows = cur.fetchall()
    return len(rows) > 0


def get_exercise_names(db):
    sql = "SELECT %s FROM %s" % (EXERCISES_NAME_COL, EXERCISES_TABLE)
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    exercises = []
    for row in rows:
        exercises.append(row[EXERCISES_NAME_COL])
    return exercises


def get_exercise_name_by_id(db, exercise_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_id,))
    row = cur.fetchone()
    if row:
        exercise_name = row[EXERCISES_NAME_COL]
    else:
        exercise_name = ""
    return exercise_name


def get_exercise_type_by_id(db, exercise_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_TYPE_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_id,))
    row = cur.fetchone()
    if row:
        exercise_type = row[EXERCISES_TYPE_COL]
    else:
        exercise_type = ""
    return exercise_type


def get_exercise_muscle_group_by_id(db, exercise_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_id,))
    row = cur.fetchone()
    if row:
        muscle_group = row[EXERCISES_MUSCLE_GROUP_COL]
    else:
        muscle_group = ""
    return muscle_group


def get_exercise_names_by_muscle_group(db, muscle_group):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL)
    cur = db.cursor()
    cur.execute(sql, (muscle_group,))
    rows = cur.fetchall()
    names = []
    for row in rows:
        names.append(row[EXERCISES_NAME_COL])
    return names


def get_exercise_ids_by_muscle_group(db, muscle_group):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_ID_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL)
    cur = db.cursor()
    cur.execute(sql, (muscle_group,))
    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[EXERCISES_ID_COL])
    return ids


def get_exercise_ids_names_by_muscle_group(db, muscle_group):
    sql = "SELECT %s, %s FROM %s WHERE %s=?" % (EXERCISES_ID_COL, EXERCISES_NAME_COL, EXERCISES_TABLE,
                                                EXERCISES_MUSCLE_GROUP_COL)
    cur = db.cursor()
    cur.execute(sql, (muscle_group,))
    rows = cur.fetchall()
    exercises = []
    for row in rows:
        id_name_token = (row[EXERCISES_ID_COL], row[EXERCISES_NAME_COL])
        exercises.append(id_name_token)
    return exercises


def get_exercise_ids_names_by_type(db, exercise_type):
    sql = "SELECT %s, %s FROM %s WHERE %s=?" % (
        EXERCISES_ID_COL, EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_TYPE_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_type,))
    rows = cur.fetchall()
    exercises = []
    for row in rows:
        id_name_token = (row[EXERCISES_ID_COL], row[EXERCISES_NAME_COL])
        exercises.append(id_name_token)
    return exercises


def get_strength_exercise_ids_names(db):
    return get_exercise_ids_names_by_type(db, EXERCISE_TYPE_STRENGTH)


def get_cardio_exercise_ids_names(db):
    return get_exercise_ids_names_by_type(db, EXERCISE_TYPE_CARDIO)


def get_exercise_names_by_type(db, exercise_type):
    sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_TYPE_COL)
    cur = db.cursor()
    cur.execute(sql, (exercise_type,))
    rows = cur.fetchall()
    exercises = []
    for row in rows:
        exercises.append(row[EXERCISES_NAME_COL])
    return exercises


def get_cardio_exercise_names(db):
    return get_exercise_names_by_type(db, EXERCISE_TYPE_CARDIO)


def get_strength_exercise_names(db):
    return get_exercise_names_by_type(db, EXERCISE_TYPE_STRENGTH)


def get_strength_muscle_groups(db):
    sql = "SELECT %s FROM %s WHERE %s=? GROUP BY(%s)" % (EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TABLE,
                                                         EXERCISES_TYPE_COL, EXERCISES_MUSCLE_GROUP_COL)
    cur = db.cursor()
    cur.execute(sql, (EXERCISE_TYPE_STRENGTH,))
    muslce_groups = []
    rows = cur.fetchall()
    for row in rows:
        muslce_groups.append(row[EXERCISES_MUSCLE_GROUP_COL])
    return muslce_groups


def get_exercise_names_by_muscle_group_and_type(db, muscle_group, exercise_type):
    sql = "SELECT %s FROM %s WHERE %s=? AND %s=?" % (
        EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TYPE_COL)
    cur = db.cursor()
    cur.execute(sql, (muscle_group, exercise_type))
    rows = cur.fetchall()
    exercises = []
    for row in rows:
        exercises.append(row[EXERCISES_NAME_COL])
    return exercises


def get_strength_exercise_names_by_muscle_group(db, muscle_group):
    return get_exercise_names_by_muscle_group_and_type(db, muscle_group, EXERCISE_TYPE_STRENGTH)


##################################################
# muscle_groups table
##################################################
def get_muscle_groups(db):
    sql = "SELECT %s FROM %s" % (MUSCLE_GROUPS_NAME_COL, MUSCLE_GROUPS_TABLE)
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    muscle_groups = []
    for row in rows:
        muscle_groups.append(row[MUSCLE_GROUPS_NAME_COL])
    return muscle_groups


##################################################
# records table
##################################################
def update_record_details_exercise(db, rdid, eid):
    if not record_details_id_exist(db, rdid):
        raise Exception("Record details id(%s) does not exist" % rdid)
    sql = "UPDATE %s SET %s=? WHERE %s=?" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_EID_COL, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (eid, rdid))
    if cur.rowcount < 1:
        raise Exception("Update exercise(%s) to record details id(%s) failed" % (eid, rdid))
    db.commit()


def add_record_id(db, uid, date):
    if get_record_id(db, uid, date) > 0:
        raise Exception("Record id already exist!")

    if not isinstance(date, datetime.datetime):
        return -1
    date_str = date.strftime(RECORDS_DATE_FMT)

    sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (RECORDS_TABLE, RECORDS_UID_COL, RECORDS_DATE_COL)
    cur = db.cursor()
    cur.execute(sql, (uid, date_str))
    if not cur.lastrowid:
        raise Exception("Add record(uid:%s, date: %s) to database failed" % (uid, date_str))
    db.commit()


def get_record_id(db, uid, date):
    if not isinstance(date, datetime.datetime):
        return -1
    date_str = date.strftime(RECORDS_DATE_FMT)
    sql = "SELECT %s FROM %s WHERE %s=? AND %s=?" % (RECORDS_ID_COL, RECORDS_TABLE, RECORDS_UID_COL,
                                                     RECORDS_DATE_COL)
    cur = db.cursor()
    cur.execute(sql, (uid, date_str))
    row = cur.fetchone()
    if row:
        rid = row[RECORDS_ID_COL]
    else:
        rid = -1
    return rid


def get_record_ids_by_range(db, uid, start_date, end_date):
    if not isinstance(start_date, datetime.datetime):
        raise Exception("start_date is not datetime type!")
    if not isinstance(end_date, datetime.datetime):
        raise Exception("end_date is not datetime type!")
    if not (start_date < end_date):
        raise Exception("start date is not early than end date")
    start_date_str = start_date.strftime(RECORDS_DATE_FMT)
    end_date_str = end_date.strftime(RECORDS_DATE_FMT)
    sql_fmt = """SELECT %s FROM %s 
                 WHERE uid=? 
                 AND strftime(\"%s\", \"%s\") <= strftime(\"%s\", date) 
                 AND strftime(\"%s\", date) < strftime(\"%s\", \"%s\");"""
    sql = sql_fmt % (RECORDS_ID_COL, RECORDS_TABLE, RECORDS_DATE_FMT, start_date_str, RECORDS_DATE_FMT,
                     RECORDS_DATE_FMT, RECORDS_DATE_FMT, end_date_str)
    cur = db.cursor()
    cur.execute(sql, (uid,))
    ids = []
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[RECORDS_ID_COL])
    return ids


def get_record_date_by_id(db, record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (RECORDS_DATE_COL, RECORDS_TABLE, RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_id,))
    row = cur.fetchone()
    date = None
    if row:
        date_str = row[RECORDS_DATE_COL]
        date = datetime.datetime.strptime(date_str, RECORDS_DATE_FMT)
    return date

##################################################
# record_details table
##################################################
def record_details_record_id_exist(db, record_id):
    sql = "SELECT * FROM %s WHERE %s=?" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_id,))
    rows = cur.fetchall()
    return len(rows) > 0


def record_details_id_exist(db, record_details_id):
    sql = "SELECT * FROM %s WHERE %s=?" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    rows = cur.fetchall()
    return len(rows) > 0


def add_record_details(db, rid, eid, order):
    if get_record_details_id(db, rid, eid, order) > 0:
        raise Exception("Record details already exist!")

    sql = "INSERT INTO %s (%s, %s, \"%s\") VALUES(?, ?, ?)" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL,
                                                               RECORD_DETAILS_EID_COL, RECORD_DETAILS_ORDER_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, order))
    if not cur.lastrowid:
        raise Exception("Add record details(rid:%s, eid: %s, order: %s) to database failed" % (rid, eid, order))
    db.commit()


def delete_record_details(db, rdid):
    if not record_details_id_exist(db, rdid):
        raise Exception("Record details does not exist")

    # delete rdid from strength exercise record table
    sql = "DELETE FROM %s WHERE %s=?" % (STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid,))
    db.commit()
    # delete rdid from cardio exercise record table
    sql = "DELETE FROM %s WHERE %s=?" % (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid,))
    db.commit()
    # delete rdid from record record details table
    sql = "DELETE FROM %s WHERE %s=?" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid,))
    if cur.rowcount < 1:
        raise Exception("Delete record details by record details id(%s) failed" % rdid)
    db.commit()


def get_record_details_id(db, rid, eid, order):
    sql = "SELECT %s FROM %s WHERE %s=? AND %s=? AND \"%s\"=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_TABLE,
                                                                  RECORD_DETAILS_RID_COL, RECORD_DETAILS_EID_COL,
                                                                  RECORD_DETAILS_ORDER_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, order))
    row = cur.fetchone()
    if row:
        rdid = row[RECORD_DETAILS_ID_COL]
    else:
        rdid = -1
    return rdid


def get_record_details_ids(db, rid):
    sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    rdids = []
    rows = cur.fetchall()
    for row in rows:
        rdids.append(row[RECORD_DETAILS_ID_COL])
    return rdids


def get_record_details_orders(db, rid):
    sql = "SELECT \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    orders = []
    rows = cur.fetchall()
    for row in rows:
        orders.append(row[RECORD_DETAILS_ORDER_COL])
    return orders


def get_record_details_exercise_order(db, record_details_id):
    sql = "SELECT \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        order = row[RECORD_DETAILS_ORDER_COL]
    else:
        order = -1
    return order


def get_exercise_id_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_EID_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        eid = row[RECORD_DETAILS_EID_COL]
    else:
        eid = -1
    return eid


def get_exercise_order_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        order = row[RECORD_DETAILS_ORDER_COL]
    else:
        order = -1
    return order


def get_exercise_ids_orders_by_record_id(db, record_id):
    sql = "SELECT %s, %s FROM %s WHERE %s=?" % (RECORD_DETAILS_EID_COL, RECORD_DETAILS_ORDER_COL,
                                                RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_id,))
    exercise_ids_orders = []
    rows = cur.fetchall()
    for row in rows:
        exercise_ids_orders.append((row[RECORD_DETAILS_EID_COL], row[RECORD_DETAILS_ORDER_COL]))
    return exercise_ids_orders


def get_rdids_eids_orders_by_record_id(db, record_id):
    sql = "SELECT %s, %s, \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_EID_COL,
                                                        RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE,
                                                        RECORD_DETAILS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_id,))
    rdids_eids_orders = []
    rows = cur.fetchall()
    for row in rows:
        rdids_eids_orders.append((row[RECORD_DETAILS_ID_COL], row[RECORD_DETAILS_EID_COL],
                                  row[RECORD_DETAILS_ORDER_COL]))
    return rdids_eids_orders


##################################################
# strength_records table
##################################################
def add_strength_record(db, rdid, set_order, inset_order, weight, reps):
    if get_strength_record_id(db, rdid, set_order, inset_order, weight, reps) > 0:
        raise Exception("Strength record already exist!")
    sql = "INSERT INTO %s (%s, %s, %s, %s, %s) VALUES(?, ?, ?, ?, ?)" % \
          (STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL, STRENGTH_RECORDS_SET_ORDER_COL,
           STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_WEIGHT_COL, STRENGTH_RECORDS_REPS_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid, set_order, inset_order, weight, reps))
    if not cur.lastrowid:
        raise Exception(
            "Add strength record (rdid:%s, set_order: %s, inset_order: %s, weight: %s, reps: %s) to database failed" %
            (rdid, set_order, inset_order, weight, reps))
    db.commit()


def delete_strength_record_by_rdid(db, rdid):
    sql = "DELETE FROM %s WHERE %s=?" % (STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid,))
    if cur.rowcount < 1:
        raise Exception("Delete strength record by record details id(%s) failed" % rdid)
    db.commit()


def get_strength_record_id(db, rdid, set_order, inset_order, weight, reps):
    sql = "SELECT %s FROM %s WHERE %s=? AND %s=? AND %s=? AND %s=? AND %s=?" % \
          (STRENGTH_RECORDS_ID_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL,
           STRENGTH_RECORDS_SET_ORDER_COL, STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_WEIGHT_COL,
           STRENGTH_RECORDS_REPS_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid, set_order, inset_order, weight, reps))
    row = cur.fetchone()
    if row:
        srid = row[STRENGTH_RECORDS_ID_COL]
    else:
        srid = -1
    return srid


def get_strength_records_ids_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_ID_COL, STRENGTH_RECORDS_TABLE,
                                            STRENGTH_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    ids = []
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[STRENGTH_RECORDS_ID_COL])
    return ids


def get_set_order_by_strength_record_id(db, strength_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (
        STRENGTH_RECORDS_SET_ORDER_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (strength_record_id,))
    row = cur.fetchone()
    if row:
        set_order = row[STRENGTH_RECORDS_SET_ORDER_COL]
    else:
        set_order = -1
    return set_order


def get_inset_order_by_strength_record_id(db, strength_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (
        STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (strength_record_id,))
    row = cur.fetchone()
    if row:
        inset_order = row[STRENGTH_RECORDS_INSET_ORDER_COL]
    else:
        inset_order = -1
    return inset_order


def get_weight_by_strength_record_id(db, strength_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (
        STRENGTH_RECORDS_WEIGHT_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (strength_record_id,))
    row = cur.fetchone()
    if row:
        weight = row[STRENGTH_RECORDS_WEIGHT_COL]
    else:
        weight = -1
    return weight


def get_reps_by_strength_record_id(db, strength_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_REPS_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (strength_record_id,))
    row = cur.fetchone()
    if row:
        reps = row[STRENGTH_RECORDS_REPS_COL]
    else:
        reps = -1
    return reps


##################################################
# cardio_records table
##################################################
def add_cardio_record(db, rdid, hours, minutes, seconds):
    if cardio_record_exist(db, rdid, hours, minutes, seconds) > 0:
        raise Exception("Cardio record already exist!")
    sql = "INSERT INTO %s (%s, %s, %s, %s) VALUES(?, ?, ?, ?)" % (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL,
                                                                  CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_MINS_COL,
                                                                  CARDIO_RECORDS_SECS_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid, hours, minutes, seconds))
    if not cur.lastrowid:
        raise Exception("Add cardio record (rdid:%s, hours: %s, minutes: %s, seconds: %s) to database failed" %
                        (rdid, hours, minutes, seconds))
    db.commit()


def delete_cardio_record_by_rdid(db, rdid):
    sql = "DELETE FROM %s WHERE %s=?" % (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid,))
    if cur.rowcount < 1:
        raise Exception("Delete cardio record by record details id(%s) failed" % rdid)
    db.commit()


def cardio_record_exist(db, rdid, hours, minutes, seconds):
    sql = "SELECT * FROM %s WHERE %s=? AND %s=? AND %s=? AND %s=?" % (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL,
                                                                      CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_MINS_COL,
                                                                      CARDIO_RECORDS_SECS_COL)
    cur = db.cursor()
    cur.execute(sql, (rdid, hours, minutes, seconds))
    rows = cur.fetchall()
    return len(rows) > 0


def get_hours_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        hours = row[CARDIO_RECORDS_HRS_COL]
    else:
        hours = -1
    return hours


def get_minutes_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_MINS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        minutes = row[CARDIO_RECORDS_MINS_COL]
    else:
        minutes = -1
    return minutes


def get_seconds_by_record_details_id(db, record_details_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_SECS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_details_id,))
    row = cur.fetchone()
    if row:
        seconds = row[CARDIO_RECORDS_SECS_COL]
    else:
        seconds = -1
    return seconds


##################################################
# max_weight_records table
##################################################
def add_max_weight_record(db, rid, eid, weight):
    if max_weight_record_exist(db, rid, eid, weight):
        raise Exception("Max weight record already exist!")

    sql = "INSERT INTO %s (%s, %s, %s) VALUES(?, ?, ?)" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_RID_COL,
                                                           MAX_WEIGHT_RECORDS_EID_COL, MAX_WEIGHT_RECORDS_WEIGHT_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, weight))
    if not cur.lastrowid:
        raise Exception("Add max weight record(rid:%s, eid: %s, weight: %s) to database failed" % (rid, eid, weight))
    db.commit()


def update_max_weight_record(db, id, rid, eid, weight):
    if not max_weight_record_id_exist(db, id):
        raise Exception("Max weight record id(%s) does not exist" % id)
    sql = "UPDATE %s SET %s=?, %s=?, %s=? WHERE %s=?" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_RID_COL,
                                                         MAX_WEIGHT_RECORDS_EID_COL, MAX_WEIGHT_RECORDS_WEIGHT_COL,
                                                         MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, weight, id))
    if cur.rowcount < 1:
        raise Exception("Update max weight record(%s) failed, rid: %s, eid: %s, weight: %s" % (id, rid, eid, weight))
    db.commit()


def delete_max_weight_record(db, id):
    if not max_weight_record_id_exist(db, id):
        raise Exception("Max weight record does not exist")

    # delete max weight record
    sql = "DELETE FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (id,))
    if cur.rowcount < 1:
        raise Exception("Delete max weight record by max weight record id(%s) failed" % id)
    db.commit()


def max_weight_record_id_exist(db, max_weight_record_id):
    sql = "SELECT * FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (max_weight_record_id,))
    rows = cur.fetchall()
    return len(rows) > 0


def max_weight_record_exist(db, rid, eid, weight):
    sql = "SELECT * FROM %s WHERE %s=? AND %s=? AND %s=?" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_RID_COL,
                                                             MAX_WEIGHT_RECORDS_EID_COL, MAX_WEIGHT_RECORDS_WEIGHT_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, weight))
    rows = cur.fetchall()
    return len(rows) > 0


def max_weight_record_exercise_exist(db, rid, eid):
    sql = "SELECT * FROM %s WHERE %s=? AND %s=?" % (MAX_WEIGHT_RECORDS_TABLE, MAX_WEIGHT_RECORDS_RID_COL,
                                                    MAX_WEIGHT_RECORDS_EID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid))
    rows = cur.fetchall()
    return len(rows) > 0


def get_max_weight_record_id(db, rid, eid, weight):
    sql = "SELECT %s FROM %s WHERE %s=? AND %s=? AND %s=?" % (MAX_WEIGHT_RECORDS_ID_COL, MAX_WEIGHT_RECORDS_TABLE,
                                                              MAX_WEIGHT_RECORDS_RID_COL, MAX_WEIGHT_RECORDS_EID_COL,
                                                              MAX_WEIGHT_RECORDS_WEIGHT_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, eid, weight))
    row = cur.fetchone()
    if row:
        id = row[MAX_WEIGHT_RECORDS_ID_COL]
    else:
        id = -1
    return id


def get_max_weight_record_ids(db, record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_ID_COL, MAX_WEIGHT_RECORDS_TABLE,
                                            MAX_WEIGHT_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (record_id,))
    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[MAX_WEIGHT_RECORDS_ID_COL])
    return ids


def get_max_weight_records_record_id(db, max_weight_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_RID_COL, MAX_WEIGHT_RECORDS_TABLE,
                                            MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (max_weight_record_id,))
    row = cur.fetchone()
    if row:
        rid = row[MAX_WEIGHT_RECORDS_RID_COL]
    else:
        rid = -1
    return rid


def get_max_weight_records_exercise_id(db, max_weight_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_EID_COL, MAX_WEIGHT_RECORDS_TABLE,
                                            MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (max_weight_record_id,))
    row = cur.fetchone()
    if row:
        eid = row[MAX_WEIGHT_RECORDS_EID_COL]
    else:
        eid = -1
    return eid


def get_max_weight_records_weight(db, max_weight_record_id):
    sql = "SELECT %s FROM %s WHERE %s=?" % (MAX_WEIGHT_RECORDS_WEIGHT_COL, MAX_WEIGHT_RECORDS_TABLE,
                                            MAX_WEIGHT_RECORDS_ID_COL)
    cur = db.cursor()
    cur.execute(sql, (max_weight_record_id,))
    row = cur.fetchone()
    if row:
        weight = row[MAX_WEIGHT_RECORDS_WEIGHT_COL]
    else:
        weight = -1
    return weight


##################################################
# max_weight_records table
##################################################
def body_records_rid_exist(db, rid):
    sql = "SELECT * FROM %s WHERE %s=?" % (BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    rows = cur.fetchall()
    return len(rows) > 0


def get_body_records_weight(db, rid):
    sql = "SELECT %s FROM %s WHERE %s=?" % (BODY_RECORDS_WEIGHT_COL, BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    row = cur.fetchone()
    if row:
        weight = row[BODY_RECORDS_WEIGHT_COL]
    else:
        weight = -1
    return weight


def add_body_records_weight(db, rid, weight):
    if body_records_rid_exist(db, rid):
        raise Exception("Body record already exist!")
    sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL, BODY_RECORDS_WEIGHT_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, weight))
    if not cur.lastrowid:
        raise Exception("Add body record(rid:%s, weight: %s) to database failed" % (rid, weight))
    db.commit()


def update_body_records_weight(db, rid, weight):
    if not body_records_rid_exist(db, rid):
        raise Exception("Body record rid(%s) does not exist!" % rid)
    sql = "UPDATE %s SET %s=? WHERE %s=?" % (BODY_RECORDS_TABLE, BODY_RECORDS_WEIGHT_COL, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (weight, rid))
    if cur.rowcount < 1:
        raise Exception("Update body record failed, rid: %s, weight: %s" % (rid, weight))
    db.commit()


def get_body_records_muscle_weight(db, rid):
    sql = "SELECT %s FROM %s WHERE %s=?" % (BODY_RECORDS_MUSCLE_WEIGHT_COL, BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    row = cur.fetchone()
    if row:
        muscle_weight = row[BODY_RECORDS_MUSCLE_WEIGHT_COL]
    else:
        muscle_weight = -1
    return muscle_weight


def add_body_records_muscle_weight(db, rid, muscle_weight):
    if body_records_rid_exist(db, rid):
        raise Exception("Body record already exist!")
    sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL, BODY_RECORDS_MUSCLE_WEIGHT_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, muscle_weight))
    if not cur.lastrowid:
        raise Exception("Add body record(rid:%s, muscle weight: %s) to database failed" % (rid, muscle_weight))
    db.commit()


def update_body_records_muscle_weight(db, rid, muscle_weight):
    if not body_records_rid_exist(db, rid):
        raise Exception("Body record rid(%s) does not exist!" % rid)
    sql = "UPDATE %s SET %s=? WHERE %s=?" % (BODY_RECORDS_TABLE, BODY_RECORDS_MUSCLE_WEIGHT_COL, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (muscle_weight, rid))
    if cur.rowcount < 1:
        raise Exception("Update body record failed, rid: %s, muscle weight: %s" % (rid, muscle_weight))
    db.commit()


def get_body_records_fat_rate(db, rid):
    sql = "SELECT %s FROM %s WHERE %s=?" % (BODY_RECORDS_FAT_RATE_COL, BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (rid,))
    row = cur.fetchone()
    if row:
        fat_rate = row[BODY_RECORDS_FAT_RATE_COL]
    else:
        fat_rate = -1
    return fat_rate


def add_body_records_fat_rate(db, rid, fat_rate):
    if body_records_rid_exist(db, rid):
        raise Exception("Body record already exist!")
    sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (BODY_RECORDS_TABLE, BODY_RECORDS_RID_COL, BODY_RECORDS_FAT_RATE_COL)
    cur = db.cursor()
    cur.execute(sql, (rid, fat_rate))
    if not cur.lastrowid:
        raise Exception("Add body record(rid:%s, fat rate: %s) to database failed" % (rid, fat_rate))
    db.commit()


def update_body_records_fat_rate(db, rid, fat_rate):
    if not body_records_rid_exist(db, rid):
        raise Exception("Body record rid(%s) does not exist!" % rid)
    sql = "UPDATE %s SET %s=? WHERE %s=?" % (BODY_RECORDS_TABLE, BODY_RECORDS_FAT_RATE_COL, BODY_RECORDS_RID_COL)
    cur = db.cursor()
    cur.execute(sql, (fat_rate, rid))
    if cur.rowcount < 1:
        raise Exception("Update body record failed, rid: %s, fat rate: %s" % (rid, fat_rate))
    db.commit()