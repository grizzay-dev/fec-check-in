import re
import sqlite3
from sqlite3 import Error
from flask import Flask, request, redirect, render_template, url_for
from flask.scaffold import F
from flask.wrappers import Response
from waitress import serve
from werkzeug.utils import redirect
import json
import user as user
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
import os


MAX_LOG_DISPLAY_LEN = 51

#STATIC VARS
DATA_PATH = r"data/users.json"
UPLOAD_FOLDER = r'static/images/users'
ALLOWED_EXTENSIONS = {'png'}

#STATIC VARS2
DB_PATH = r'data/data.db'

#WEB SERVER
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#HELPER METHODS
#Get single user by id
def get_user(id, db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_find_user_by_id = "SELECT * FROM user WHERE id='{0}'".format(id)
        c.execute(q_find_user_by_id)
        rows = c.fetchall()

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
            return rows[0]

#Get all users in db
def get_all_users(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q_find_users = "SELECT * FROM user"
        c.execute(q_find_users)
        rows = c.fetchall()

    except Error as e:
        print(e)

    finally:
        if conn:
            print(rows)
            conn.close()
            return rows

#Checks for allowed file types for profile pictures
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###------------------------------------------------------------------------------------###
###                                   ROUTES                                           ###
###------------------------------------------------------------------------------------###
#ROOT - Status Board.
@app.route('/')
def root():
    data = get_all_users(DB_PATH)
    return render_template("status.html", title="STATUS BOARD", users=data)

#CREATE PROFILE - Create new profile
@app.route("/create", methods=['POST', 'GET'])
def createProfile():
    if request.method == 'GET':
        return render_template("new.html", statusOptions=user.STATUS)
    if request.method == "POST":
        req =request.form
        new_user = user.User(req["fName"], req["lName"], req["email"])
        user.create_user(new_user, DB_PATH)
        return redirect("/")

#USER PROFILE - View / edit user profiles.
@app.route('/id/<id>', methods=['POST', 'GET'])
def profile(id):
    if request.method=='GET':
        u = urlparse(request.base_url)
        profile = get_user(id, DB_PATH)
        profileTitle = "Profile  - {0} {1}".format(profile[2], profile[3])
        return render_template("profile.html", title=profileTitle, user=profile, id = profile[0], statusOptions=user.STATUS, hostname = u.hostname)
    
    elif request.method=='POST':
        req = request.form
        userUpdate = {
                'status': req['status'],
                "fName": req['fName'],
                'lName': req['lName'],
                'email': req['email'],
                'comment': req['comment'],
                'lastmod': user.get_time_stamp()
            }

        user.update_user(id, userUpdate, DB_PATH)
        if 'profilePicture' in request.files:
            file = request.files['profilePicture']
            if file and allowed_file(file.filename ):
                fn = id + ".png"
                fn = secure_filename(fn)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))        
        return redirect("/")

#DELETE PROFILE - Permenantly remove profile
@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    if request.method=='POST':
        user.delete_user(id, DB_PATH)
        return redirect("/")

#UPDATE STATUS - Allows individual users to update their status.
@app.route("/update-status/<id>", methods=['GET', 'POST'])
def updateStatusGet(id):
    if request.method == 'GET':
        profile = get_user(id, DB_PATH)
        return render_template("update-status.html", title="Update Status", id=id, user=profile, statusOptions=user.STATUS)
    
    elif request.method == 'POST':
        req = request.form
        profile = get_user(id, DB_PATH)
        profile = list(profile)
        profile[5] = user.STATUS[int(req['status'])]
        profile[6] = req['comment']
        profile[4] = user.get_time_stamp()
        user_update = {
                'status': profile[5],
                "fName": profile[2],
                'lName': profile[3],
                'email': profile[1],
                'comment': profile[6],
                'lastmod': user.get_time_stamp()
            }
        user.update_user(id, user_update, DB_PATH)
        return redirect("/")
    
#READ ONLY
@app.route("/admin")
def readonly():
    data = get_all_users(DB_PATH)
    return render_template("admin.html", title="STATUS BOARD", users=data)

#LOG FILE
@app.route("/admin/logs")
def logs():
    logs  = user.get_logs(DB_PATH, MAX_LOG_DISPLAY_LEN)
    return render_template("logs.html", title="AUDIT LOGS", logs=logs, logLen = len(logs))


###------------------------------------------------------------------------------------###
###                                   END - ROUTES                                     ###
###------------------------------------------------------------------------------------###

#if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=80)
    




