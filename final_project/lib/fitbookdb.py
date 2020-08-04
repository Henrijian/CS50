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

class FitBookDB:
    def __init__(self, db_path):
        print("Connecting with database(%s) ..." % db_path)
        if not isinstance(db_path, str):
            raise Exception("Wrong data type for database path")
        if not os.path.isfile(db_path):
            raise Exception("Database path does not exist")
        try:
            self.db_path = os.path.abspath(db_path)
            self.db = sqlite3.connect(self.db_path, check_same_thread=False)
            self.db.text_factory = str
            self.db.row_factory = lambda cur, row: dict((col[0], row[idx]) for idx, col in enumerate(cur.description))
            self.cur = self.db.cursor()
        except Exception as e:
            raise Exception("Unexpected error happened, message: %s" % e)

    def __del__(self):
        print("Closing database(%s) ..." % self.db_path)
        try:
            self.db.close()
        except Exception as e:
            raise Exception("Unexpected error happened, message: %s" % e)

    ##################################################
    # users table
    ##################################################
    def get_usernames(self):
        sql = "SELECT %s FROM %s" % (USERS_USERNAME_COL, USERS_TABLE)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        usernames = []
        for row in rows:
            usernames.append(row[USERS_USERNAME_COL])
        return usernames

    def get_user_hash(self, username):
        sql = "SELECT %s FROM %s WHERE %s=?" % (USERS_HASH_COL, USERS_TABLE, USERS_USERNAME_COL)
        self.cur.execute(sql, (username,))
        user_hash = ""
        row = self.cur.fetchone()
        if row:
            user_hash = row[USERS_HASH_COL]
        return user_hash

    def get_user_id(self, username):
        sql = "SELECT %s FROM %s WHERE %s=?" % (USERS_ID_COL, USERS_TABLE, USERS_USERNAME_COL)
        self.cur.execute(sql, (username,))
        uid = -1
        row = self.cur.fetchone()
        if row:
            uid = row[USERS_ID_COL]
        return uid

    def username_exist(self, username):
        username = username.lower()
        usernames = self.get_usernames()
        return username in usernames

    def add_user(self, username, hash):
        username = username.lower()
        if self.username_exist(username):
            raise Exception("Username(%s) already exist" % username)

        sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (USERS_TABLE, USERS_USERNAME_COL, USERS_HASH_COL)
        self.cur.execute(sql, (username, hash))
        if not self.cur.lastrowid:
            raise Exception("Add user(%s) to database failed" % username)
        self.db.commit()

    def user_id_exist(self, user_id):
        sql = "SELECT * FROM %s WHERE %s=?" % (USERS_TABLE, USERS_ID_COL)
        self.cur.execute(sql, (user_id,))
        rows = self.cur.fetchall()
        return len(rows) > 0

    ##################################################
    # exercises table
    ##################################################
    def get_exercise_names(self):
        sql = "SELECT %s FROM %s" % (EXERCISES_NAME_COL, EXERCISES_TABLE)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        exercises = []
        for row in rows:
            exercises.append(row[EXERCISES_NAME_COL])
        return exercises

    def get_exercise_name_by_id(self, exercise_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
        self.cur.execute(sql, (exercise_id,))
        row = self.cur.fetchone()
        if row:
            exercise_name = row[EXERCISES_NAME_COL]
        else:
            exercise_name = ""
        return exercise_name

    def get_exercise_type_by_id(self, exercise_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_TYPE_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
        self.cur.execute(sql, (exercise_id,))
        row = self.cur.fetchone()
        if row:
            exercise_type = row[EXERCISES_TYPE_COL]
        else:
            exercise_type = ""
        return exercise_type

    def get_exercise_muscle_group_by_id(self, exercise_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TABLE, EXERCISES_ID_COL)
        self.cur.execute(sql, (exercise_id,))
        row = self.cur.fetchone()
        if row:
            muscle_group = row[EXERCISES_MUSCLE_GROUP_COL]
        else:
            muscle_group = ""
        return muscle_group

    def get_exercise_names_by_muscle_group(self, muscle_group):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL)
        self.cur.execute(sql, (muscle_group,))
        rows = self.cur.fetchall()
        names = []
        for row in rows:
            names.append(row[EXERCISES_NAME_COL])
        return names

    def get_exercise_ids_by_muslce_group(self, muscle_group):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_ID_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL)
        self.cur.execute(sql, (muscle_group,))
        rows = self.cur.fetchall()
        ids = []
        for row in rows:
            ids.append(row[EXERCISES_ID_COL])
        return ids

    def get_exercise_ids_names_by_muscle_group(self, muscle_group):
        sql = "SELECT %s, %s FROM %s WHERE %s=?" % (EXERCISES_ID_COL, EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL)
        self.cur.execute(sql, (muscle_group,))
        rows = self.cur.fetchall()
        exercises = []
        for row in rows:
            id_name_token = (row[EXERCISES_ID_COL], row[EXERCISES_NAME_COL])
            exercises.append(id_name_token)
        return exercises

    def get_exercise_ids_names_by_type(self, exercise_type):
        sql = "SELECT %s, %s FROM %s WHERE %s=?" % (EXERCISES_ID_COL, EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_TYPE_COL)
        self.cur.execute(sql, (exercise_type,))
        rows = self.cur.fetchall()
        exercises = []
        for row in rows:
            id_name_token = (row[EXERCISES_ID_COL], row[EXERCISES_NAME_COL])
            exercises.append(id_name_token)
        return exercises

    def get_strength_exercise_ids_names(self):
        return self.get_exercise_ids_names_by_type(EXERCISE_TYPE_STRENGTH)

    def get_cardio_exercise_ids_names(self):
        return self.get_exercise_ids_names_by_type(EXERCISE_TYPE_CARDIO)

    def get_exercise_names_by_type(self, exercise_type):
        sql = "SELECT %s FROM %s WHERE %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_TYPE_COL)
        self.cur.execute(sql, (exercise_type,))
        rows = self.cur.fetchall()
        exercises = []
        for row in rows:
            exercises.append(row[EXERCISES_NAME_COL])
        return exercises

    def get_cardio_exercise_names(self):
        return self.get_exercise_names_by_type(EXERCISE_TYPE_CARDIO)

    def get_strength_exercise_names(self):
        return self.get_exercise_names_by_type(EXERCISE_TYPE_STRENGTH)

    def get_strength_muscle_groups(self):
        sql = "SELECT %s FROM %s WHERE %s=? GROUP BY(%s)" % (EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TABLE,
                                                              EXERCISES_TYPE_COL, EXERCISES_MUSCLE_GROUP_COL)
        self.cur.execute(sql, (EXERCISE_TYPE_STRENGTH,))
        muslce_groups = []
        rows = self.cur.fetchall()
        for row in rows:
            muslce_groups.append(row[EXERCISES_MUSCLE_GROUP_COL])
        return muslce_groups

    def get_exercise_names_by_muscle_group_and_type(self, muscle_group, exercise_type):
        sql = "SELECT %s FROM %s WHERE %s=? AND %s=?" % (EXERCISES_NAME_COL, EXERCISES_TABLE, EXERCISES_MUSCLE_GROUP_COL, EXERCISES_TYPE_COL)
        self.cur.execute(sql, (muscle_group, exercise_type))
        rows = self.cur.fetchall()
        exercises = []
        for row in rows:
            exercises.append(row[EXERCISES_NAME_COL])
        return exercises

    def get_strength_exercise_names_by_muscle_group(self, muscle_group):
        return self.get_exercise_names_by_muscle_group_and_type(muscle_group, EXERCISE_TYPE_STRENGTH)

    ##################################################
    # muscle_groups table
    ##################################################
    def get_muscle_groups(self):
        sql = "SELECT %s FROM %s" % (MUSCLE_GROUPS_NAME_COL, MUSCLE_GROUPS_TABLE)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        muscle_groups = []
        for row in rows:
            muscle_groups.append(row[MUSCLE_GROUPS_NAME_COL])
        return muscle_groups

    ##################################################
    # records table
    ##################################################
    def add_record_id(self, uid, date):
        if self.get_record_id(uid, date) > 0:
            raise Exception("Record id already exist!")

        if not isinstance(date, datetime.datetime):
            return -1
        date_str = date.strftime(RECORDS_DATE_FMT)

        sql = "INSERT INTO %s (%s, %s) VALUES(?, ?)" % (RECORDS_TABLE, RECORDS_UID_COL, RECORDS_DATE_COL)
        self.cur.execute(sql, (uid, date_str))
        if not self.cur.lastrowid:
            raise Exception("Add record(uid:%s, date: %s) to database failed" % (uid, date_str))
        self.db.commit()

    def get_record_id(self, uid, date):
        if not isinstance(date, datetime.datetime):
            return -1
        date_str = date.strftime(RECORDS_DATE_FMT)
        sql = "SELECT %s FROM %s WHERE %s=? AND %s=?" % (RECORDS_ID_COL, RECORDS_TABLE, RECORDS_UID_COL,
                                                         RECORDS_DATE_COL)
        self.cur.execute(sql, (uid, date_str))
        row = self.cur.fetchone()
        if row:
            rid = row[RECORDS_ID_COL]
        else:
            rid = -1
        return rid

    ##################################################
    # record_details table
    ##################################################
    def add_record_details(self, rid, eid, order):
        if self.get_record_details_id(rid, eid, order) > 0:
            raise Exception("Record details already exist!")

        sql = "INSERT INTO %s (%s, %s, \"%s\") VALUES(?, ?, ?)" % (RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL,
                                                               RECORD_DETAILS_EID_COL, RECORD_DETAILS_ORDER_COL)
        self.cur.execute(sql, (rid, eid, order))
        if not self.cur.lastrowid:
            raise Exception("Add record details(rid:%s, eid: %s, order: %s) to database failed" % (rid, eid, order))
        self.db.commit()

    def get_record_details_id(self, rid, eid, order):
        sql = "SELECT %s FROM %s WHERE %s=? AND %s=? AND \"%s\"=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_TABLE,
                                                                      RECORD_DETAILS_RID_COL, RECORD_DETAILS_EID_COL,
                                                                      RECORD_DETAILS_ORDER_COL)
        self.cur.execute(sql, (rid, eid, order))
        row = self.cur.fetchone()
        if row:
            rdid = row[RECORD_DETAILS_ID_COL]
        else:
            rdid = -1
        return rdid

    def get_record_details_ids(self, rid):
        sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
        self.cur.execute(sql, (rid,))
        rdids = []
        rows = self.cur.fetchall()
        for row in rows:
            rdids.append(row[RECORD_DETAILS_ID_COL])
        return rdids

    def get_record_details_orders(self, rid):
        sql = "SELECT \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
        self.cur.execute(sql, (rid,))
        orders = []
        rows = self.cur.fetchall()
        for row in rows:
            orders.append(row[RECORD_DETAILS_ORDER_COL])
        return orders

    def get_record_details_exercise_order(self, record_details_id):
        sql = "SELECT \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            order = row[RECORD_DETAILS_ORDER_COL]
        else:
            order = -1
        return order

    def get_exercise_id_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_EID_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            eid = row[RECORD_DETAILS_EID_COL]
        else:
            eid = -1
        return eid

    def get_exercise_order_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE, RECORD_DETAILS_ID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            order = row[RECORD_DETAILS_ORDER_COL]
        else:
            order = -1
        return order

    def get_exercise_ids_orders_by_record_id(self, record_id):
        sql = "SELECT %s, %s FROM %s WHERE %s=?" % (RECORD_DETAILS_EID_COL, RECORD_DETAILS_ORDER_COL,
                                                    RECORD_DETAILS_TABLE, RECORD_DETAILS_RID_COL)
        self.cur.execute(sql, (record_id,))
        exercise_ids_orders = []
        rows = self.cur.fetchall()
        for row in rows:
            exercise_ids_orders.append((row[RECORD_DETAILS_EID_COL], row[RECORD_DETAILS_ORDER_COL]))
        return exercise_ids_orders

    def get_rdids_eids_orders_by_record_id(self, record_id):
        sql = "SELECT %s, %s, \"%s\" FROM %s WHERE %s=?" % (RECORD_DETAILS_ID_COL, RECORD_DETAILS_EID_COL,
                                                        RECORD_DETAILS_ORDER_COL, RECORD_DETAILS_TABLE,
                                                        RECORD_DETAILS_RID_COL)
        self.cur.execute(sql, (record_id,))
        rdids_eids_orders = []
        rows = self.cur.fetchall()
        for row in rows:
            rdids_eids_orders.append((row[RECORD_DETAILS_ID_COL], row[RECORD_DETAILS_EID_COL],
                                      row[RECORD_DETAILS_ORDER_COL]))
        return rdids_eids_orders

    ##################################################
    # strength_records table
    ##################################################
    def add_strength_record(self, rdid, set_order, inset_order, weight, reps):
        if self.get_strength_record_id(rdid, set_order, inset_order, weight, reps) > 0:
            raise Exception("Strength record already exist!")
        sql = "INSERT INTO %s (%s, %s, %s, %s, %s) VALUES(?, ?, ?, ?, ?)" % \
              (STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL, STRENGTH_RECORDS_SET_ORDER_COL,
               STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_WEIGHT_COL, STRENGTH_RECORDS_REPS_COL)
        self.cur.execute(sql, (rdid, set_order, inset_order, weight, reps))
        if not self.cur.lastrowid:
            raise Exception("Add strength record (rdid:%s, set_order: %s, inset_order: %s, weight: %s, reps: %s) to database failed" %
                            (rdid, set_order, inset_order, weight, reps))
        self.db.commit()

    def get_strength_record_id(self, rdid, set_order, inset_order, weight, reps):
        sql = "SELECT %s FROM %s WHERE %s=? AND %s=? AND %s=? AND %s=? AND %s=?" % \
              (STRENGTH_RECORDS_ID_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_RDID_COL,
               STRENGTH_RECORDS_SET_ORDER_COL, STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_WEIGHT_COL,
               STRENGTH_RECORDS_REPS_COL)
        self.cur.execute(sql, (rdid, set_order, inset_order, weight, reps))
        row = self.cur.fetchone()
        if row:
            srid = row[STRENGTH_RECORDS_ID_COL]
        else:
            srid = -1
        return srid

    def get_strength_records_ids_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_ID_COL, STRENGTH_RECORDS_TABLE,
                                                STRENGTH_RECORDS_RDID_COL)
        self.cur.execute(sql, (record_details_id,))
        ids = []
        rows = self.cur.fetchall()
        for row in rows:
            ids.append(row[STRENGTH_RECORDS_ID_COL])
        return ids

    def get_set_order_by_strength_record_id(self, strength_record_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_SET_ORDER_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
        self.cur.execute(sql, (strength_record_id,))
        row = self.cur.fetchone()
        if row:
            set_order = row[STRENGTH_RECORDS_SET_ORDER_COL]
        else:
            set_order = -1
        return set_order

    def get_inset_order_by_strength_record_id(self, strength_record_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_INSET_ORDER_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
        self.cur.execute(sql, (strength_record_id,))
        row = self.cur.fetchone()
        if row:
            inset_order = row[STRENGTH_RECORDS_INSET_ORDER_COL]
        else:
            inset_order = -1
        return inset_order

    def get_weight_by_strength_record_id(self, strength_record_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_WEIGHT_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
        self.cur.execute(sql, (strength_record_id,))
        row = self.cur.fetchone()
        if row:
            weight = row[STRENGTH_RECORDS_WEIGHT_COL]
        else:
            weight = -1
        return weight

    def get_reps_by_strength_record_id(self, strength_record_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (STRENGTH_RECORDS_REPS_COL, STRENGTH_RECORDS_TABLE, STRENGTH_RECORDS_ID_COL)
        self.cur.execute(sql, (strength_record_id,))
        row = self.cur.fetchone()
        if row:
            reps = row[STRENGTH_RECORDS_REPS_COL]
        else:
            reps = -1
        return reps

    ##################################################
    # cardio_records table
    ##################################################
    def add_cardio_record(self, rdid, hours, minutes, seconds):
        if self.cardio_record_exist(rdid, hours, minutes, seconds) > 0:
            raise Exception("Cardio record already exist!")
        sql = "INSERT INTO %s (%s, %s, %s, %s) VALUES(?, ?, ?, ?)" %  (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL,
                                                                       CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_MINS_COL,
                                                                       CARDIO_RECORDS_SECS_COL)
        self.cur.execute(sql, (rdid, hours, minutes, seconds))
        if not self.cur.lastrowid:
            raise Exception("Add cardio record (rdid:%s, hours: %s, minutes: %s, seconds: %s) to database failed" %
                            (rdid, hours, minutes, seconds))
        self.db.commit()

    def cardio_record_exist(self, rdid, hours, minutes, seconds):
        sql = "SELECT * FROM %s WHERE %s=? AND %s=? AND %s=? AND %s=?" % (CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL,
                                                                           CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_MINS_COL,
                                                                           CARDIO_RECORDS_SECS_COL)
        self.cur.execute(sql, (rdid, hours, minutes, seconds))
        rows = self.cur.fetchall()
        return len(rows) > 0

    def get_hours_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_HRS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            hours = row[CARDIO_RECORDS_HRS_COL]
        else:
            hours = -1
        return hours

    def get_minutes_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_MINS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            minutes = row[CARDIO_RECORDS_MINS_COL]
        else:
            minutes = -1
        return minutes

    def get_seconds_by_record_details_id(self, record_details_id):
        sql = "SELECT %s FROM %s WHERE %s=?" % (CARDIO_RECORDS_SECS_COL, CARDIO_RECORDS_TABLE, CARDIO_RECORDS_RDID_COL)
        self.cur.execute(sql, (record_details_id,))
        row = self.cur.fetchone()
        if row:
            seconds = row[CARDIO_RECORDS_SECS_COL]
        else:
            seconds = -1
        return seconds