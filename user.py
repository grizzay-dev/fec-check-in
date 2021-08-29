from os import linesep
import uuid
import os.path
import json
from datetime import datetime, tzinfo

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

    with open(data_path, "wt") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

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
            d.close()

        with open(data_path, "r+") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

def deleteUser(id):
    with open(data_path, "r") as d:
        tmp = json.load(d)
        d.close()
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

