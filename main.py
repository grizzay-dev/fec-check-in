from re import template
from flask import Flask, request, redirect, render_template
from waitress import serve

import json

from werkzeug.utils import redirect

import user as user

#STATIC VARS
DATA_PATH = r"data/users.json"

#WEB SERVER
app = Flask(__name__)



#HELPER METHODS
def getUserData(id):
    with open(DATA_PATH, 'r') as data:
        tmp = json.load(data)
        user = tmp[id]
        return user

def getUsers():
    with open(DATA_PATH, 'r') as data:
        tmp = json.load(data)
        return tmp

### ROUTES
#ROOT - Status Board.
@app.route('/')
def root():
    data = getUsers()

    return render_template("status.html", title="STATUS BOARD", users=data)

#CREATE PROFILE - Create new profile
@app.route("/create", methods=['POST', 'GET'])
def createProfile():
    if request.method == 'GET':
        return render_template("new.html", statusOptions=user.STATUS)
    if request.method == "POST":
        req =request.form
        newUser = user.User(req["fName"], req["lName"], req["email"])
        user.createNew(newUser)
        return redirect("/")

#USER PROFILE - View / edit user profiles.
@app.route('/id/<id>', methods=['POST', 'GET'])
def profile(id):
    if request.method=='GET':
        profile = getUserData(id)
        profileTitle = "Profile  - {0} {1}".format(profile['fName'], profile['lName'])
        return render_template("profile.html", title=profileTitle, user=profile, id = id, statusOptions=user.STATUS)
    
    elif request.method=='POST':
        req = request.form
        userUpdate = {
                'status': req['status'],
                "fName": req['fName'],
                'lName': req['lName'],
                'email': req['email'],
            }
        user.updateByID(id, userUpdate)
        return redirect("/")

@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    if request.method=='POST':
        user.deleteUser(id)
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)





