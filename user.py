#from logging.handlers import RotatingFileHandler
from os import linesep, write
import uuid
import os.path
import json
from datetime import datetime, tzinfo
import sqlite3
from sqlite3 import Error

#LOGGING
MAX_LOG_DISPLAY_LEN = 51

image_path = r"images/users/"

STATUS = {
    0: 'OUT',
    1: 'IN',
    2: 'WFH',
    3: 'ON LEAVE'
}

#helper method to get formatted timestamp as string
def get_time_stamp():
    now = datetime.now()
    nowstr = now.strftime
    return now.strftime("%d/%m/%Y, %H:%M:%S")

#Update user by id - table user
def update_user(id, user, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        #get prev value
        c.execute("SELECT * FROM user WHERE id='{0}'".format(id))
        rows = c.fetchall()
        old_user = rows[0]
        #update value user in db
        q_update_user = "UPDATE user SET email='{0}', fname='{1}', lname='{2}', lastmod='{3}', status='{4}', comment='{5}' WHERE id='{6}'".format(user['email'], user['fName'], user['lName'], user['lastmod'], user['status'], user['comment'], id)
        c.execute(q_update_user)
        conn.commit()
        #write change to log
        write_log(db, "UPDATE", str(old_user), str(user))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#create new user - table user
def create_user(user, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_new_user = "INSERT INTO user (id, email, fname, lname, lastmod, status, comment) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(user.id, user.email, user.fName, user.lName, user.lastmod, user.status, "new user")
        c.execute(q_new_user)
        conn.commit()
        #write change to log
        c.execute("SELECT * FROM user WHERE id='{0}'".format(user.id))
        rows = c.fetchall()
        new_user = rows[0]
        write_log(db, "CREATE", "NA", str(new_user))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#delete existing user - table user
def delete_user(id, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        #get existing user for deletion --> to be saved to audit log
        c.execute("SELECT * FROM user WHERE id='{0}'".format(id))
        rows = c.fetchall()
        user_for_del = rows[0]
        #del existing user
        q_del_user = "DELETE FROM user WHERE id='{0}'".format(id)
        c.execute(q_del_user)
        conn.commit()
        #write change to log
        write_log(db, "DELETE", user_for_del, "user deleted")

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

#write log entry to db - table auditlog
def write_log(db, change, prev, new):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        #replace ' with '' 
        prev = str(prev).replace("'", "''")
        new = str(new).replace("'", "''")
        #build query
        q = "INSERT INTO auditlog (timestamp, change, prev, new) VALUES ('{0}', '{1}', '{2}', '{3}')".format(get_time_stamp(), change, prev, new)
        c.execute(q)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#get x number of logs - table auditlog
def get_logs(db, count):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q = "SELECT * FROM auditlog ORDER BY id DESC LIMIT {0}".format(count)
        c.execute(q)
        rows = c.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return rows

class User:

    def __init__(self, fName, lName, email):
        self.id     = uuid.uuid4()
        self.status = STATUS[0]
        self.fName  = fName
        self.lName  = lName
        self.email  = email
        self.lastmod = get_time_stamp()

