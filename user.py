from logging.handlers import RotatingFileHandler
from os import linesep
import uuid
import os.path
import json
from datetime import datetime, tzinfo
import logging
import sqlite3
from sqlite3 import Error

#LOGGING
logger = logging.getLogger("audit_log")
logger.setLevel(logging.WARNING)

ah = RotatingFileHandler("data/audit.log", maxBytes=20, backupCount=5)
ah = logging.FileHandler("data/audit.log")
ah.setLevel(logging.WARNING)

logger.addHandler(ah)
MAX_LOG_DISPLAY_LEN = 51

image_path = r"images/users/"
data_path = r"data/users.json"

STATUS = {
    0: 'OUT',
    1: 'IN',
    2: 'WFH',
    3: 'ON LEAVE'
}

def getTimeStamp():
    now = datetime.now()
    nowstr = now.strftime
    return now.strftime("%d/%m/%Y, %H:%M:%S")

def updateByID(id, user):
    with open(data_path, "r") as d:
        tmp = json.load(d)
        tmp[id] = user
        d.close()
        logger.warning("UPDATED PROFILE: {0}".format(json.dumps(tmp[id])))

    with open(data_path, "wt") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

#update for db
def update_user(id, user, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_update_user = "UPDATE user SET email='{0}', fname='{1}', lname='{2}', lastmod='{3}', status='{4}', comment='{5}' WHERE id='{6}'".format(user['email'], user['fName'], user['lName'], user['lastmod'], user['status'], user['comment'], id)
        c.execute(q_update_user)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

def createNew(user):
        with open(data_path, "r") as d:
            try:
                tmp = json.load(d)
            except:
                print("No data in user file. {0}".format(data_path))
            tmp[str(user.id)] = {
                'status': user.status,
                "fName": user.fName,
                'lName': user.lName,
                'email': user.email,
                'lastmod': user.lastmod
            }
            logger.warning("CREATED PROFILE: {0}".format(json.dumps(tmp[str(user.id)])))
            d.close()

        with open(data_path, "r+") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

#new for db
def create_user(user, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_new_user = "INSERT INTO user (id, email, fname, lname, lastmod, status, comment) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(user.id, user.email, user.fName, user.lName, user.lastmod, user.status, "new user")
        c.execute(q_new_user)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

#delete for db
def delete_user(id, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_del_user = "DELETE FROM user WHERE id='{0}'".format(id)
        c.execute(q_del_user)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

def deleteUser(id):
    with open(data_path, "r") as d:
        tmp = json.load(d)
        d.close()
        logger.warning("DELETED PROFILE: {0}".format(json.dumps(tmp[id])))
        del tmp[id]
        print(tmp)

    with open(data_path, "wt") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

class User:

    def __init__(self, fName, lName, email):
        self.id     = uuid.uuid4()
        self.status = STATUS[0]
        self.fName  = fName
        self.lName  = lName
        self.email  = email
        self.lastmod = getTimeStamp()


    def convertToJSON(self):
        user = {
            str(self.id): {
                'status': self.status,
                "fName": self.fName,
                'lName': self.lName,
                'email': self.email,
                'lastmod': self.lastmod
            }
        }
        return user

