from re import template
from flask import Flask, request, redirect, render_template
from waitress import serve
from werkzeug.utils import redirect
import json
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

###------------------------------------------------------------------------------------###
###                                   ROUTES                                           ###
###------------------------------------------------------------------------------------###
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
                'comment': req['comment']
            }
        user.updateByID(id, userUpdate)
        return redirect("/")

#DELETE PROFILE - Permenantly remove profile
@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    if request.method=='POST':
        user.deleteUser(id)
        return redirect("/")

#UPDATE STATUS - Allows individual users to update their status.
@app.route("/update-status/<id>", methods=['GET', 'POST'])
def updateStatusGet(id):
    if request.method == 'GET':
        profile = getUserData(id)
        return render_template("update-status.html", title="Update Status", id=id, user=profile, statusOptions=user.STATUS)
    
    elif request.method == 'POST':
        req = request.form
        profile = getUserData(id)
        profile['status'] = user.STATUS[int(req['status'])]
        profile['comment'] = req['comment']
        user.updateByID(id, profile)
        return redirect("/")
    
#READ ONLY
@app.route("/admin")
def readonly():
    data = getUsers()
    return render_template("admin.html", title="STATUS BOARD", users=data)

###------------------------------------------------------------------------------------###
###                                   END - ROUTES                                     ###
###------------------------------------------------------------------------------------###

#if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=8000)
    #app.run(debug=True)





