import sqlite3
import os


USERS_TABLE = "users"
USERS_ID_COL = "id"
USERS_USERNAME_COL = "username"
USERS_HASH_COL = "hash"


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
        row = self.cur.fetchone()
        return row[USERS_HASH_COL]

    def get_user_id(self, username):
        sql = "SELECT %s FROM %s WHERE %s=?" % (USERS_ID_COL, USERS_TABLE, USERS_USERNAME_COL)
        self.cur.execute(sql, (username,))
        row = self.cur.fetchone()
        return row[USERS_ID_COL]


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
