from os import linesep
import uuid
import os.path
import json

image_path = r"images/users/"
data_path = r"data/users.json"

STATUS = {
    0: 'OUT',
    1: 'IN',
    2: 'WFH',
    3: 'ON LEAVE'
}

def updateByID(id, user):
    with open(data_path, "r") as d:
        tmp = json.load(d)
        tmp[id] = user
        d.close()

    with open(data_path, "wt") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

def create_new(user):
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
            }
            d.close()

        with open(data_path, "r+") as d:
            json.dump(tmp, d, sort_keys=True, indent=4, separators=(',', ': '))
            d.close()

class User:

    def __init__(self, fName, lName, email):
        self.id     = uuid.uuid4()
        self.status = STATUS[0]
        self.fName  = fName
        self.lName  = lName
        self.email  = email

    def convertToJSON(self):
        user = {
            str(self.id): {
                'status': self.status,
                "fName": self.fName,
                'lName': self.lName,
                'email': self.email,
            }
        }
        return user